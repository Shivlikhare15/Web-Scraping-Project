from django.urls import path
from .views import * 

urlpatterns = [
    path('',scrape_and_save,name="scrape_and_save"),
]
