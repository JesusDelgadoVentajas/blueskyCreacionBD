# 🤖 Detección de Bots - Sistema de Machine Learning

Sistema completo de detección de bots en Bluesky usando XGBoost, con etiquetado automático mediante heurísticas y análisis de 18 características.

## 📋 Descripción

Este módulo permite:
1. **Etiquetar automáticamente** perfiles como bot/humano usando reglas heurísticas
2. **Entrenar modelo XGBoost** con los datos etiquetados
3. **Predecir** si una cuenta específica es bot en tiempo real
4. **Analizar features** que influencian la clasificación

**Accuracy esperado**: 85-92%

---

## 🚀 Inicio Rápido

### Instalación

```bash
pip install xgboost scikit-learn pandas pyyaml numpy
```

### Pipeline Completo (Primera Vez)

```bash
cd prediccion

# Paso 1: Etiquetar datos automáticamente
python scripts/1_etiquetar_datos.py

# Paso 2: Entrenar modelo XGBoost
python scripts/2_entrenar_modelo.py

# Paso 3: Editar config.yaml y especificar usuario
# Luego predecir
python scripts/3_predecir.py
```

### Predicción Diaria (Modelo Ya Entrenado)

```bash
# 1. Edita prediccion/config.yaml
# Cambia: target_handle: "usuario.bsky.social"

# 2. Ejecuta predicción
python scripts/3_predecir.py
```

---

## 📁 Estructura

```
prediccion/
├── config.yaml               # Configuración centralizada
├── README.md                 # Este archivo
│
├── datos/                    # Datasets (generados automáticamente)
│   ├── dataset_etiquetado.csv
│   └── features_extracted.csv
│
├── modelos/                  # Modelos entrenados (generados)
│   ├── bot_detector.pkl
│   ├── feature_scaler.pkl
│   ├── feature_columns.pkl
│   ├── feature_importance.csv
│   └── checksums.json        # Integridad SHA-256
│
├── scripts/
│   ├── 1_etiquetar_datos.py  # Etiquetado automático
│   ├── 2_entrenar_modelo.py  # Entrenamiento XGBoost
│   └── 3_predecir.py         # Predicción de usuario
│
└── utils/
    ├── feature_extraction.py # Extracción de 18 features
    └── heuristics.py         # Reglas de etiquetado
```

---

## 📊 Variables y Sistema de Puntuación (Scoring)

El sistema utiliza una "calculadora de reputación" basada en **18 variables**. Cada perfil comienza con 0 puntos. Según sus características, suma (humano) o resta (bot) puntos.

### 🔴 Indicios de BOT (Restan puntos)
*Señales de comportamiento anómalo o automatizado.*

| Variable | Condición | Puntos | Razón Técnica |
|----------|-----------|--------|---------------|
| **Perfil Fantasma** | `has_avatar`=0 Y `bio_length`<10 | **-4.0** | Abandono total de personalización. |
| **Hiperactividad** | `posts_per_day` > 100 | **-3.5** | Físicamente imposible para un humano sostener este ritmo. |
| **Bebé Spam** | `account_age` < 30d Y `posts` > 300 | **-3.5** | Patrón de creación de cuenta para ataque masivo inmediato. |
| **Ratio Abismal** | `ratio` < 0.01 Y `following` > 500 | **-3.0** | Follow-for-follow fallido (sigue a miles, nadie le sigue). |
| **Nombre de Serie** | `handle_has_many_numbers` = True | **-2.5** | Nombres generados por script (ej: `alex192834`). |
| **Sin Avatar** | `has_avatar` = 0 | **-2.0** | Cuenta 'huevo', descuido típico de bots masivos. |
| **Cadencia Robótica** | `post_interval_std` < 5 seg | **-2.0** | Publica con precisión matemática (cron job). |
| **Amplificador** | `repost_ratio` > 0.8 | **-2.0** | Cuenta dedicada exclusivamente a hacer RT (granja de likes). |
| **Vampiro** | `night_posts_ratio` > 0.4 | **-1.5** | Actividad predominante en horario de sueño (00h-06h). |

