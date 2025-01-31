# NEET-rank-predictor-using-testline-quiz
Student Rank Predictor using testline quiz
This project predicts NEET ranks based on students' performance in Testline quizzes. It utilizes historical quiz data and a trained machine learning model to estimate ranks and suggest possible college admissions.

## Features

* Fetches quiz data from APIs

* Preprocesses data to extract key performance metrics

* Trains a RandomForestRegressor model using past NEET ranks

* Provides an API to predict a student's NEET rank

* Predicts potential college admission based on rank

## Tech Stack

* Python (FastAPI, Pandas, Scikit-learn, NumPy, Requests, Redis)

* Machine Learning (RandomForestRegressor)

* API Deployment (FastAPI)

* Data Storage (Redis for caching,json files which was given)
