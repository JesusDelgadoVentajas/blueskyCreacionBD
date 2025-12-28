# 🤖 Detector de Bots para Bluesky

Sistema de machine learning para detectar cuentas bot en Bluesky usando XGBoost.

## 📁 Estructura del Proyecto

```
prediccion/
├── config.yaml              # Configuración centralizada
├── README.md               # Este archivo
│
├── datos/                  # Datasets generados (creados automáticamente)
│   ├── dataset_etiquetado.csv
│   └── features_extracted.csv
│
├── modelos/                # Modelos entrenados (creados automáticamente)
│   ├── bot_detector.pkl
│   ├── feature_scaler.pkl
│   ├── feature_columns.pkl
│   └── feature_importance.csv
│
├── scripts/                # Scripts principales
│   ├── 1_etiquetar_datos.py     # Paso 1: Etiquetar con heurísticas
│   ├── 2_entrenar_modelo.py     # Paso 2: Entrenar XGBoost
│   └── 3_predecir.py            # Paso 3: Predecir usuarios
│
└── utils/                  # Módulos auxiliares
    ├── __init__.py
    ├── feature_extraction.py    # Extracción de features
    └── heuristics.py            # Reglas heurísticas
```

---

## 🚀 Uso Rápido

### **Paso 1: Etiquetar Datos (Solo primera vez)**

```bash
cd prediccion
python scripts/1_etiquetar_datos.py
```

**¿Qué hace?**
- Lee `almacen/profiles_to_scan.json` y `almacen/posts_usuarios.json`
- Aplica reglas heurísticas para etiquetar automáticamente como bot/humano
- Genera `datos/dataset_etiquetado.csv` (dataset de entrenamiento)

**Salida esperada:**
```
📊 Etiquetado completado:
  • Bots: 2,345
  • Humanos: 8,234
  • Inciertos: 4,321
✓ Dataset final: 10,579 perfiles etiquetados
```

---

### **Paso 2: Entrenar Modelo (Solo primera vez, o para re-entrenar)**

```bash
python scripts/2_entrenar_modelo.py
```

**¿Qué hace?**
- Lee el dataset etiquetado
- Entrena un modelo XGBoost
- Evalúa métricas (accuracy, precision, recall, AUC)
- Guarda el modelo entrenado en `modelos/`

**Salida esperada:**
```
📊 Evaluando modelo...
              precision    recall  f1-score   support
      Humano       0.88      0.92      0.90      1647
         Bot       0.85      0.78      0.81       469
    accuracy                           0.87      2116
🎯 AUC-ROC: 0.9234
```

---

### **Paso 3: Predecir Usuario**

**3.1. Edita `config.yaml` y especifica el usuario:**

```yaml
prediccion:
  target_handle: "suspicious_account.bsky.social"  # O:
  target_did: ""  # did:plc:abc123...
```

**3.2. Ejecuta la predicción:**

```bash
python scripts/3_predecir.py
```

**Salida esperada:**
```
================================================================================
RESULTADO DE LA PREDICCIÓN
================================================================================

👤 Usuario: @suspicious_account.bsky.social
📛 Display Name: Suspicious Account
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

## ⚙️ Configuración

Todo se configura en `config.yaml`:

### **Modificar Parámetros del Modelo**

```yaml
modelo:
  xgboost:
    n_estimators: 100      # Número de árboles (más = mejor pero más lento)
    max_depth: 6           # Profundidad (más = más complejo)
    learning_rate: 0.1     # Tasa de aprendizaje
  
  threshold_bot: 0.7       # Umbral de decisión (subir = más estricto)
```

### **Modificar Heurísticas**

```yaml
heuristicas:
  min_reglas_bot: 3        # Mín. reglas para etiquetar como bot
  min_reglas_humano: 3     # Mín. reglas para etiquetar como humano
```

### **Configurar Predicción**

```yaml
prediccion:
  target_handle: ""        # Handle a analizar
  target_did: ""           # O DID a analizar
  num_posts_analizar: 25   # Cuántos posts usar
  mostrar_features: true   # Mostrar todos los features
  mostrar_top_factores: 5  # Top N factores más importantes
