from django.urls import path, re_path
from authentication.forms import LoginForm
from system import views
from django.contrib.auth import views as auth_views
from system import views

app_name = 'system'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("reviewcenters/<slug:slug>", views.reviewcenter_detail, name="reviewcenter_detail"),
    path("course_videos/<int:pk>", views.VideoListView.as_view(), name='course_videos'),
    path('video_watch/<int:pk>', views.VideoDetailView.as_view(), name='video_watch'),
    path('video_tutorials/', views.free_video_tutorials, name='free_video_tutorials'),
    path('check_course_payment/<int:pk>', views.check_course_payment, name='check_course_payment'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('process-payment/<int:pk>', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled')
    
]