### 🟢 Indicios de HUMANO (Suman puntos)
*Señales de esfuerzo, coherencia y vida social.*

| Variable | Condición | Puntos | Razón Técnica |
|----------|-----------|--------|---------------|
| **Perfil Premium** | `has_avatar`=1 Y `bio` > 100 char | **+3.0** | Alta inversión de tiempo en personalizar la identidad. |
| **Veteranía** | `account_age` > 2 años | **+2.5** | Las redes de bots suelen ser efímeras y recientes. |
| **Prueba Social** | `followers` > 1000 | **+2.5** | Difícil de conseguir orgánicamente para un bot simple. |
| **Ratio Saludable** | `followers_ratio` > 0.5 | **+2.0** | Tiene al menos 1 seguidor por cada 2 seguidos. |
| **Poeta** | `vocabulary_diversity` > 0.6 | **+2.0** | Riqueza léxica alta (no repite frases prefabricadas). |
| **Ritmo Humano** | `posts_per_day` entre 1 y 15 | **+2.0** | Rango habitual de actividad de una persona real. |
| **Engagement** | `avg_engagement` > 10 | **+2.0** | Recibe respuestas y likes reales de la comunidad. |
| **Originalidad** | `post_similarity` < 0.2 | **+1.5** | Sus posts son muy distintos entre sí (baja repetición). |

### ⚖️ Veredicto Final (Umbrales)

La calculadora suma todos los puntos y aplica estos cortes para etiquetar el dataset de entrenamiento:

*   🤖 **BOT**: Puntuación Total **≤ -0.5**
*   👤 **HUMANO**: Puntuación Total **≥ 0.8**
*   ❓ **INCIERTO**: Entre -0.5 y 0.8 (Se descartan para mantener la pureza de los datos).

---

## ⚙️ Configuración

Todo se configura en `config.yaml`:

### Predicción

```yaml
prediccion:
  target_handle: "usuario.bsky.social"  # Handle a analizar
  target_did: ""                        # O DID
  num_posts_analizar: 25                # Posts a obtener
  mostrar_features: true                # Mostrar todos los features
  mostrar_top_factores: 5               # Top features influyentes
```

### Modelo

```yaml
modelo:
  xgboost:
    n_estimators: 100     # Número de árboles
    max_depth: 6          # Profundidad máxima
    learning_rate: 0.1    # Tasa de aprendizaje
    min_child_weight: 1
    gamma: 0
    subsample: 0.8
    colsample_bytree: 0.8
  
  threshold_bot: 0.7      # Umbral de clasificación
                          # Más alto = más estricto
```

### Heurísticas

```yaml
heuristicas:
  min_reglas_bot: 3       # Mín. reglas para etiquetar como bot
  min_reglas_humano: 3    # Mín. reglas para etiquetar como humano
```

---

## 📈 Ejemplo de Salida

```
================================================================================
RESULTADO DE LA PREDICCIÓN
================================================================================

👤 Usuario: @suspicious_account.bsky.social
📛 Display Name: Suspicious Bot
🆔 DID: did:plc:abc123...

--------------------------------------------------------------------------------
🤖 CLASIFICACIÓN: BOT
   Probabilidad: 87.3%
--------------------------------------------------------------------------------

📊 Probabilidades:
  • Humano: 12.7%
  • Bot:    87.3%
  • Threshold usado: 0.7

🔍 Top factores que influenciaron la decisión:
  1. posts_per_day                = 127.5432
  2. handle_has_many_numbers      = 1.0000
  3. has_avatar                   = 0.0000
  4. followers_ratio              = 0.0024
  5. account_age_days             = 7.0000
```

---

## 🔄 Re-entrenar Modelo

