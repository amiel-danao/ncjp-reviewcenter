from django.urls import path
from authentication.forms import LoginForm
from system import views
from django.contrib.auth import views as auth_views
from system import views

app_name = 'system'

urlpatterns = [
    path('', views.index, name='index'),
]