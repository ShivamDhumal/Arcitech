from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password2 = models.CharField(max_length=8)
    phone = models.CharField(  max_length=12,blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city =  models.CharField(max_length=20,blank=True, null=True)
    state = models.CharField(max_length=20 , blank=True, null=True)
    country = models.CharField(max_length=20 , blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)



    def __str__(self):
        return self.email

class category(models.Model):
    name =models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class content_item(models.Model):
    title = models.CharField(max_length=30,blank=False, null=False)
    body = models.TextField(blank=False, null=False)
    summary = models.CharField(max_length=60 , blank=False, null=False)
    document = models.FileField(upload_to='file' , blank=False, null=False)
    category = models.ManyToManyField(category)
    user = models.CharField(max_length=30)


    def __str__(self) -> str:
        return self.title
    