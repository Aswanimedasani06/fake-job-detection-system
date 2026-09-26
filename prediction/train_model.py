import pandas as pd
import joblib
import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# 1. Load dataset
file_path = r"A:\FakeJobDetection\fake_job_project\prediction\dataset\fake_job_postings.csv"

df = pd.read_csv(file_path)


# 2. Select useful text columns
text_columns = [
    "title",
    "company_profile",
    "description",
    "requirements",
    "benefits"
]


# 3. Replace missing values
for column in text_columns:
    df[column] = df[column].fillna("")


# 4. Combine all text
df["text"] = df[text_columns].agg(" ".join, axis=1)


# 5. Input and output
X = df["text"]
y = df["fraudulent"]


# 6. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# 7. Create ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        stop_words="english",
        max_features=50000
    )),
    ("classifier", LogisticRegression(
        max_iter=1000
    ))
])


# 8. Train model
print("Training model...")

model.fit(X_train, y_train)


# 9. Test model
# 9. Test model

y_pred = model.predict(X_test)


# 10. Calculate evaluation metrics

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

cm = confusion_matrix(y_test, y_pred)
metrics = {
    "accuracy": round(accuracy * 100, 2),
    "precision": round(precision * 100, 2),
    "recall": round(recall * 100, 2),
    "f1_score": round(f1 * 100, 2),
    "confusion_matrix": cm.tolist()
}

with open("prediction/metrics.json", "w") as file:
    json.dump(metrics, file, indent=4)


# 11. Display evaluation results

print("\nModel Evaluation")
print("-------------------------")

print("Accuracy :", round(accuracy * 100, 2), "%")
print("Precision:", round(precision * 100, 2), "%")
print("Recall   :", round(recall * 100, 2), "%")
print("F1 Score :", round(f1 * 100, 2), "%")

print("\nConfusion Matrix:")
print(cm)


# 10. Test with a sample job
sample_job = """
We are looking for a Python Developer.
The candidate should have knowledge of Python,
Django, SQL and machine learning.
"""

prediction = model.predict([sample_job])[0]

if prediction == 1:
    print("Prediction: FAKE JOB")
else:
    print("Prediction: GENUINE JOB")
    joblib.dump(model, "prediction/fake_job_model.pkl")
print("Model saved successfully!")