```

---

## 📊 Features Utilizados

El sistema extrae **18 features** de cada perfil:

### **Features de Perfil (9)**
1. `account_age_days` - Edad de la cuenta
2. `followers_count` - Número de seguidores
3. `following_count` - Número de seguidos
4. `followers_ratio` - Ratio followers/following
5. `posts_count` - Total de posts
6. `has_avatar` - Tiene avatar (0/1)
7. `bio_length` - Longitud de la biografía
8. `display_name_length` - Longitud del nombre
9. `handle_has_many_numbers` - Handle con patrón numérico (0/1)

### **Features de Comportamiento (9)**
10. `posts_per_day` - Posts promedio por día
11. `avg_post_length` - Longitud promedio de posts
12. `std_post_length` - Desviación estándar de longitud
13. `post_interval_std` - Regularidad temporal de posts
14. `night_posts_ratio` - % de posts nocturnos (00:00-06:00)
15. `repost_ratio` - % de reposts
16. `url_ratio` - % de posts con URLs
17. `avg_engagement` - Engagement promedio (likes + replies)
18. `vocabulary_diversity` - Diversidad de vocabulario
19. `post_similarity_avg` - Similitud promedio entre posts

---

## 🔧 Heurísticas de Etiquetado

### **Reglas para Identificar Bots**
- Cuenta nueva (<30 días) + muy activa (>500 posts)
- Muy pocos seguidores (<10) y muchos seguidos (>1000)
- Sin avatar + bio vacía
- Handle con muchos números (ej: `user12345678`)
- Posts muy frecuentes (>50 por día)
- Intervalos de posts muy regulares
- Muchos posts nocturnos (24/7)
- Alta ratio de reposts

### **Reglas para Identificar Humanos**
- Cuenta antigua (>1 año)
- Perfil completo (avatar + bio >50 chars)
- Engagement saludable (>100 followers, ratio >0.1)
- Actividad moderada (0.1-10 posts/día)
- Alta diversidad de vocabulario
- Contenido variado (baja similitud entre posts)

---

## 📈 Métricas Esperadas

Con un buen etiquetado heurístico, el modelo debería alcanzar:

- **Accuracy**: 85-92%
- **Precision**: 80-88% (de los que dice bot, cuántos lo son)
- **Recall**: 75-85% (de todos los bots, cuántos detecta)
- **AUC-ROC**: 0.88-0.94

---

## 🛠️ Mantenimiento

### **Re-entrenar con Nuevos Datos**

Si obtienes más perfiles:

```bash
# 1. Ejecuta el scraping para obtener más datos
cd ../Main
python main.py

# 2. Re-etiqueta con los nuevos datos
cd ../prediccion
python scripts/1_etiquetar_datos.py

# 3. Re-entrena el modelo
python scripts/2_entrenar_modelo.py
```

### **Ajustar el Threshold**

Si tienes muchos **falsos positivos** (humanos marcados como bots):
```yaml
threshold_bot: 0.8  # Más estricto (antes 0.7)
```

Si tienes muchos **falsos negativos** (bots que pasan como humanos):
```yaml
threshold_bot: 0.6  # Más sensible (antes 0.7)
```

---

## 🐛 Troubleshooting

### **Error: No module named 'xgboost'**
```bash
pip install xgboost scikit-learn pandas pyyaml
```

### **Error: No se encontró el archivo de configuración**
Asegúrate de estar en la carpeta `prediccion/` al ejecutar los scripts.

### **Error: No se pudo obtener el perfil**
- Verifica que el handle/DID sea correcto
- Asegúrate de tener credenciales configuradas en `configuracion/contraseñas.properties`

### **Modelo predice todo como humano/bot**
- Re-entrena con más datos
- Ajusta heurísticas en `config.yaml`
- Revisa la distribución de labels en el dataset etiquetado

---

## 💡 Próximos Pasos

1. **Etiquetado Manual**: Para mejorar precisión, etiquetar manualmente 100-200 casos
2. **Feature Engineering**: Añadir más features (ej: análisis de red de seguidores)
3. **Modelos Avanzados**: Probar LSTM para análisis temporal o BERT para texto
4. **API**: Crear API REST con FastAPI para predicciones en tiempo real
5. **Dashboard**: Visualizar métricas y predicciones con Streamlit

---

## 📚 Referencias

- XGBoost: https://xgboost.readthedocs.io/
- Scikit-learn: https://scikit-learn.org/
- Bluesky API: https://docs.bsky.app/

---

¿Preguntas? Revisa el código fuente o contacta al desarrollador.
