from django.contrib import admin
from django.urls import path
from .views import BASE,sign_up, sign_in
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('index/',BASE,name='index'),
    path('signup/',sign_up,name='signup'),
    path('signin/',sign_in,name='signin')



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
