from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=USER_ROLES, default='student')
    phone_no = models.BigIntegerField(null=True, blank=True)   # optional phone number

    def __str__(self):
        return f"{self.username} ({self.role})"

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default="")
    instructor = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20,unique=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='subjects')
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
    
class Chapter(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=100)
    number = models.PositiveBigIntegerField(help_text="Chapter order number")
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta :
        ordering = ['number']

    def __str__(self):
        return f"chapter {self.number} : {self.title}"
    
class Assignment(models.Model):
    chapter = models.ForeignKey('Chapter',on_delete=models.CASCADE,related_name='assignments')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    due_date = models.DateField(null=True,blank=True)
    marks = models.PositiveBigIntegerField(default=0)
    file = models.FileField(upload_to='assignments/',blank=True,null=True)

    def __str__(self):
        return f"{self.title} (Chapter{self.chapter.number})"

class AssignmentSubmission(models.Model):

    STATUS_CHOICES = (
        ('on_time', 'On Time'),
        ('late', 'Late')
    )

    assignment = models.ForeignKey('Assignment',on_delete=models.CASCADE,related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='submissions')
    submitted_at = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='submissions/',blank=True,null=True)
    mark_awarded = models.PositiveBigIntegerField(blank=True,null=True)
    answer_text = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='on_time')
    graded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True,blank=True,related_name='graded_submission')
    graded_at = models.DateTimeField(null=True, blank=True)
    feedback = models.TextField(blank=True,null=True)

    class Meta:
        ordering = ['-submitted_at']
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.assignment.title} by {self.student.username}"

# from django.db import models

# class User(models.Model):
#         firstname=models.CharField(max_length=100,default="")
#         lastname=models.CharField(max_length=100,default="")
#         email=models.EmailField(max_length=100,default="")
#         # phone=models.BigIntegerField(default=0)
#         password=models.CharField(max_length=10)