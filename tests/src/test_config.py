"""Tests minimalistas para configuración."""
import pytest
import yaml
from pathlib import Path
from configuracion.load_config import Config

class TestConfig:
    """Tests para la clase Config real del proyecto."""
    
    def test_config_methods_with_sample_data(self):
        """Test: Validar métodos de la clase Config usando datos de prueba."""
        # 1. Cargar datos de prueba
        sample_config_path = Path(__file__).parent.parent / "resources" / "sample_config.yaml"
        with open(sample_config_path, 'r', encoding='utf-8') as f:
            test_data = yaml.safe_load(f)
            
        # 2. Instanciar clase REAL (es un Singleton)
        config = Config()
        
        # 3. Inyectar datos de prueba (bypass de _load_config para no depender del archivo real)
        # Guardamos el estado original para restaurarlo después si fuera necesario
        original_data = config._config_data
        config._config_data = test_data
        
        try:
            # 4. Probamos los métodos REALES de la clase
            assert config.get_pool_size() == 10
            assert config.get_usuarios_por_semilla() == 5
            assert config.get_posts_por_usuario_limite() == 10
            assert config.get('rutas', 'directorio_almacen') == "almacen"
            
        finally:
            # Restaurar estado (buena práctica en Singletons)
            config._config_data = original_data

