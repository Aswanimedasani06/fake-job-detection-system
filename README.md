Fake Job Posting Detection System Using NLP and Cloud Deployment

## Project Overview

The Fake Job Posting Detection System is a web-based application that uses Natural Language Processing (NLP) and Machine Learning to identify potentially fraudulent job postings.

The system allows users to enter job-posting information and receive a prediction indicating whether the posting is Genuine or Potentially Fake. The application also stores prediction history and provides analytics to understand previous predictions.

## Objectives

- Detect potentially fraudulent job postings using Machine Learning.
- Process job-posting text using NLP techniques.
- Provide a simple web interface for users.
- Store and display previous prediction results.
- Provide prediction analytics and model performance information.
- Deploy the application using cloud technologies.

## Technologies Used

- Python
- Django
- Machine Learning
- Natural Language Processing (NLP)
- HTML
- CSS
- JavaScript
- SQLite
- Joblib
- Git & GitHub

## Main Features

- User Registration and Login
- Job Posting Prediction
- Fake/Genuine Job Classification
- Confidence Score
- Prediction History
- Search Prediction History
- Prediction Details
- Prediction Analytics
- Machine Learning Model Performance
- Logout functionality

## System Workflow

1. User registers or logs into the application.
2. User enters the details of a job posting.
3. The system processes the entered job information.
4. NLP techniques are used to process the text.
5. The trained Machine Learning model analyzes the job posting.
6. The system predicts whether the job is Genuine or Potentially Fake.
7. The prediction result and confidence score are displayed.
8. The prediction is stored in the database.
9. Users can view their prediction history and analytics.

## Project Structure

fake-job-detection-system/
│
├── dashboard/
├── prediction/
├── fake_job_project/
├── manage.py
├── requirements.txt
├── Procfile
├── db.sqlite3
└── README.md

## Prediction Analytics

The application provides analytics such as:

- Total Predictions
- Fake Jobs
- Genuine Jobs
- Fake Percentage
- Accuracy
- Precision
- Recall
- F1 Score
- Fake vs Genuine Job comparison

## How to Run the Project

1. Clone the repository

git clone https://github.com/Aswanimedasani06/fake-job-detection-system.git

2. Open the project

cd fake-job-detection-system

3. Install dependencies

pip install -r requirements.txt

4. Run database migrations

python manage.py migrate

5. Start the Django server

python manage.py runserver

6. Open the application

Open the local server address shown by Django in your browser.

## Machine Learning

The system uses a trained Machine Learning model to classify job postings. The model processes information from job postings and generates a classification result along with a confidence score.

Model-related files are maintained inside the "prediction" application.

## User Authentication

The application provides authentication features including:

- Registration
- Login
- Logout
- User-specific prediction activity

## Project

Project Title: Fake Job Posting Detection System Using NLP and Cloud Deployment

Developer: Medasani Aswani

Degree: B.Tech – Computer Science / Information Technology

## Future Scope

- Improve the model using larger and more diverse datasets.
- Experiment with advanced NLP and Deep Learning techniques.
- Add an API for external applications.
- Improve cloud deployment and scalability.
- Add additional fraud-detection features.
- Improve the user interface and reporting.

📄 License

This project is developed for academic purposes.
