from django.urls import path
from .views import BASE,BASES, sign_up, sign_in, user_login, user_logout, student_dashboard, teacher_dashboard, admin_dashboard,register,courses_list,add_course,course_detail,delete_course, edit_course
from .views import subject_list,subject_add,subject_update,subject_delete,chapter_list,chapter_add,chapter_update,chapter_delete,chapter_detail,assignment_list,assignment_add,assignment_detail,assignment_update,assignment_delete
from .views import submission_list,submission_add,submission_view,submission_update,submission_grade,submission_delete
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('index/',BASE,name='index'),
    path('indexs/',BASES,name='indexs'),
    path("login/", user_login, name="login"),
    path("logout/",user_logout, name="logout"),
    path("dashboard/student/", student_dashboard, name="student_dashboard"),
    path("teacher/dashboard/", teacher_dashboard, name="teacher_dashboard"),
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),
    path('',register,name='signup'),
    path("course/", courses_list, name='courses_list'),
    path("add_course/", add_course, name='add_course'),
    path("course_detail/<int:id>/", course_detail, name='course_detail'),
    path("delete_course/<int:id>/", delete_course, name='delete_course'),
    path("edit_course/<int:id>/",  edit_course, name='edit_course'),
    path("subjects/",  subject_list, name='subject_list'),
    path("add_subject/",  subject_add, name='add_subject'),
    path("update_subject/<int:id>/",  subject_update, name='update_subject'),
    path("delete_subject/<int:id>/", subject_delete, name='delete_subject'),
    path("chapters/",  chapter_list, name='chapters'),
    path("add_chapter/", chapter_add, name='add_chapter'),
    path("update_chapter/<int:id>/",  chapter_update, name='update_chapter'),
    path("delete_chapter/<int:id>/", chapter_delete, name='delete_chapter'),
    path("chapter_detail/<int:id>/", chapter_detail, name='chapter_detail'),
    #----assignments-----------#
    path("assignments/",  assignment_list, name='assignment_list'),
    path("add_assignment/", assignment_add, name='add_assignment'),
    path("assignmet_detail/<int:id>/", assignment_detail, name='assignmet_detail'),
    path("update_assignment/<int:id>/",  assignment_update, name='update_assignment'),
    path("delete_assignment/<int:id>/", assignment_delete, name='delete_assignment'),
    #-------submission---------#
    path("submissions/",  submission_list, name='submissions'),
    path("submission_add/<int:assignment_id>/", submission_add, name='submission_add'),
    path("submission_view/<int:id>/", submission_view, name='submission_view'),
    path("submission_update/<int:id>/", submission_update, name='submission_update'),
    path("submission_grade/<int:id>/", submission_grade, name='submission_grade'),
    path("submission_delete/<int:id>/", submission_delete, name='submission_delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)