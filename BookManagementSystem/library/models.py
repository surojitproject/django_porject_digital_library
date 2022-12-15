from django.db import models
from django.contrib.auth.models import User
import os, datetime

# Create your models here.
def filepath(request, filename):
    old_filename = filename
    timenow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" %(timenow, old_filename)
    return os.path.join('uploads/', filename)

class Book(models.Model):
    types = [
        ('Edited', 'Edited'),
        ('Reference', 'Reference'),
        ('Fictious', 'Fictious'),
        ('Non-Fictious', 'Non-Fictious'),
    ]

    book_name = models.CharField(max_length=255, null=True)
    author = models.CharField(max_length=255, null=True)
    book_type = models.CharField(max_length=255, null=True, choices=types)
    price = models.FloatField(null=True)
    rating = models.FloatField(null=True)
    book_pic = models.ImageField(upload_to=filepath, null=True, blank=True)

    def __str__(self):
        return self.book_name

class UserTable(models.Model):
    STATUS = [
        ('Pending', 'Pending'),
        ('Over', 'Over'),
    ]

    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, null=True, choices=STATUS, default='Pending')
    def __str__(self):
        return self.customer.username

 
class UserProfile(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=filepath, null=True, blank=True, default='uploads/img_avatar.png')
    def __str__(self):
        return self.user.username