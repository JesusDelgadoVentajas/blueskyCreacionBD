"""Tests para el módulo gestor (Gestión de usuarios y conexión)."""
import pytest
import os
import json
from unittest.mock import MagicMock, patch
from gestor.conexion import ConexionBluesky
from gestor.info import datosUsuario

class TestGestor:
    """Suite de tests para el módulo Gestor."""
    
    def test_conexion_missing_credentials(self):
        """Test: Validar que falla si no se proveen credenciales."""
        # Asegurar que no hay variables de entorno que interfieran
        with patch.dict(os.environ, {}, clear=True):
            conexion = ConexionBluesky(handle=None, app_password=None)
            with pytest.raises(ValueError, match="Configura BSKY_HANDLE"):
                conexion.conectar()
                
    def test_save_profiles_deduplication(self, tmp_path):
        """Test: Validar que save_profiles elimina duplicados por DID."""
        # Mockear ruta del proyecto para que use carpeta temporal
        with patch("gestor.info.Path") as mock_path:
            mock_path.return_value.parent.parent = tmp_path
            
            # Crear directorio 'almacen' dentro del tmp_path
            almacen = tmp_path / "almacen"
            almacen.mkdir(parents=True, exist_ok=True)
            
            # Instanciar clase
            gestor_usuario = datosUsuario("mock_user", "mock_pass")
            
            # Crear archivo existente con 1 perfil
            archivo_destino = "profiles_test.json"
            perfil_existente = {"did": "did:plc:1", "handle": "user1.bsky.social"}
            
            # Guardamos manualmente el archivo inicial
            with open(almacen / archivo_destino, "w") as f:
                json.dump([perfil_existente], f)
                
            # Nuevos perfiles (uno nuevo, uno duplicado)
            nuevos_perfiles = [
                {"did": "did:plc:2", "handle": "user2.bsky.social"}, # Nuevo
                {"did": "did:plc:1", "handle": "user1.bsky.social"}  # Duplicado
            ]
            
            # Ejecutar función
            gestor_usuario.save_profiles(nuevos_perfiles, output_filename=archivo_destino)
            
            # Verificar resultado
            with open(almacen / archivo_destino, "r") as f:
                resultado = json.load(f)
            
            # Debería haber 2 perfiles, NO 3
            assert len(resultado) == 2
            dids = [p["did"] for p in resultado]
            assert "did:plc:1" in dids
            assert "did:plc:2" in dids
