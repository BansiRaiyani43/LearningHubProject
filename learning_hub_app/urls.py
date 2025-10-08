from django.contrib import admin
from django.urls import path
from .views import BASE,sign_up, sign_in, user_login, user_logout, student_dashboard, teacher_dashboard, admin_dashboard,register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('index/',BASE,name='index'),
    path('signup/',register,name='signup'),
    # path('signin/',sign_in,name='signin'),
    path("login/", user_login, name="login"),
    path("logout/",user_logout, name="logout"),
    path("student/dashboard/", student_dashboard, name="student_dashboard"),
    path("teacher/dashboard/", teacher_dashboard, name="teacher_dashboard"),
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)