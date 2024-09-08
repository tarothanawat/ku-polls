from django.urls import path
from . import views

app_name = 'polls'  # Namespacing for the app

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # Route for the index page
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),  # Route for question details
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),  # Route for question results
    path('<int:question_id>/vote/', views.VoteView.as_view(), name='vote'),  # Route for voting
]
