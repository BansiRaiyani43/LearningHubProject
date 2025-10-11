from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=USER_ROLES, default='student')
    email = models.EmailField(_('email address'), unique=True)  # unique email
    phone_no = models.BigIntegerField(null=True, blank=True)   # optional phone number

    def __str__(self):
        return f"{self.username} ({self.role})"

class course(models.Model):
    title:models.CharField(max_length=200)
    description:models.TextField()
    instructor:models.CharField(max_length=50)

    def __str__(self):
        return self.title





# from django.db import models

# class User(models.Model):
#         firstname=models.CharField(max_length=100,default="")
#         lastname=models.CharField(max_length=100,default="")
#         email=models.EmailField(max_length=100,default="")
#         # phone=models.BigIntegerField(default=0)
#         password=models.CharField(max_length=10)

