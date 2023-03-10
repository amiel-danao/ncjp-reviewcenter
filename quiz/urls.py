from django.urls import re_path
from .views import QuizListView,\
    ViewQuizListByCourse, QuizUserProgressView, QuizMarkingList,\
    QuizMarkingDetail, QuizDetailView, QuizTake, index, login_user, logout_user
# from system.views import CourseListView
from django.urls import path

app_name = 'quiz'


urlpatterns = [         
    
                       re_path(r'^quizzes/$',
                           view=QuizListView.as_view(),
                           name='quiz_index'),

                    #    re_path(r'^category/$',
                    #        view=CourseListView.as_view(),
                    #        name='quiz_category_list_all'),

                       re_path(r'^category/(?P<category_name>[\w|\W-]+)/$',
                           view=ViewQuizListByCourse.as_view(),
                           name='quiz_category_list_matching'),

                       re_path(r'^progress/$',
                           view=QuizUserProgressView.as_view(),
                           name='quiz_progress'),

                       re_path(r'^marking/$',
                           view=QuizMarkingList.as_view(),
                           name='quiz_marking'),

                       re_path(r'^marking/(?P<pk>[\d.]+)/$',
                           view=QuizMarkingDetail.as_view(),
                           name='quiz_marking_detail'),

                       #  passes variable 'quiz_name' to quiz_take view
                       re_path(r'^(?P<slug>[\w-]+)/$',
                           view=QuizDetailView.as_view(),
                           name='quiz_start_page'),

                       re_path(r'^(?P<quiz_name>[\w-]+)/take/$',
                           view=QuizTake.as_view(),
                           name='quiz_question'),
]