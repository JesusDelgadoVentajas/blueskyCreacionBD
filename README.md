# Proyecto Bluesky Data Extractor

## Descripción General
Este proyecto permite la extracción y análisis de datos de usuarios y publicaciones de la red social Bluesky. Utiliza la API de Bluesky para autenticar usuarios, obtener seguidores y recopilar publicaciones.

### Funcionalidades Principales
1. **Autenticación y Seguidores**:
   - Maneja la autenticación y la obtención de seguidores de una cuenta Bluesky.
   - Los seguidores se guardan en un archivo JSON para su posterior procesamiento.
   - Los datos obtenidos incluyen información detallada del perfil, actividad y relación con el usuario objetivo.

2. **Extracción de Publicaciones**:
   - Inicia sesión en Bluesky, carga perfiles de un archivo JSON, obtiene los posts de cada usuario y guarda los resultados en otro archivo JSON.
   - Diseñado para reanudar el proceso en caso de interrupciones o errores, evitando repetir trabajo ya realizado.

---

## Instalación

### Requisitos
- Python 3.13 o superior
- Librerías necesarias:
  ```bash
  pip install atproto
  ```

### Configuración
1. Genera una contraseña de aplicación en Bluesky:
   - Inicia sesión en Bluesky (preferiblemente desde la versión web).
   - Ve a "Settings" (Configuración) > "App Passwords" (Contraseñas de Aplicación).
   - Genera una nueva contraseña y guárdala en un lugar seguro.

2. Configura las variables de entorno:
   - En Linux/macOS:
     ```bash
     export BSKY_HANDLE="tu-usuario.bsky.social"
     export BSKY_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"
     ```
   - En Windows (CMD):
     ```powershell
     $env:BSKY_HANDLE = "tu_usuario.bsky.social"
     $env:BSKY_APP_PASSWORD = "xxxx-xxxx-xxxx-xxxx"
     ```

---

## Uso

### Ejecución Principal
El archivo `main.py` es el punto de entrada principal del proyecto. Ejecuta la extracción de seguidores y publicaciones:
```bash
python Main/main.py
```

### Detalles del Proceso
1. **Obtención de Nuevos Usuarios**:
   - Cuando ejecutas `main.py`, el script obtiene seguidores del usuario objetivo y los guarda en `profiles_to_scan.json`.
   - Si el archivo ya existe, se añaden solo los nuevos seguidores, evitando duplicados.

2. **Extracción de Posts**:
   - La clase `BlueskyPostsFetcher` procesa los perfiles en `profiles_to_scan.json`.
   - Antes de procesar, verifica el progreso guardado en `posts_usuarios.json` y carga los `DID` de los usuarios cuyos posts ya han sido recogidos.
   - Solo se procesan los usuarios que no están en `processed_dids`, es decir, aquellos cuyos posts aún no han sido recogidos.

3. **Interrupciones en el Proceso**:
   - Si el proceso de extracción de posts se detiene, el progreso se guarda automáticamente en `posts_usuarios.json`.
   - Al reanudar el script, se procesan únicamente los usuarios pendientes.

---

## Estructura del Proyecto
```
bluesky2/
├── almacen/
│   ├── posts_usuarios.json
│   ├── profiles_to_scan.json
├── configuracion/
│   ├── config.md
├── gestor/
│   ├── conexion.py
├── Main/
│   ├── main.py
├── usuarios/
│   ├── info.py
│   ├── post.py
```

---

## Notas Adicionales
- **Reanudar Procesos**: El proyecto está diseñado para reanudar procesos interrumpidos automáticamente.
- **Gestión de Usuarios y Posts**: Los usuarios nuevos se añaden a `profiles_to_scan.json`, y los posts pendientes se procesan de manera incremental.

---

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para sugerencias o mejoras.

---

## Licencia
Este proyecto está bajo la licencia MIT.