# Proyecto Bluesky Data Extractor

## Descripción General
Este proyecto permite la extracción y análisis de datos de usuarios y publicaciones de la red social Bluesky. Utiliza la API de Bluesky para autenticar usuarios, obtener seguidores y recopilar publicaciones. Además, incluye un detector de bots basado en redes neuronales simples.

### Funcionalidades Principales
1. **Autenticación y Seguidores**:
   - Maneja la autenticación y la obtención de seguidores de una cuenta Bluesky.
   - Los seguidores se guardan en un archivo JSON para su posterior procesamiento.
   - Los datos obtenidos incluyen información detallada del perfil, actividad y relación con el usuario objetivo.

2. **Extracción de Publicaciones**:
   - Inicia sesión en Bluesky, carga perfiles de un archivo JSON, obtiene los posts de cada usuario y guarda los resultados en otro archivo JSON.
   - Diseñado para reanudar el proceso en caso de interrupciones o errores, evitando repetir trabajo ya realizado.

3. **Detección de Bots**:
   - Implementa una red neuronal simple para clasificar usuarios como bots o no bots usando datos de perfiles.

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

### Clases Principales

#### Clase `datosUsuario`
- **Descripción**: Maneja la autenticación y obtención de seguidores de una cuenta Bluesky.
- **Datos Obtenidos**:
  - **Datos de usuario**: DID, handle, display_name, description, avatar, pronouns, created_at.
  - **Datos de actividad**: indexed_at, labels, verification, status.
  - **Datos de visor**: blocked_by, blocking, following, followed_by, muted.
  - **Datos técnicos**: associated, py_type.

#### Clase `BlueskyPostsFetcher`
- **Descripción**: Extrae posts de usuarios de Bluesky.
- **Datos Obtenidos**:
  - cid: Identificador único del contenido.
  - uri: Identificador único del post.
  - createdAt: Fecha y hora de creación.
  - text: Contenido textual del post.
  - replyCount: Número de respuestas.
  - repostCount: Número de veces compartido.
  - likeCount: Número de "me gusta".
  - hasEmbed: Indica si contiene contenido incrustado.

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
├── Modelo/
│   ├── octopus.py
├── usuarios/
│   ├── info.py
│   ├── post.py
```

---

## Notas Adicionales
- **Reanudar Procesos**: El proyecto está diseñado para reanudar procesos interrumpidos automáticamente.
- **Detección de Bots**: Usa características como longitud del handle, avatar, y biografía para clasificar usuarios.

---

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para sugerencias o mejoras.

---

## Licencia
Este proyecto está bajo la licencia MIT. (Permite el uso, copia, modificación y distribución del software).