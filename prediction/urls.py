from django.urls import path
from . import views

urlpatterns = [
    path("", views.predict_job, name="predict_job"),
    path("history/", views.prediction_history, name="prediction_history"),
]