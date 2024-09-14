"""
polls/urls.py

This module defines the URL patterns for the polls application.
It maps URL paths to views for handling different poll-related requests.

URL patterns:
- Index page: List of latest polls.
- Detail page: Details for a specific poll question.
- Results page: Results for a specific poll question.
- Vote page: Handling votes for a specific poll question.
"""

from django.urls import path
from . import views

app_name = 'polls'  # Namespace for this app's URLs

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # Route for the index page listing all polls
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),  # Route for showing details of a specific poll
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),  # Route for displaying results of a specific poll
    path('<int:question_id>/vote/', views.VoteView.as_view(), name='vote'),  # Route for submitting a vote on a specific poll
]
