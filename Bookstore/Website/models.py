from django.db import models
import datetime
from django_mysql.models import ListCharField

class Book(models.Model):
    bookname = models.CharField(max_length=30)
    author = models.CharField(max_length=50)
    price = models.IntegerField()

class User(models.Model):
    userName = models.CharField(max_length=30)
    userPassword = models.CharField(max_length=150)
    userRole = models.IntegerField()

class Orders(models.Model):
    userName = models.CharField(max_length=30)
    date = models.DateTimeField()
    totalSum = models.IntegerField()
    booksList = models.TextField()
