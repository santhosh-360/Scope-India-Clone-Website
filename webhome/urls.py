from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('courses/',views.courses,name='courses'),
    path('contact/',views.contact,name='contact'),
    path('register/',views.registartion,name='registartion'),
    path('verify/<uuid:token>/',views.verify_email,name='verify_email'),
    path('login/',views.user_login,name='login'),
    path('create-new-password/',views.create_new_password,name='create_new_password'),
    path('student-dashboard/',views.student_dashboard,name='student_dashboard'),
    path('signup-course/<int:course_id>/',views.signup_course,name='signup_course'),
    path('remove-course/<int:course_id>/',views.remove_course,name='remove_course'),
    path('generate-password/',views.generate_password,name='generate_password'),
    path('forgot-password/',views.forgot_password,name='forgot_password'),
    path('logout/',views.logout_view,name='logout'),
    path('profile-edit/',views.profile_edit,name='profile_edit'),
    path('change-password/',views.change_password,name='change_password'),
    
    
]   