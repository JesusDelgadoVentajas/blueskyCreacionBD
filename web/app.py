"""Simple Flask web UI to run the bot predictor for a given handle/DID.

Security notes:
- The app uses `gestor/conexion.ConexionBluesky` and expects `BSKY_HANDLE` and
  `BSKY_APP_PASSWORD` environment variables to be set for API access.
- Models are loaded using `seguridad.SecureModelHandler` and checksums are verified.

Usage (development):
  pip install -r requirements.txt
  export BSKY_HANDLE=your_handle
  export BSKY_APP_PASSWORD=your_app_password
  python web/app.py
  # open http://127.0.0.1:5000
"""
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so internal imports like `prediccion` work
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')

# Import internal utilities lazily (so app can import even if deps missing until used)
def load_prediction_components():
    """Lazily import internal modules used for prediction.

    Raises a clear ImportError if the package imports fail, with hints to fix
    PYTHONPATH or to run the app from the repository root / activated venv.
    """
    try:
        from prediccion.utils.feature_extraction import FeatureExtractor
        from seguridad.secure_model_handler import SecureModelHandler
        from gestor.conexion import ConexionBluesky
    except ModuleNotFoundError as e:
        # Provide a helpful message for troubleshooting import issues
        raise ImportError(
            "Could not import internal modules. Ensure you run the app from the project "
            "root, the virtualenv is activated, and PYTHONPATH includes the repository root. "
            f"Original error: {e}"
        ) from e

    return FeatureExtractor, SecureModelHandler, ConexionBluesky


def generar_explicacion(features, prob_bot, es_bot):
    """Genera una explicación detallada con frase principal y 5 puntos específicos."""
    puntos = []
    
    # Analizar ratio seguidores/seguidos
    ratio = features.get('follower_following_ratio', 0)
    followers = features.get('followers_count', 0)
    following = features.get('following_count', 0)
    if ratio < 0.1:
        puntos.append(f"Ratio seguidores/seguidos muy bajo ({ratio:.2f}): sigue a {following} cuentas pero solo tiene {followers} seguidores")
    elif ratio > 10:
        puntos.append(f"Ratio seguidores/seguidos muy alto ({ratio:.2f}): tiene {followers} seguidores pero solo sigue a {following} cuentas")
    else:
        puntos.append(f"Ratio seguidores/seguidos equilibrado ({ratio:.2f}): {followers} seguidores y {following} seguidos")
    
    # Analizar frecuencia de posts
    posts_dia = features.get('posts_per_day', 0)
    total_posts = features.get('posts_count', 0)
    if posts_dia > 50:
        puntos.append(f"Frecuencia de publicación muy alta: {posts_dia:.1f} posts/día ({total_posts} posts totales)")
    elif posts_dia < 0.1:
        puntos.append(f"Frecuencia de publicación muy baja: {posts_dia:.2f} posts/día ({total_posts} posts totales)")
    else:
        puntos.append(f"Frecuencia de publicación normal: {posts_dia:.1f} posts/día ({total_posts} posts totales)")
    
    # Analizar longitud de posts
    longitud = features.get('avg_post_length', 0)
    if longitud < 20:
        puntos.append(f"Posts muy cortos (promedio {longitud:.0f} caracteres): posible contenido automatizado o spam")
    elif longitud > 200:
        puntos.append(f"Posts extensos (promedio {longitud:.0f} caracteres): contenido elaborado y detallado")
    else:
        puntos.append(f"Longitud de posts normal (promedio {longitud:.0f} caracteres)")
    
    # Analizar edad de cuenta vs actividad
    dias_cuenta = features.get('account_age_days', 0)
    if dias_cuenta < 30:
        if posts_dia > 10:
            puntos.append(f"Cuenta muy nueva ({dias_cuenta} días) con actividad sospechosamente alta")
        else:
            puntos.append(f"Cuenta reciente ({dias_cuenta} días) con actividad normal para un usuario nuevo")
    elif dias_cuenta > 365:
        puntos.append(f"Cuenta establecida ({dias_cuenta} días, ~{dias_cuenta/365:.1f} años) con historial prolongado")
    else:
        puntos.append(f"Cuenta con {dias_cuenta} días de antigüedad")
    
    # Analizar interacciones
    avg_likes = features.get('avg_likes_per_post', 0)
    avg_replies = features.get('avg_replies_per_post', 0)
    if avg_likes < 1 and avg_replies < 1:
        puntos.append(f"Muy poca interacción: promedio de {avg_likes:.1f} likes y {avg_replies:.1f} respuestas por post")
    elif avg_likes > 10 or avg_replies > 5:
        puntos.append(f"Alta interacción comunitaria: promedio de {avg_likes:.1f} likes y {avg_replies:.1f} respuestas por post")
    else:
        puntos.append(f"Interacción moderada: promedio de {avg_likes:.1f} likes y {avg_replies:.1f} respuestas por post")
    
    # Asegurar que tenemos exactamente 5 puntos
    puntos = puntos[:5]
    
    # Construir explicación con frase principal y lista
    if es_bot:
        frase = f"🤖 <strong>Clasificado como BOT</strong> con {prob_bot:.1%} de confianza."
    else:
        frase = f"👤 <strong>Clasificado como HUMANO</strong> con {(1-prob_bot):.1%} de confianza."
    
    return {'frase': frase, 'puntos': puntos}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/healthz', methods=['GET'])
