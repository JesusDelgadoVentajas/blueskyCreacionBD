"""Tests minimalistas para reglas heurísticas."""
import pytest
from prediccion.utils.heuristics import HeuristicLabeler

class TestBotHeuristics:
    """Tests para HeuristicLabeler real del proyecto."""
    
    @pytest.fixture
    def labeler(self):
        # Configuración simulada pero usada por la clase REAL
        config = {'min_score_bot': 0.5, 'min_score_humano': 0.8}
        return HeuristicLabeler(config)

    def test_detect_bot_high_frequency_real(self, labeler):
        """Test: Validar que el código REAL detecta bots por frecuencia."""
        # Feature map que debería detonar la lógica de bot
        features = {
            'posts_per_day': 150,        # > 100
            'has_avatar': 0,             # Sin avatar
            'bio_length': 0,             # Bio vacía
            'followers_ratio': 0.001     # Ratio bajo
        }
        
        # Llamada al código REAL
        # Debe retornar 1 (Bot) porque score será muy negativo
        veredicto = labeler.label_profile(features)
        assert veredicto == 1

    def test_detect_human_real(self, labeler):
        """Test: Validar que el código REAL detecta humanos."""
        features = {
            'posts_per_day': 5,          # Normal
            'has_avatar': 1,             # Sí avatar
            'bio_length': 150,           # Bio larga
            'followers_ratio': 1.5,      # Ratio saludable
            'followers_count': 500
        }
        veredicto = labeler.label_profile(features)
        assert veredicto == 0 # 0 es Humano

