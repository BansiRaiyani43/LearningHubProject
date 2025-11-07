from django.urls import path
from .views import BASE,BASET,BASES, sign_up, sign_in, user_login, user_logout, student_dashboard, teacher_dashboard, admin_dashboard,register,courses_list,add_course,course_detail,delete_course, edit_course
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('index/',BASE,name='index'),
    path('indext/',BASET,name='indext'),
    path('indexs/',BASES,name='indexs'),
    path('signup/',register,name='signup'),
    # path('signin/',sign_in,name='signin'),
    path("login/", user_login, name="login"),
    path("logout/",user_logout, name="logout"),
    path("dashboard/student/", student_dashboard, name="student_dashboard"),
    path("dashboard/teacher/", teacher_dashboard, name="teacher_dashboard"),
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),
    path('',register,name='register'),
    path("course/", courses_list, name='courses_list'),
    path("add_course/", add_course, name='add_course'),
    path("course_detail/<int:id>/", course_detail, name='course_detail'),
    path("delete_course/<int:id>/", delete_course, name='delete_course'),
    path("edit_course/<int:id>/",  edit_course, name='edit_course')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)