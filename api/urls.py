from django.urls import path
from .views import suggest_colors,ping

urlpatterns = [
    path('suggest-colors/', suggest_colors), 
    path('ping/', ping),
   
]
