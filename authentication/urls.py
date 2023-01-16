from django.urls import path
from authentication.forms import LoginForm
from system import views
from django.contrib.auth import views as auth_views
from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('accounts/login/',
        views.CustomLoginView.as_view(template_name = 'index.html',
                                        authentication_form=LoginForm, 
                                        redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/verify/<str:id>/', views.verify_account_view, name='create'),
    path('accounts/verification/', views.verification, name='verification'),
    path('accounts/send_verification/', views.send_verification, name='send_verification'),
]

