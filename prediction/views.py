from django.shortcuts import render
import joblib
import os

from .models import PredictionHistory


# Load trained model
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "fake_job_model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_job(request):
    result = None

    if request.method == "POST":

        title = request.POST.get("title", "")
        company_profile = request.POST.get("company_profile", "")
        description = request.POST.get("description", "")
        requirements = request.POST.get("requirements", "")
        benefits = request.POST.get("benefits", "")

        # Combine all job information
        job_text = " ".join([
            title,
            company_profile,
            description,
            requirements,
            benefits
        ])

        if job_text.strip():

            prediction = model.predict([job_text])[0]

            if prediction == 1:
                result = "FAKE JOB POSTING"
            else:
                result = "GENUINE JOB POSTING"

            # Save prediction to database
            PredictionHistory.objects.create(
                job_title=title,
                result=result
            )

    return render(
        request,
        "prediction/predict.html",
        {"result": result}
    )
def prediction_history(request):
    history = PredictionHistory.objects.all().order_by("-created_at")

    return render(
        request,
        "prediction/history.html",
        {"history": history}
    )

