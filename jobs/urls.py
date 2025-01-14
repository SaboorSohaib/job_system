from django.urls import path
from .views import JobListCreateView, JobDetailView, JobResultListView, JobResultDetailView

urlpatterns = [
    # Job Endpoints
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),

    # JobResult Endpoints
    path('job-results/<int:pk>/', JobResultDetailView.as_view(), name='job-result-detail'),
]
