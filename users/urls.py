from django.urls import path
from . import views

urlpatterns = [
    path('mainLogin', views.mainLogin, name='mainLogin'),
    path('mainDashboard', views.dashboard, name='mainDashboard'),
    path('approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('disapprove-user/<int:user_id>/', views.disapprove_user, name='disapprove_user'),
    path('<int:user_id>/deleteuser/', views.deleteUser, name='deleteuser'),
    
    path('approve-instructor/<int:instructor_id>/', views.approve_instructor, name='approve_instructor'),
    path('disapprove-instructor/<int:instructor_id>/', views.disapprove_instructor, name='disapprove_instructor'),
    
    path('homepage', views.homepage, name='homepage'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('student_classroom', views.student_classroom, name='student_classroom'),
    path('<str:class_code>/student_room/', views.student_room, name='student_room'),
    
    path('remove_student/<int:classroom_id>/<int:student_id>/', views.remove_student, name='remove_student'),
    path('classlist', views.classlist, name='classlist'),
    path('teacher_dashboard', views.teacher_dashboard, name='teacher_dashboard'),
    path('<str:class_code>/classroom/', views.classroom, name='classroom'),
    path('<int:act_id>/pass_activity/', views.pass_activity, name='pass_activity'),
    
    path('<int:class_id>/deleteClassroom/', views.deleteClassroom, name='deleteClassroom'),
    path('<int:act_id>/deleteActivity/', views.deleteActivity, name='deleteActivity'),
    path('<int:lesson_id>/deleteLesson/', views.deleteLesson, name='deleteLesson'),
    
    path('forum', views.forum, name='forum'),
    path('student_forum', views.student_forum, name='student_forum'),
    
    path('about', views.about, name='about'),
]