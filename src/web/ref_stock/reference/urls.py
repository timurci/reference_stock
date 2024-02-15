from django.urls import path

from . import views

app_name = "reference"

urlpatterns = [
    path("", views.index, name="index"),
    path("new-entry/", views.NewEntry.as_view(), name="new-entry"),
    path("search/", views.Search.as_view(), name="search"),
]
