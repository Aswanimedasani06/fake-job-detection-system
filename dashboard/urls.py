from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path("register/", views.register, name="register"),

    path("login/", views.login_view, name="login"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("predict/", views.predict, name="predict"),

    path("history/",views.history, name="history"),
    path(
    "delete/<int:prediction_id>/",
    views.delete_prediction,
    name="delete_prediction"
),
path(
    "prediction/<int:prediction_id>/",
    views.prediction_detail,
    name="prediction_detail"
),
path("logout/", views.logout_view, name="logout"),
path("analytics/",views.analytics, name="analytics"),
]