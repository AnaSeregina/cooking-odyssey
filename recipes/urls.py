# recipes/urls.py
from django.urls import path
from .views import home, recipe_detail, nutrition_table, about, contact_view

urlpatterns = [
    path("", home, name="home"),
    path("r/<slug:slug>/", recipe_detail, name="recipe_detail"),
    path("nutrition/", nutrition_table, name="nutrition"),
    path("about/", about, name="about"),
    path("contact/", contact_view, name="contact"),
]