# 🧪 Tests - Proyecto Bluesky

Suite de tests minimalista para validar las funciones más importantes del proyecto.

## Estructura

```
tests/
├── __init__.py
├── src/                          # Tests
│   ├── test_seguridad.py         # Tests de seguridad
│   ├── test_features.py          # Tests de extracción de características
│   ├── test_heuristics.py        # Tests de reglas heurísticas
│   └── test_config.py            # Tests de configuración
└── resources/                    # Datos de prueba
    └── sample_config.yaml        # Configuración de prueba
```

## Ejecutar Tests

### Todos los tests
```bash
pytest
```

### Tests específicos
```bash
# Solo tests de seguridad
pytest tests/src/test_seguridad.py

# Solo tests de features
pytest tests/src/test_features.py

# Solo tests de heurísticas
pytest tests/src/test_heuristics.py

# Solo tests de configuración
pytest tests/src/test_config.py
```

### Con más detalle
```bash
pytest -v
```

### Con cobertura
```bash
pytest --cov=seguridad --cov=prediccion --cov=configuracion
```

## Tests Implementados

### 1. `test_seguridad.py`
- ✅ Guardar y cargar modelos
- ✅ Validación de rutas seguras
- ✅ Generación de checksums

### 2. `test_features.py`
- ✅ Extracción de características de perfil
- ✅ Cálculo de ratios
- ✅ Manejo de posts vacíos

### 3. `test_heuristics.py`
- ✅ Detección de bots por alta frecuencia
- ✅ Detección de bots por ratio bajo
- ✅ Clasificación de usuarios normales
- ✅ Detección de bots por posts cortos

### 4. `test_config.py`
- ✅ Carga de configuración
- ✅ Obtención de parámetros
- ✅ Acceso a rutas configuradas

## Requisitos

```bash
pip install pytest
```

## Notas

- Los tests son **minimalistas** y se centran en funcionalidad core
- Usan **fixtures** de pytest para datos de prueba
- No requieren conexión a Bluesky (usan datos mock)
- Rápidos de ejecutar (~1-2 segundos)
