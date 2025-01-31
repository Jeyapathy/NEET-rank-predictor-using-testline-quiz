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

## Screenshots
![Image](https://github.com/user-attachments/assets/0f302d8f-9b62-41a0-8878-54714ab2fbed)

This states a sample page of detecting the whole quiz data in which it predicts the student rank

![Image](https://github.com/user-attachments/assets/131b6209-d17b-48c0-9806-b6538e26b3d6)
![Image](https://github.com/user-attachments/assets/9d868faa-3443-43e5-a1d6-91692be8e348)
![Image](https://github.com/user-attachments/assets/05ad9773-21d8-42d8-a662-5957d7528974)

This a interactive page of detecting the student rank predicting the results using the quiz in which the particualr student has successfully completed
