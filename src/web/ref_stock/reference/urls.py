from django.urls import path

from . import views

app_name = "reference"

urlpatterns = [
    path("", views.index, name="index"),
]