Si obtienes más datos con el scraper:

```bash
# 1. Obtén más datos
cd Main
python main.py

# 2. Re-etiqueta con los nuevos datos
cd ../prediccion
python scripts/1_etiquetar_datos.py

# 3. Re-entrena el modelo
python scripts/2_entrenar_modelo.py
```

El modelo se guardará con nuevos checksums SHA-256 automáticamente.

---

## 🎯 Ajustar Sensibilidad

### Muchos Falsos Positivos (Humanos → Bot)

**Solución**: Aumentar threshold

```yaml
modelo:
  threshold_bot: 0.8  # Más estricto (era 0.7)
```

### Muchos Falsos Negativos (Bots → Humano)

**Solución**: Disminuir threshold

```yaml
modelo:
  threshold_bot: 0.6  # Más sensible (era 0.7)
```

---

## 🛡️ Seguridad

El módulo utiliza `SecureModelHandler` para:

- ✅ **Checksums SHA-256**: Detecta modificaciones no autorizadas en modelos
- ✅ **Permisos Restrictivos**: Modelos guardados con permisos 0o600
- ✅ **Validación Automática**: Verifica integridad al cargar modelos
- ✅ **Registro de Integridad**: `modelos/checksums.json`

Verificar integridad de modelos:

```bash
cd ..
python verificar_seguridad.py
```

---

## 🛠️ Troubleshooting

### Error: No module named 'xgboost'

**Solución**:
```bash
pip install xgboost scikit-learn pandas pyyaml numpy
```

### Error: No se encontró el modelo

**Causa**: No has entrenado el modelo aún.

**Solución**: Ejecuta los pasos 1 y 2 del pipeline.

### Error: No se pudo obtener el perfil

**Causa**: Handle/DID incorrecto o usuario no existe.

**Solución**: Verifica el valor de `target_handle` o `target_did` en `config.yaml`.

### Modelo predice todo como humano/bot

**Causa**: Etiquetado heurístico sesgado o threshold incorrecto.

**Solución**:
- Ajusta `min_reglas_bot` y `min_reglas_humano` en `config.yaml`
- Ajusta `threshold_bot`
- Re-entrena con más datos

### Checksum inválido

**Causa**: El modelo fue modificado externamente.

**Solución**: Re-entrena el modelo desde cero:
```bash
rm -rf modelos/
python scripts/2_entrenar_modelo.py
```

---

## 📊 Métricas Esperadas

Con un buen etiquetado heurístico y suficientes datos:

- **Accuracy**: 85-92%
- **Precision**: 80-88% (de los que dice bot, cuántos lo son)
- **Recall**: 75-85% (de todos los bots, cuántos detecta)
- **AUC-ROC**: 0.88-0.94

---

## 💡 Mejoras Futuras

1. **Etiquetado Manual**: UI para revisar y corregir etiquetas
2. **Más Features**: Análisis de red de seguidores, NLP avanzado
3. **Modelos Avanzados**: LSTM para análisis temporal, BERT para texto
4. **API REST**: FastAPI para predicciones en tiempo real
5. **Dashboard**: Streamlit para visualización interactiva
6. **Batch Processing**: Analizar múltiples usuarios a la vez

---

## 📚 Documentación Relacionada

- **Configuración**: [`../configuracion/README.md`](../configuracion/README.md)
- **Seguridad**: [`../seguridad/README.md`](../seguridad/README.md)
- **Proyecto general**: [`../README.md`](../README.md)

---

## 🎓 Tecnologías Utilizadas

- **XGBoost**: Modelo de clasificación gradient boosting
- **Scikit-learn**: Preprocessing, métricas, train/test split
- **Pandas**: Manejo de datasets
- **NumPy**: Cálculos numéricos
- **YAML**: Configuración
- **Bluesky API**: Obtención de datos en tiempo real

---

✅ **Sistema completo, probado y listo para usar!**
