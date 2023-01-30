from django.urls import path, re_path
from authentication.forms import LoginForm
from system import views
from django.contrib.auth import views as auth_views
from job import views

app_name = 'job'

urlpatterns = [
    path('job_list/', views.JobListView.as_view(), name='job_list'),
    path('jobpost_detail/<slug:slug>/', views.JobDetailView.as_view(), name='jobpost_detail'),
    path('submit_job_application/<slug:slug>/', views.submit_job_application, name='submit_job_application'),
]