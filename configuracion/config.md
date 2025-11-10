# Instalar la librería
pip install atproto


Lo siguiente lo tenemos que escribir en la terminal. La contraseña no es con la que iniciamos sesion, es una
"Contraseña de Aplicación" (o App Password). Es una contraseña especial que generas dentro de Bluesky y que le
da acceso a tu script (o a cualquier aplicación de terceros) sin que tengas que darle tu contraseña principal.
Esta en:
1. Inicia sesión en Bluesky (generalmente es más fácil desde la versión web en un computador).
2. Ve a "Settings" (Configuración) en el menú lateral.
3. Busca la sección de seguridad. Dentro de ella, encontrarás una opción llamada "App Passwords" (Contraseñas de Aplicación).
4. Pulsa el botón para "Add App Password" (Añadir contraseña de aplicación).
5. Te pedirá que le pongas un nombre a esta contraseña. Esto es solo para que tú la identifiques. Ponle algo claro, como "Mi Script de Python" o "Bot de Pruebas".
6. Bluesky te generará la contraseña. Tendrá un formato como: xxxx-xxxx-xxxx-xxxx.
7. ¡MUY IMPORTANTE! Copia esa contraseña y guárdala en un lugar seguro inmediatamente. Bluesky solo te la mostrará una vez. Si la pierdes antes de usarla, tendrás que borrarla y generar una nueva.

# Configurar variables de entorno (Linux/macOS)
export BSKY_HANDLE="tu-usuario.bsky.social"
export BSKY_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx" # Tu contraseña de aplicación

# Configurar variables de entorno (Windows CMD)
$env:BSKY_HANDLE = "tu_usuario.bsky.social"
$env:BSKY_APP_PASSWORD = "aqui-va-la-contraseña-de-app-xxxx-xxxx"