# 🦋 Proyecto Bluesky - Análisis y Detección de Bots

Sistema completo de extracción, análisis y detección de bots en la red social Bluesky utilizando machine learning.

## 📋 Descripción General

Este proyecto permite:
1. **Extracción de datos** de usuarios y publicaciones de Bluesky
2. **Análisis descriptivo** de perfiles y comportamientos usando PySpark
3. **Detección de bots** mediante machine learning (XGBoost)
4. **Seguridad robusta** con validación de archivos y modelos

---

## 🚀 Inicio Rápido

### Instalación de Dependencias

```bash
# Opción recomendada: instalar desde requirements.txt
pip install -r requirements.txt

# O instalar manualmente las dependencias principales:
pip install atproto pyspark xgboost scikit-learn pandas pyyaml numpy matplotlib seaborn flask
```

### Configuración de Credenciales

Genera una contraseña de aplicación en Bluesky:
1. Inicia sesión en [Bluesky Web](https://bsky.app)
2. Ve a **Configuracion** → **Seguridad** → **Contrasenas de aplicacion**
3. Genera una nueva contraseña (formato: `xxxx-xxxx-xxxx-xxxx`)

Configura las variables de entorno (Windows PowerShell):
```powershell
$env:BSKY_HANDLE = "tu_usuario.bsky.social"
$env:BSKY_APP_PASSWORD = "xxxx-xxxx-xxxx-xxxx"
```

### Ejecución Básica

```bash
# 1. Extraer datos de seguidores y posts
python Main/main.py

# 2. Ejecutar análisis descriptivo
cd analisis
python main_analisis.py

# 3. Entrenar modelo de detección de bots
cd ../prediccion
python scripts/1_etiquetar_datos.py
python scripts/2_entrenar_modelo.py

# 4. Predecir si un usuario es bot
python scripts/3_predecir.py

## 🕸️ Interfaz Web (opcional)

Se anadio una interfaz minima en `web/` para analizar un handle/DID desde el navegador.

Cómo usarla (desarrollo):

```bash
source .venv/bin/activate
pip install -r requirements.txt
export BSKY_HANDLE=your_handle
export BSKY_APP_PASSWORD=your_app_password
python web/app.py
# abrir http://127.0.0.1:5000
```

Nota: La interfaz es para uso local; si la despliegas, anade autenticacion y HTTPS.
```

---

## 📁 Estructura del Proyecto

```
bluesky2/
├── almacen/                      # Datos extraídos (JSON)
│   ├── posts_usuarios.json       # Posts de usuarios
│   └── profiles_to_scan.json     # Perfiles escaneados
│
├── analisis/                     # Análisis descriptivo (PySpark)
│   ├── main_analisis.py          # Script principal de análisis
│   ├── generar_graficos.py       # Generación de 25-30 gráficos
│   ├── exportador_markdown.py    # Exporta resultados a Markdown
│   ├── carga_datos.py            # Carga segura de datos JSON
│   ├── analizar_profiles.py      # Análisis de perfiles
│   ├── analizar_post.py          # Análisis de publicaciones
│   ├── spark_utils.py            # Configuración de Spark
│   └── resultados/               # Resultados y gráficos generados
│
├── configuracion/                # Configuración centralizada
│   ├── config.yaml               # Configuración principal
│   └── load_config.py            # Cargador de configuración
│
├── gestor/                       # Gestión de conexiones
│   └── conexion.py               # Cliente Bluesky
│
├── Main/                         # Scripts principales
│   └── main.py                   # Extracción de datos
│
├── prediccion/                   # Detección de bots (ML)
│   ├── scripts/                  # Scripts del pipeline
│   │   ├── 1_etiquetar_datos.py  # Etiquetado automático
│   │   ├── 2_entrenar_modelo.py  # Entrenamiento XGBoost
│   │   ├── 3_predecir.py         # Predicción de bots
│   │   └── check_results.py      # Verificación de resultados
│   ├── utils/                    # Utilidades
│   │   ├── feature_extraction.py # Extracción de características
│   │   └── heuristics.py         # Reglas heurísticas
│   ├── datos/                    # Datasets generados
│   └── modelos/                  # Modelos entrenados
│
├── seguridad/                    # Módulo de seguridad
│   ├── secure_file_handler.py    # Manejo seguro de archivos
│   └── secure_model_handler.py   # Manejo seguro de modelos
│
├── usuarios/                     # Obtención de usuarios
│   ├── info.py                   # Extracción de perfiles
│   └── post.py                   # Extracción de posts
│
├── web/                          # Interfaz web (Flask)
│   ├── app.py                    # Aplicación Flask
│   ├── templates/                # Plantillas HTML
│   └── static/                   # Archivos estáticos (CSS/JS)
│
├── EXPLICACION_NO_TECNICA_SCRIPTS.md  # Guía no técnica
├── SECURITY_REPORT.md            # Reporte de seguridad
└── verificar_seguridad.py        # Script de auditoría
```

---

## 🔧 Configuración

Toda la configuración se gestiona desde `configuracion/config.yaml`:

```yaml
# Modificar parámetros de scraping
scraping:
  usuarios_por_semilla: 10
  pool_size: 12

# Modificar límite de posts
posts:
  posts_por_usuario_limite: 25
  delay_entre_requests: 1

# Modificar memoria de Spark
spark:
  driver_memory: "8g"
  executor_memory: "8g"
```

**No necesitas modificar código Python** - todos los scripts leen automáticamente desde el YAML.

---

## 📊 Componentes Principales

### 1. Extracción de Datos
- **Ubicación**: `Main/main.py`, `usuarios/`
- **Función**: Obtiene seguidores y posts de cuentas Bluesky
- **Salida**: `almacen/profiles_to_scan.json`, `almacen/posts_usuarios.json`
- **Documentación**: Ver [`usuarios/README.md`](usuarios/README.md)

### 2. Análisis Descriptivo
- **Ubicación**: `analisis/`
- **Función**: Analiza patrones de perfiles y publicaciones con PySpark
- **Características nuevas**:
  - Genera automáticamente reporte Markdown completo
  - Crea 25-30 gráficos visuales (histogramas, mapas de calor, evolución temporal)
  - Exporta tablas Spark formateadas
- **Salida**: `analisis/resultados/analisis_descriptivo.md` + gráficos PNG
- **Documentación**: Ver [`analisis/README.md`](analisis/README.md)

### 3. Detección de Bots
- **Ubicación**: `prediccion/`
- **Función**: Entrena modelo XGBoost para clasificar bots
- **Caracteristicas**: 18 caracteristicas (perfil + comportamiento)
- **Precision**: ~85-92%
- **Documentación**: Ver [`prediccion/README.md`](prediccion/README.md)

### 4. Interfaz Web
- **Ubicación**: `web/`
- **Función**: Interfaz web Flask para análisis interactivo de usuarios
- **Características**:
  - Analiza cualquier handle o DID de Bluesky
  - Muestra probabilidad de bot en tiempo real
  - Visualiza características extraídas
- **Uso**: `python web/app.py` (requiere credenciales en variables de entorno)
- **Documentación**: Ver [`web/README.md`](web/README.md)

### 5. Seguridad
- **Ubicación**: `seguridad/`
- **Función**: Protección contra path traversal, pickle RCE, y más
- **Funciones**: Checksums SHA-256, validacion de rutas, permisos restrictivos
- **Documentación**: Ver [`seguridad/README.md`](seguridad/README.md) y [`SECURITY_REPORT.md`](SECURITY_REPORT.md)

---

## ⚙️ Requisitos del Sistema

- **Python**: 3.13 o superior
- **Java**: JDK 17 (para PySpark)
- **RAM**: Mínimo 8GB (16GB recomendado para Spark)
- **Sistema Operativo**: Windows, Linux, macOS

### Configurar Java 17 (Windows)

```powershell
$env:JAVA_HOME = "C:\Program Files\Java\jdk-17"
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
java -version  # Debe mostrar versión 17
```

---

## 🔒 Seguridad

El proyecto implementa varias capas de seguridad:

- ✅ **Prevencion de path traversal**: Validacion estricta de rutas
- ✅ **Proteccion contra RCE en pickle**: Checksums SHA-256 en modelos ML
- ✅ **Mitigacion de TOCTOU**: Operaciones atomicas de archivos
- ✅ **Permisos restrictivos**: Archivos sensibles con permisos 0o600
- ✅ **Proteccion de symlinks**: Resolucion segura de enlaces simbolicos

Verificar seguridad del sistema:
```bash
python verificar_seguridad.py
```

---

## 📈 Flujo de Trabajo Típico

```
1. EXTRACCIÓN DE DATOS
   └─ python Main/main.py
   └─ Genera: almacen/profiles_to_scan.json, posts_usuarios.json

2. ANÁLISIS DESCRIPTIVO
   └─ cd analisis
   └─ python main_analisis.py
   └─ Genera: resultados/analisis_descriptivo.md

3. DETECCIÓN DE BOTS
   └─ cd prediccion
   └─ python scripts/1_etiquetar_datos.py
   └─ python scripts/2_entrenar_modelo.py
   └─ Edita config.yaml (target_handle)
   └─ python scripts/3_predecir.py
```

---

## 🛠️ Solución de Problemas

### Error: Version de Java no coincide
**Solucion**: Configura Java 17 como se indica en la seccion de requisitos.

### Error: Limite de tasa excedido
**Solucion**: El script espera automaticamente. Aumenta `delay_entre_requests` en `config.yaml`.

### Error: Sin memoria (Spark)
**Solucion**: Aumenta `driver_memory` y `executor_memory` en `config.yaml`.

### Error: Actor not found
**Solucion**: Normal, algunos usuarios borran sus cuentas. El script los salta automaticamente.

---

## 📚 Documentación Adicional

- **Análisis**: [`analisis/README.md`](analisis/README.md)
- **Configuración**: [`configuracion/README.md`](configuracion/README.md)
- **Predicción**: [`prediccion/README.md`](prediccion/README.md)
- **Seguridad**: [`seguridad/README.md`](seguridad/README.md) | [`SECURITY_REPORT.md`](SECURITY_REPORT.md)
- **Usuarios**: [`usuarios/README.md`](usuarios/README.md)
- **Interfaz Web**: [`web/README.md`](web/README.md)
- **Guía No Técnica**: [`EXPLICACION_NO_TECNICA_SCRIPTS.md`](EXPLICACION_NO_TECNICA_SCRIPTS.md)

---

## 🎯 Estado del Proyecto

- ✅ Extracción de perfiles y posts
- ✅ Análisis descriptivo con PySpark
- ✅ Generación automática de reportes Markdown con gráficos
- ✅ Sistema de detección de bots con XGBoost (18 características)
- ✅ Interfaz web Flask para predicción interactiva
- ✅ Módulo de seguridad implementado (checksums, validación de rutas)
- ✅ Configuración centralizada (YAML)
- ✅ Documentación técnica y no técnica completa
- ⏳ Scraping completo de todos los usuarios (~77.6% pendiente)

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT.
