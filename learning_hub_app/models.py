from django.db import models

class User(models.Model):
        firstname=models.CharField(max_length=100,default="")
        lastname=models.CharField(max_length=100,default="")
        email=models.EmailField(max_length=100,default="")
        phone=models.BigIntegerField(default=0)
        password=models.CharField(max_length=10)

