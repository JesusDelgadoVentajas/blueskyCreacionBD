# 🤖 Sistema de Detección de Bots - Resumen de Implementación

## ✅ Archivos Creados

### **Configuración**
- ✅ `prediccion/config.yaml` - Configuración centralizada del sistema
- ✅ `prediccion/.gitignore` - Ignorar archivos generados

### **Documentación**
- ✅ `prediccion/README.md` - Documentación completa
- ✅ `prediccion/QUICKSTART.md` - Guía de inicio rápido

### **Scripts Principales**
- ✅ `prediccion/scripts/1_etiquetar_datos.py` - Etiquetado heurístico
- ✅ `prediccion/scripts/2_entrenar_modelo.py` - Entrenamiento XGBoost
- ✅ `prediccion/scripts/3_predecir.py` - Predicción de usuarios

### **Módulos de Utilidades**
- ✅ `prediccion/utils/__init__.py` - Init del módulo
- ✅ `prediccion/utils/feature_extraction.py` - Extracción de 18 features
- ✅ `prediccion/utils/heuristics.py` - Reglas de etiquetado

### **Carpetas**
- ✅ `prediccion/datos/` - Para datasets (se genera automáticamente)
- ✅ `prediccion/modelos/` - Para modelos entrenados (se genera automáticamente)

---

## 🎯 Flujo Complete

```
PASO 1: Etiquetar Datos
└─ Lee: almacen/profiles_to_scan.json + posts_usuarios.json
└─ Extrae: 18 features por perfil
└─ Aplica: Reglas heurísticas (bot/humano)
└─ Crea: datos/dataset_etiquetado.csv

PASO 2: Entrenar Modelo
└─ Lee: datos/dataset_etiquetado.csv
└─ Entrena: XGBoost con 18 features
└─ Evalúa: Métricas (accuracy, precision, recall, AUC)
└─ Guarda: modelos/bot_detector.pkl + scaler + columns

PASO 3: Predecir Usuario
└─ Lee config.yaml: target_handle o target_did
└─ Obtiene datos: API Bluesky (perfil + 25 posts)
└─ Extrae features: Mismos 18 features
└─ Predice: Probabilidad de bot (0-1)
└─ Clasifica: Bot si prob > threshold (default 0.7)
```

---

## 📊 Features Implementados (18 total)

### Perfil (9)
1. account_age_days
2. followers_count
3. following_count
4. followers_ratio
5. posts_count
6. has_avatar
7. bio_length
8. display_name_length
9. handle_has_many_numbers

### Comportamiento (9)
10. posts_per_day
11. avg_post_length
12. std_post_length
13. post_interval_std
14. night_posts_ratio
15. repost_ratio
16. url_ratio
17. avg_engagement
18. vocabulary_diversity
19. post_similarity_avg

---

## 🔧 Heurísticas Implementadas

### Reglas Bot (8)
1. Cuenta nueva + muy activa
2. Pocos followers + muchos following
3. Sin avatar + sin bio
4. Handle con patrón numérico
5. Posts muy frecuentes
6. Intervalos regulares
7. Muchos posts nocturnos
8. Alta ratio de reposts

### Reglas Humano (7)
1. Cuenta antigua
2. Perfil completo
3. Engagement saludable
4. Actividad moderada
5. Vocabulario diverso
6. Contenido variado
7. Engagement alto

---

## 🚀 Cómo Usar

### Primera Vez (Setup Completo)

```bash
# 1. Instalar dependencias
pip install xgboost scikit-learn pandas pyyaml numpy

# 2. Etiquetar datos
cd prediccion
python scripts/1_etiquetar_datos.py

# 3. Entrenar modelo
python scripts/2_entrenar_modelo.py

# 4. Predecir (edita config.yaml primero)
python scripts/3_predecir.py
```

### Uso Diario (Solo Predicción)

```bash
# 1. Edita config.yaml
vim prediccion/config.yaml
# Cambia: target_handle: "usuario.bsky.social"

# 2. Ejecuta predicción
python scripts/3_predecir.py
```

---

## ⚙️ Configuración en config.yaml

```yaml
# USUARIO A ANALIZAR
prediccion:
  target_handle: ""  # ← Pon aquí el handle
  target_did: ""     # O el DID

# PARÁMETROS DEL MODELO
modelo:
  threshold_bot: 0.7  # ← Ajusta sensibilidad

# HEURÍSTICAS
heuristicas:
  min_reglas_bot: 3     # ← Mín. reglas para etiquetar
  min_reglas_humano: 3
```

---

## 📈 Salida Esperada

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

🔍 Top factores:
  1. posts_per_day = 127.5432
  2. handle_has_many_numbers = 1.0000
  3. has_avatar = 0.0000
  4. followers_ratio = 0.0024
  5. account_age_days = 7.0000
```

---

## 🎓 Tecnologías Usadas

- **XGBoost**: Modelo de clasificación
- **Scikit-learn**: Preprocessing y métricas
- **Pandas**: Manejo de datos
- **NumPy**: Cálculos numéricos
- **YAML**: Configuración
- **Bluesky API**: Obtención de datos en tiempo real

---

## ✨ Características Destacadas

✅ Configuración centralizada en YAML
✅ Etiquetado automático con heurísticas
✅ 18 features engineered
✅ Modelo XGBoost optimizado
✅ Predicción en tiempo real desde handle/DID
✅ Top factores que influencian decisión
✅ Métricas de evaluación completas
✅ Documentación exhaustiva
✅ Modular y extensible

---

## 🔮 Próximas Mejoras Posibles

1. **Etiquetado Manual**: UI para revisar y etiquetar casos
2. **Feature Engineering**: Más features (análisis de red, NLP avanzado)
3. **Modelos Avanzados**: LSTM, Transformers
4. **API REST**: FastAPI para integración
5. **Dashboard**: Streamlit para visualización
6. **Batch Processing**: Analizar múltiples usuarios a la vez

---

## 📚 Archivos de Referencia

- **README.md**: Documentación completa
- **QUICKSTART.md**: Guía de inicio rápido
- **config.yaml**: Configuración con comentarios

---

✅ **Sistema completo y listo para usar!**
