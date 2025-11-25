from django.contrib import admin
from .models import User,Course,Subject,Chapter,Assignment

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Assignment)