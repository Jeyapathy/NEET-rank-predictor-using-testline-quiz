# ml_models.py
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

class FeatureEngineering:
    def __init__(self):
        self.scaler = StandardScaler()
        
    def extract_topic_features(self, responses: List[Dict]) -> Dict[str, float]:
        """Extract performance metrics for each topic."""
        topic_stats = {}
        for response in responses:
            topic = response['topic']
            if topic not in topic_stats:
                topic_stats[topic] = {'correct': 0, 'total': 0, 'time': []}
            
            topic_stats[topic]['total'] += 1
            topic_stats[topic]['correct'] += (
                response['selected_option_id'] == response['correct_option_id']
            )
            topic_stats[topic]['time'].append(response['time_taken'])
        
        features = {}
        for topic, stats in topic_stats.items():
            features[f"{topic}_accuracy"] = stats['correct'] / stats['total']
            features[f"{topic}_avg_time"] = np.mean(stats['time'])
            features[f"{topic}_time_std"] = np.std(stats['time'])
        
        return features

    def extract_temporal_features(self, history: List[Dict]) -> Dict[str, float]:
        """Extract features from historical performance."""
        scores = [quiz['total_score'] for quiz in history]
        times = [quiz['total_time'] for quiz in history]
        
        return {
            'avg_score': np.mean(scores),
            'score_trend': np.polyfit(range(len(scores)), scores, 1)[0],
            'score_std': np.std(scores),
            'avg_time': np.mean(times),
            'time_trend': np.polyfit(range(len(times)), times, 1)[0],
            'time_efficiency': np.mean([s/t for s, t in zip(scores, times)])
        }

    def prepare_features(self, current_quiz: Dict, history: List[Dict]) -> np.array:
        """Combine all features and prepare for model input."""
        features = {}
        
        # Current quiz features
        topic_features = self.extract_topic_features(current_quiz['responses'])
        features.update(topic_features)
        
        # Historical features
        temporal_features = self.extract_temporal_features(history)
        features.update(temporal_features)
        
        # Additional derived features
        features['consistency'] = 1 - features['score_std'] / features['avg_score']
        features['improvement_rate'] = features['score_trend'] / features['avg_score']
        
        return self.scaler.transform(pd.DataFrame([features]))

class RankPredictor:
    def __init__(self):
        self.feature_engineering = FeatureEngineering()
        self.models = {
            'rf': RandomForestRegressor(n_estimators=100, random_state=42),
            'gb': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }
        self.best_model = None
        self.feature_importance = None
        
    def train(self, X_train: np.array, y_train: np.array):
        """Train multiple models and select the best one."""
        best_score = float('inf')
        
        for name, model in self.models.items():
            # Define parameter grid for each model
            param_grid = {
                'rf': {
                    'n_estimators': [100, 200],
                    'max_depth': [10, 20, None],
                    'min_samples_split': [2, 5]
                },
                'gb': {
                    'n_estimators': [100, 200],
                    'learning_rate': [0.01, 0.1],
                    'max_depth': [3, 5]
                }
            }
            
            # Perform grid search
            grid_search = GridSearchCV(
                model,
                param_grid[name],
                cv=5,
                scoring='neg_mean_absolute_error'
            )
            grid_search.fit(X_train, y_train)
            
            # Update best model if current one is better
            if -grid_search.best_score_ < best_score:
                best_score = -grid_search.best_score_
                self.best_model = grid_search.best_estimator_
        
        # Calculate feature importance
        if hasattr(self.best_model, 'feature_importances_'):
            self.feature_importance = dict(zip(
                X_train.columns,
                self.best_model.feature_importances_
            ))
    
    def predict(self, current_quiz: Dict, history: List[Dict]) -> Dict:
        """Make prediction with confidence estimation."""
        features = self.feature_engineering.prepare_features(current_quiz, history)
        
        # Make prediction
        predicted_rank = self.best_model.predict(features)[0]
        
        # Estimate confidence based on feature similarity
        confidence = self._estimate_confidence(features)
        
        return {
            'predicted_rank': int(predicted_rank),
            'confidence_score': confidence,
            'feature_importance': self.feature_importance,
            'improvement_areas': self._get_improvement_areas(features)
        }
    
    def _estimate_confidence(self, features: np.array) -> float:
        """Estimate prediction confidence based on feature similarity to training data."""
        # This would use more sophisticated methods in production
        return np.clip(0.9 - np.std(features) * 0.1, 0.5, 0.95)
    
    def _get_improvement_areas(self, features: np.array) -> List[Dict]:
        """Identify areas where improvement would most impact rank."""
        if not self.feature_importance:
            return []
            
        improvements = []
        for feature, importance in self.feature_importance.items():
            if 'accuracy' in feature and importance > 0.05:
                improvements.append({
                    'topic': feature.split('_')[0],
                    'importance': importance,
                    'current_value': features[0][list(self.feature_importance.keys()).index(feature)]
                })
        
        return sorted(improvements, key=lambda x: x['importance'], reverse=True)
