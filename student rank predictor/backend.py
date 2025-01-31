from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

app = FastAPI()

# Data models
class QuizResponse(BaseModel):
    question_id: int
    selected_option_id: int
    correct_option_id: int
    topic: str
    difficulty: str
    time_taken: int

class QuizSubmission(BaseModel):
    user_id: int
    quiz_id: int
    total_score: float
    responses: List[QuizResponse]

class HistoricalQuiz(BaseModel):
    quiz_id: int
    score: float
    response_map: Dict[str, int]

class UserHistory(BaseModel):
    user_id: int
    last_5_quizzes: List[HistoricalQuiz]

# Helper functions
def calculate_topic_performance(responses: List[QuizResponse]) -> Dict[str, float]:
    topic_correct = {}
    topic_total = {}
    
    for response in responses:
        topic = response.topic
        is_correct = response.selected_option_id == response.correct_option_id
        
        topic_total[topic] = topic_total.get(topic, 0) + 1
        topic_correct[topic] = topic_correct.get(topic, 0) + (1 if is_correct else 0)
    
    return {topic: (correct / topic_total[topic]) * 100 
            for topic, correct in topic_correct.items()}

def analyze_improvement_trends(history: List[HistoricalQuiz]) -> Dict:
    scores = [quiz.score for quiz in history]
    improvement = np.polyfit(range(len(scores)), scores, 1)[0]
    
    return {
        "trend": "improving" if improvement > 0 else "declining",
        "rate": abs(improvement),
        "recent_scores": scores
    }

class RankPredictor:
    def __init__(self):
        # In production, these would be loaded from saved models
        self.model = RandomForestRegressor()
        self.scaler = StandardScaler()
        
    def prepare_features(self, current_quiz: QuizSubmission, history: UserHistory) -> np.array:
        # Extract relevant features
        recent_scores = [quiz.score for quiz in history.last_5_quizzes]
        topic_performance = calculate_topic_performance(current_quiz.responses)
        
        features = [
            current_quiz.total_score,
            np.mean(recent_scores),
            np.std(recent_scores),
            *topic_performance.values()
        ]
        
        return self.scaler.transform([features])
    
    def predict_rank(self, features: np.array) -> Dict:
        predicted_rank = self.model.predict(features)[0]
        confidence = self.model.predict_proba(features)[0] if hasattr(self.model, 'predict_proba') else None
        
        return {
            "predicted_rank": int(predicted_rank),
            "confidence": float(confidence) if confidence is not None else None
        }

# Initialize predictor
rank_predictor = RankPredictor()

@app.post("/analyze/performance")
async def analyze_performance(quiz: QuizSubmission, history: UserHistory):
    try:
        # Calculate topic-wise performance
        topic_performance = calculate_topic_performance(quiz.responses)
        
        # Analyze improvement trends
        improvement_trends = analyze_improvement_trends(history.last_5_quizzes)
        
        # Calculate weak areas (topics with < 60% accuracy)
        weak_areas = [topic for topic, score in topic_performance.items() if score < 60]
        
        return {
            "topic_performance": topic_performance,
            "improvement_trends": improvement_trends,
            "weak_areas": weak_areas
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/rank")
async def predict_rank(quiz: QuizSubmission, history: UserHistory):
    try:
        features = rank_predictor.prepare_features(quiz, history)
        prediction = rank_predictor.predict_rank(features)
        
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Bonus: College prediction endpoint
@app.post("/predict/college")
async def predict_college(predicted_rank: int):
    # This would use a database of college cutoffs from previous years
    # Simplified example:
    college_cutoffs = {
        "AIIMS Delhi": 50,
        "JIPMER": 500,
        "Maulana Azad": 1000,
        "Government Medical College": 2000
    }
    
    eligible_colleges = [
        college for college, cutoff in college_cutoffs.items()
        if predicted_rank <= cutoff
    ]
    
    return {
        "eligible_colleges": eligible_colleges
    }
