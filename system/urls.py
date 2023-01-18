from django.urls import path
from authentication.forms import LoginForm
from system import views
from django.contrib.auth import views as auth_views
from system import views

app_name = 'system'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('video_tutorials/', views.video_tutorials, name='video_tutorials'),
    path('quizzes/', views.quizzes, name='quizzes'),
    path("reviewcenters/<slug:slug>", views.reviewcenter_detail, name="reviewcenter_detail"),
]