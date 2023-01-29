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
    path('registration_redirect/', views.StudentProfileRedirectView.as_view(), name='registration_redirect'),
    path('registration_redirect_course/<slug:course_slug>', views.StudentProfileRedirectView.as_view(), name='registration_redirect_course'),
    path('registration_form/<slug:course_slug>', views.StudentProfileCreateView.as_view(), name='registration_form'),
    path('update_reg_form/<int:pk>', views.StudentProfileUpdateView.as_view(), name='update_reg_form')
]

