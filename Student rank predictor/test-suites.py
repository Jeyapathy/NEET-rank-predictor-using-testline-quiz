# backend/tests/test_ml_models.py
import pytest
import numpy as np
from app.ml.models import FeatureEngineering, RankPredictor

@pytest.fixture
def sample_quiz_data():
    return {
        'responses': [
            {
                'question_id': 1,
                'selected_option_id': 2,
                'correct_option_id': 2,
                'topic': 'Physics',
                'time_taken': 60
            },
            {
                'question_id': 2,
                'selected_option_id': 3,
                'correct_option_id': 4,
                'topic': 'Chemistry',
                'time_taken': 45
            }
        ],
        'total_score': 85,
        'total_time': 105
    }

@pytest.fixture
def sample_history():
    return [
        {'total_score': 80, 'total_time': 100},
        {'total_score': 85, 'total_time': 95},
        {'total_score': 90, 'total_time': 90}
    ]

class TestFeatureEngineering:
    def test_extract_topic_features(self, sample_quiz_data):
        fe = FeatureEngineering()
        features = fe.extract_topic_features(sample_quiz_data['responses'])
        
        assert 'Physics_accuracy' in features
        assert 'Chemistry_accuracy' in features
        assert features['Physics_accuracy'] == 1.0
        assert features['Chemistry_accuracy'] == 0.0
        
    def test_extract_temporal_features(self, sample_history):
        fe = FeatureEngineering()
        features = fe.extract_temporal_features(sample_history)
        
        assert 'avg_score' in features
        assert 'score_trend' in features
        assert features['avg_score'] == pytest.approx(85.0)
        assert features['score_trend'] > 0  # Positive trend

class TestRankPredictor:
    def test_prediction_structure(self, sample_quiz_data, sample_history):
        predictor = RankPredictor()
        # Mock training data
        X_train = np.random.rand(100, 10)
        y_train = np.random.randint(1000, 10000, 100)
        predictor.train