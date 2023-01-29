from django.urls import path, re_path
from authentication.forms import LoginForm
from system import views
from django.contrib.auth import views as auth_views
from system import views

app_name = 'system'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("reviewcenters/", views.reviewcenter_list, name="reviewcenter_list"),
    path("reviewcenters/<slug:slug>", views.reviewcenter_detail, name="reviewcenter_detail"),
    path("course_videos/", views.VideoListView.as_view(), name='course_videos'),
    path('video_watch/<slug:course_slug>/<slug:video_slug>', views.VideoDetailView.as_view(), name='video_watch'),
    path('video_tutorials/', views.free_video_tutorials, name='free_video_tutorials'),
    path('review_materials/', views.ReviewMaterialListView.as_view(), name='review_materials'),
    path('review_courses/', views.ReviewCourseListView.as_view(), name='review_courses'),
    path('check_course_payment/<slug:course_slug>', views.check_course_payment, name='check_course_payment'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('process_payment/<slug:course_slug>', views.process_payment, name='process_payment'),
    path('payment_done/<slug:course_slug>', views.payment_done, name='payment_done'),
    path('payment_cancelled/', views.payment_canceled, name='payment_cancelled')
    
]