def healthz():
    return 'OK', 200


@app.errorhandler(405)
def method_not_allowed(_error):
    flash('Método no permitido. Te llevamos al inicio.', 'warning')
    return redirect(url_for('index'))


@app.route('/predict', methods=['POST'])
def predict():
    identifier = request.form.get('identifier', '').strip()
    id_type = request.form.get('id_type', 'handle')

    if not identifier:
        flash('Debes indicar un handle o DID para analizar.', 'danger')
        return redirect(url_for('index'))

    try:
        FeatureExtractor, SecureModelHandler, ConexionBluesky = load_prediction_components()
    except ImportError as e:
        flash(str(e), 'danger')
        return redirect(url_for('index'))

    # Load model components
    base_dir = Path(__file__).parent.parent / 'prediccion'
    modelos_dir = base_dir / 'modelos'
    handler = SecureModelHandler(modelos_dir)

    try:
        model = handler.cargar_modelo('bot_detector.pkl', verificar_integridad=True)
        scaler = handler.cargar_modelo('feature_scaler.pkl', verificar_integridad=True)
        feature_cols = handler.cargar_modelo('feature_columns.pkl', verificar_integridad=True)
    except Exception as e:
        flash(f'Error cargando el modelo: {e}', 'danger')
        return redirect(url_for('index'))

    # Obtain profile and posts
    conexion = ConexionBluesky()
    client = None
    try:
        client = conexion.get_client()
    except Exception as e:
        flash(f'Error conectando a Bluesky: {e}', 'danger')
        return redirect(url_for('index'))

    identifier_arg = identifier if id_type == 'handle' else identifier
    try:
        profile_resp = client.get_profile(actor=identifier_arg)
        profile = profile_resp.model_dump(mode='json')
    except Exception as e:
        flash(f'No se pudo obtener el perfil: {e}', 'warning')
        return redirect(url_for('index'))

    # Get posts
    try:
        # default to 25 posts (same as config)
        posts_response = client.get_author_feed(actor=identifier_arg, limit=25)
        posts = []
        for item in posts_response.feed:
            post = item.post
            posts.append({'text': post.record.text, 'createdAt': post.record.created_at,
                          'likeCount': post.like_count, 'replyCount': post.reply_count,
                          'repostCount': post.repost_count})
    except Exception:
        posts = []

    # Extract features and predict
    extractor = FeatureExtractor()
    features = extractor.extract_profile_features(profile, posts)

    import pandas as pd
    X = pd.DataFrame([features])[feature_cols]
    X_scaled = scaler.transform(X)
    prob = model.predict_proba(X_scaled)[0]
    prob_humano, prob_bot = prob[0], prob[1]
    threshold = 0.7
    es_bot = prob_bot > threshold

    # Generar explicación
    explicacion = generar_explicacion(features, prob_bot, es_bot)

    result = {
        'handle': profile.get('handle'),
        'did': profile.get('did'),
        'prob_humano': float(prob_humano),
        'prob_bot': float(prob_bot),
        'es_bot': bool(es_bot),
        'threshold': threshold,
        'explicacion': explicacion,
        'features': {k: float(v) for k, v in features.items() if isinstance(v, (int, float))}
    }

    return render_template('result.html', result=result)



if __name__ == '__main__':
    # Allow overriding the port cleanly without changing the code each time.
    port = int(os.environ.get('PORT', '5000'))
    # When running in a background process (nohup, &), the reloader can fail
    # due to missing terminal; disable the reloader to avoid termios errors.
    app.run(debug=True, use_reloader=False, port=port)
