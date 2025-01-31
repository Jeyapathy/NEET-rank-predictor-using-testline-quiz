# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    quizzes = relationship("QuizSubmission", back_populates="user")
    predictions = relationship("RankPrediction", back_populates="user")

class QuizSubmission(Base):
    __tablename__ = "quiz_submissions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_date = Column(DateTime, default=datetime.utcnow)
    total_score = Column(Float)
    total_time = Column(Integer)  # in seconds
    responses = relationship("QuizResponse", back_populates="submission")
    user = relationship("User", back_populates="quizzes")

class QuizResponse(Base):
    __tablename__ = "quiz_responses"
    
    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey("quiz_submissions.id"))
    question_id = Column(Integer)
    selected_option_id = Column(Integer)
    correct_option_id = Column(Integer)
    topic = Column(String)
    subtopic = Column(String)
    difficulty = Column(String)
    time_taken = Column(Integer)  # in seconds
    submission = relationship("QuizSubmission", back_populates="responses")

class RankPrediction(Base):
    __tablename__ = "rank_predictions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    predicted_rank = Column(Integer)
    confidence_score = Column(Float)
    prediction_date = Column(DateTime, default=datetime.utcnow)
    features_used = Column(JSON)  # Store feature values used for prediction
    user = relationship("User", back_populates="predictions")

class College(Base):
    __tablename__ = "colleges"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    cutoff_history = relationship("CollegeCutoff", back_populates="college")

class CollegeCutoff(Base):
    __tablename__ = "college_cutoffs"
    
    id = Column(Integer, primary_key=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    year = Column(Integer)
    general_cutoff = Column(Integer)
    sc_cutoff = Column(Integer)
    st_cutoff = Column(Integer)
    obc_cutoff = Column(Integer)
    college = relationship("College", back_populates="cutoff_history")

# schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class QuizResponseCreate(BaseModel):
    question_id: int
    selected_option_id: int
    correct_option_id: int
    topic: str
    subtopic: str
    difficulty: str
    time_taken: int

class QuizSubmissionCreate(BaseModel):
    total_score: float
    total_time: int
    responses: List[QuizResponseCreate]

class RankPredictionResponse(BaseModel):
    predicted_rank: int
    confidence_score: float
    prediction_date: datetime
    eligible_colleges: List[str]
