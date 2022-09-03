from datetime import datetime
from queue import Empty
from statistics import mode
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MyApp(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    age = models.IntegerField(default=18,null=True,blank=True)
    qualification = models.CharField(max_length=255,default='abc')
    city = models.CharField(max_length=255,blank=True,null=True)
    college = models.CharField(max_length=255,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # def __str__(self):
    #     return self.firstname
    # The __str__ method just tells Django what to print when it needs to print out an instance of the any model.
