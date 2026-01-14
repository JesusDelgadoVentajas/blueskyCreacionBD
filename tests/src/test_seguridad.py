"""Tests minimalistas para módulo de seguridad."""
import pytest
import os
import pickle
from pathlib import Path
from seguridad.secure_model_handler import SecureModelHandler


class TestSecureModelHandler:
    """Tests para SecureModelHandler."""
    
    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Crea directorio temporal para tests."""
        return tmp_path
    
    @pytest.fixture
    def handler(self, temp_dir):
        """Crea instancia de SecureModelHandler."""
        return SecureModelHandler(temp_dir)
    
    def test_guardar_y_cargar_modelo_simple(self, handler, temp_dir):
        """Test: guardar y cargar un modelo simple."""
        # Crear modelo de prueba
        modelo = {"tipo": "test", "version": 1.0}
        nombre = "test_model.pkl"
        
        # Guardar
        handler.guardar_modelo(modelo, nombre)
        
        # Verificar que existe
        assert (temp_dir / nombre).exists()
        
        # Cargar
        modelo_cargado = handler.cargar_modelo(nombre, verificar_integridad=False)
        
        # Verificar contenido
        assert modelo_cargado == modelo
