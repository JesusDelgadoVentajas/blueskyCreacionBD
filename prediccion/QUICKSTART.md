# ═══════════════════════════════════════════════════════════════
# GUÍA DE INICIO RÁPIDO - DETECTOR DE BOTS
# ═══════════════════════════════════════════════════════════════

## 📦 Instalación de Dependencias

Primero, asegúrate de tener todas las librerías necesarias:

```bash
pip install xgboost scikit-learn pandas pyyaml numpy
```

---

## 🚀 Ejecutar el Sistema Completo

### **Opción 1: Paso a Paso (Recomendado para primera vez)**

```bash
cd prediccion

# Paso 1: Etiquetar datos con heurísticas
python scripts/1_etiquetar_datos.py

# Paso 2: Entrenar modelo
python scripts/2_entrenar_modelo.py

# Paso 3: Edita config.yaml y pon el handle a analizar
# Luego ejecuta la predicción
python scripts/3_predecir.py
```

### **Opción 2: Script Todo-en-Uno**

Si ya etiquetaste y entrenaste, solo usa:

```bash
python scripts/3_predecir.py
```

---

## 📝 Ejemplo de Uso

### **1. Configurar Usuario a Analizar**

Edita `config.yaml`:

```yaml
prediccion:
  target_handle: "elonmusk.bsky.social"  # Pon aquí el handle
  target_did: ""
```

### **2. Ejecutar Predicción**

```bash
python scripts/3_predecir.py
```

### **3. Ver Resultado**

```
🤖 CLASIFICACIÓN: BOT
   Probabilidad: 87.3%

📊 Probabilidades:
  • Humano: 12.7%
  • Bot:    87.3%

🔍 Top factores:
  1. posts_per_day = 127.54
  2. handle_has_many_numbers = 1.00
  3. has_avatar = 0.00
```

---

## ⚙️ Configuración Rápida

### **Ajustar Sensibilidad**

```yaml
modelo:
  threshold_bot: 0.7  # Bajar = más sensible, Subir = más estricto
```

### **Cambiar Número de Posts Analizados**

```yaml
prediccion:
  num_posts_analizar: 25  # Cambiar a 50, 100, etc.
```

---

## 🔧 Troubleshooting

**Problema: "No se encontró el modelo"**
→ Ejecuta primero los pasos 1 y 2

**Problema: "No se pudo obtener el perfil"**
→ Verifica el handle/DID en config.yaml

**Problema: "ModuleNotFoundError: No module named 'xgboost'"**
→ `pip install xgboost`

---

## 📖 Más Información

Lee el `README.md` completo para detalles sobre:
- Features utilizados
- Heurísticas de etiquetado
- Métricas del modelo
- Mantenimiento y mejoras
