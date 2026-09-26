from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

from prediction.models import PredictionHistory
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.contrib.auth.decorators import login_required
import os
import json
import joblib
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "prediction",
    "fake_job_model.pkl"
)

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

def home(request):
    return render(request, "dashboard/home.html")


# --------------------------------------------------
# REGISTER
# --------------------------------------------------

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            messages.error(request, "Passwords do not match.")
            return render(request, "dashboard/register.html")

        if User.objects.filter(username=username).exists():

            messages.error(request, "Username already exists.")
            return render(request, "dashboard/register.html")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Registration successful. Please login."
        )

        return redirect("login")

    return render(request, "dashboard/register.html")


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "dashboard/login.html")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------
@login_required(login_url="login")
def dashboard(request):

    total_predictions = PredictionHistory.objects.count()

    fake_predictions = PredictionHistory.objects.filter(
        result="FAKE JOB POSTING"
    ).count()

    genuine_predictions = PredictionHistory.objects.filter(
        result="GENUINE JOB POSTING"
    ).count()

    if total_predictions > 0:

        genuine_percentage = round(
            (genuine_predictions / total_predictions) * 100,
            1
        )

        fake_percentage = round(
            (fake_predictions / total_predictions) * 100,
            1
        )

    else:

        genuine_percentage = 0
        fake_percentage = 0
        # Analytics data for dashboard chart
    chart_data = {
        "genuine": genuine_predictions,
        "fake": fake_predictions,
    }

    # Latest 5 predictions
    recent_predictions = PredictionHistory.objects.order_by(
        "-created_at"
    )[:5]
    # Prediction trend data
    trend_data = (
        PredictionHistory.objects
        .annotate(date=TruncDate("created_at"))
        .values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )

    trend_labels = [
        item["date"].strftime("%d %b")
        for item in trend_data
    ]

    trend_values = [
        item["count"]
        for item in trend_data
    ]

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "total_predictions": total_predictions,
            "fake_predictions": fake_predictions,
            "genuine_predictions": genuine_predictions,
            "genuine_percentage": genuine_percentage,
            "fake_percentage": fake_percentage,
            "recent_predictions": recent_predictions,
            "chart_data": chart_data,
            "trend_labels": trend_labels,
    "trend_values": trend_values,
        }
    )
@login_required(login_url="login")
def predict(request):

    result = None
    confidence = None

    if request.method == "POST":

        # Get data from the form
        job_title = request.POST.get("title", "")
        company_profile = request.POST.get("company", "")
        location = request.POST.get("location", "")
        job_description = request.POST.get("description", "")
        requirements = request.POST.get("requirements", "")
        benefits = request.POST.get("salary", "")

        # Combine all job posting information
        job_text = " ".join([
            job_title,
            company_profile,
            location,
            job_description,
            requirements,
            benefits
        ])

        # Predict
        prediction = model.predict([job_text])[0]

        # Calculate confidence
        try:
            probabilities = model.predict_proba([job_text])[0]
            confidence = round(max(probabilities) * 100, 2)
        except AttributeError:
            confidence = None

        # Convert prediction to readable result
        if prediction == 1 or str(prediction).lower() in ["fake", "1"]:
            result = "FAKE JOB POSTING"
        else:
            result = "GENUINE JOB POSTING"

        # Save prediction to database
        PredictionHistory.objects.create(
            job_title=job_title,
            company_profile=company_profile,
            job_description=job_description,
            requirements=requirements,
            benefits=benefits,
            result=result,
            confidence=confidence or 0
        )

    return render(
        request,
        "dashboard/predict.html",
        {
            "prediction": result,
            "confidence": confidence
        }
    )
# --------------------------------------------------
# PREDICT JOB
# --------------------------------------------------


@login_required(login_url="login")
def history(request):

    from django.core.paginator import Paginator

    search_query = request.GET.get("search", "").strip()
    result_filter = request.GET.get("result", "").strip()

    prediction_history = PredictionHistory.objects.all().order_by(
        "-created_at"
    )

    # Search by job title
    if search_query:
        prediction_history = prediction_history.filter(
            job_title__icontains=search_query
        )

    # Filter by result
    if result_filter in [
        "FAKE JOB POSTING",
        "GENUINE JOB POSTING"
    ]:
        prediction_history = prediction_history.filter(
            result=result_filter
        )

    # Pagination: 5 predictions per page
    paginator = Paginator(prediction_history, 5)

    page_number = request.GET.get("page")

    prediction_history = paginator.get_page(page_number)

    return render(
        request,
        "dashboard/history.html",
        {
            "prediction_history": prediction_history,
            "search_query": search_query,
            "result_filter": result_filter,
        }
    )
@login_required(login_url="login")
def delete_prediction(request, prediction_id):
    prediction = PredictionHistory.objects.get(id=prediction_id)
    prediction.delete()
    return redirect("history")
@login_required(login_url="login")
def prediction_detail(request, prediction_id):

    prediction = PredictionHistory.objects.get(
        id=prediction_id
    )

    return render(
        request,
        "dashboard/prediction_detail.html",
        {
            "prediction": prediction
        }
    )
def logout_view(request):
    logout(request)
    return redirect("login")
def predict_job(request):
    if request.method == "POST":

        title = request.POST.get("title", "")
        company_profile = request.POST.get("company_profile", "")
        description = request.POST.get("description", "")
        requirements = request.POST.get("requirements", "")
        benefits = request.POST.get("benefits", "")

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
                result = "REAL JOB POSTING"

            return render(request, "dashboard/dashboard.html", {
                "result": result
            })

    return render(request, "dashboard/dashboard.html")
def analytics(request):
    predictions = PredictionHistory.objects.all()

    total = predictions.count()
    fake_count = predictions.filter(
        result__icontains="fake"
    ).count()

    genuine_count = predictions.filter(
        result__icontains="genuine"
    ).count()

    fake_percentage = 0

    if total > 0:
        fake_percentage = round(
            (fake_count / total) * 100,
            2
        )

    # Read ML evaluation metrics
    metrics_path = os.path.join(
        "prediction",
        "metrics.json"
    )

    metrics = {
        "accuracy": 0,
        "precision": 0,
        "recall": 0,
        "f1_score": 0
    }

    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as file:
            metrics = json.load(file)

    return render(
        request,
        "dashboard/analytics.html",
        {
            "total": total,
            "fake_count": fake_count,
            "genuine_count": genuine_count,
            "fake_percentage": fake_percentage,

            "accuracy": metrics["accuracy"],
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "f1_score": metrics["f1_score"],
        }
    )




