from django.urls import path
from .views import suggest_colors

urlpatterns = [
    path('suggest-colors/', suggest_colors),  
]
