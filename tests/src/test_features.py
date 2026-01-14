"""Tests minimalistas para extracción de características."""
import pytest
from prediccion.utils.feature_extraction import FeatureExtractor

class TestFeatureExtractor:
    """Tests para FeatureExtractor real del proyecto."""
    
    @pytest.fixture
    def extractor(self):
        return FeatureExtractor()

    def test_extract_profile_features_real(self, extractor):
        """Test: Validar que la clase real extrae features correctamente."""
        # FeatureExtractor espera snake_case
        profile = {
            "followers_count": 100, 
            "follows_count": 50, 
            "posts_count": 10, 
            "created_at": "2020-01-01T00:00:00.000Z"
        }
        posts = [{"text": "a", "createdAt": "2024-01-01T00:00:00.000Z", "likeCount": 0, "replyCount": 0, "repostCount": 0}]
        
        # Llamada al código REAL
        features = extractor.extract_profile_features(profile, posts)
        
        # Validar lógica REAL
        assert features['followers_ratio'] == 2.0
        assert features['posts_count'] == 10
        
    def test_zero_posts_features_real(self, extractor):
        """Test: Validar comportamiento con 0 posts."""
        profile = {"followers_count": 100, "follows_count": 50, "posts_count": 0}
        features = extractor.extract_profile_features(profile, [])
        assert features['avg_post_length'] == 0

