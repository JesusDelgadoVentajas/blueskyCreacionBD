# Configuración del Proyecto Bluesky

Este documento contiene toda la información necesaria para configurar y ejecutar el proyecto de análisis de datos de Bluesky.

---

## 📦 Instalación de Dependencias

### Librería de Bluesky (atproto)

```bash
pip install atproto
```

---

## 🔑 Configuración de Credenciales de Bluesky

### ¿Qué es una App Password?

**IMPORTANTE:** No uses tu contraseña principal de Bluesky. Debes generar una **Contraseña de Aplicación** (App Password), que es una contraseña especial para scripts y aplicaciones de terceros.

### Cómo generar una App Password

1. Inicia sesión en [Bluesky Web](https://bsky.app) desde un navegador
2. Ve a **Settings** (Configuración) en el menú lateral
3. Busca la sección **Security** (Seguridad)
4. Encuentra la opción **App Passwords** (Contraseñas de Aplicación)
5. Haz clic en **Add App Password** (Añadir contraseña de aplicación)
6. Ponle un nombre descriptivo (ej: "Script de Análisis Python", "Bot de Investigación")
7. Bluesky generará una contraseña con formato: `xxxx-xxxx-xxxx-xxxx`

> ⚠️ **¡MUY IMPORTANTE!** Copia y guarda esta contraseña inmediatamente. Bluesky solo la mostrará una vez. Si la pierdes, deberás generar una nueva.

### Configurar Variables de Entorno

#### Windows (PowerShell)

```powershell
$env:BSKY_HANDLE = "tu_usuario.bsky.social"
$env:BSKY_APP_PASSWORD = "xxxx-xxxx-xxxx-xxxx"
```

#### Linux/macOS (Bash)

```bash
export BSKY_HANDLE="tu-usuario.bsky.social"
export BSKY_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"
```

---

## ☕ Configuración de Java para PySpark

El script de análisis (`main_analisis.py`) requiere **Java 17** para ejecutar PySpark correctamente.

### Verificar Versiones de Java Instaladas

```powershell
dir "C:\Program Files\Java"
```

### Configurar Java 17 (Windows PowerShell)

```powershell
# Configurar JAVA_HOME para Java 17
$env:JAVA_HOME = "C:\Program Files\Java\jdk-17"
$env:Path = "$env:JAVA_HOME\bin;$env:Path"

# Verificar la versión
java -version
# Debe mostrar: java version "17.0.x"
```

### Hacer la Configuración Permanente (Opcional)

Para no tener que configurar Java 17 cada vez que abras PowerShell:

1. Busca "Variables de entorno" en el menú de Windows
2. En "Variables del sistema", edita `JAVA_HOME` → `C:\Program Files\Java\jdk-17`
3. Edita `Path` → Asegúrate que `%JAVA_HOME%\bin` esté al principio

---

## 🚀 Ejecutar los Scripts

### Script de Análisis Principal

```powershell
cd C:\Escritorio\bluesky2\analisis
python main_analisis.py
```

O desde cualquier directorio:

```powershell
python C:\Escritorio\bluesky2\analisis\main_analisis.py
```

---

## 📝 Notas del Proyecto

### Estrategia de Recolección de Datos

- **Método de muestreo:** Usar el enfoque de "semillas" (similar a Twitter Bot 22)
- **Semillas iniciales:** Aproximadamente 10 personas muy famosas por categoría
- **Muestreo secundario:** De cada semilla, descargar 5 usuarios al azar
- **Categorías recomendadas por Sheng:**
  - Deportes
  - Política y noticias
  - Entretenimiento
  - Tecnología
  - Ciencia

> Este enfoque proporciona un espectro más amplio y representativo de la red social.

### Información a Capturar por Perfil

- ✅ Handle y DID (identificador único)
- ✅ Nombre de usuario y descripción
- ✅ Fecha de creación de la cuenta
- ✅ Verificación y estado
- ⏳ **Por implementar:**
  - Conteo de seguidores y seguidos
  - Número de posts, reposts y likes
  - Frecuencia de publicación (actividad temporal)

### Análisis de Posts

- [ ] Revisar los últimos 1000 posts y documentar los repetidos
- [ ] Extraer palabras clave y términos recurrentes
- [ ] Identificar chavisms/spam keywords
- [ ] Detectar hashtags repetidos (especialmente 3-6 hashtags en el mismo orden)

---

## 🔧 Solución de Problemas Comunes

### Error: "java.lang.UnsupportedClassVersionError"

**Causa:** Estás usando Java 8 en lugar de Java 17.

**Solución:** Configura Java 17 como se indica en la sección "Configuración de Java".

### Error: "[PATH_NOT_FOUND] Path does not exist"

**Causa:** Las rutas de los archivos JSON son incorrectas.

**Solución:** Verifica que los archivos existan en `C:\Escritorio\bluesky2\almacen\`

### Error: Variables de entorno no reconocidas

**Causa:** Las variables de entorno solo duran la sesión actual de PowerShell.

**Solución:** Configura las variables de entorno cada vez que abras PowerShell, o hazlas permanentes mediante las configuraciones del sistema.
