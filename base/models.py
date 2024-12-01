from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True,null=True)
    bio=models.TextField(null=True)

    avatar=models.ImageField(upload_to="images/", null=True,blank=True,default='avatar.svg')

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username']  # Required when creating a superuser

    # def __str__(self):
    #     return f"{self.username}"

class Topic(models.Model):
    name=models.CharField(max_length=200,null=True,unique=True)

    def __str__(self):
        return f"{self.name}"

class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic =models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=220)
    description = models.TextField(null=True, blank=True)
    participants=models.ManyToManyField(User,related_name='participants', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering =['-updated_at','-created_at']

    def __str__(self):
        return f"{self.name}"
    


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at','-created_at']

    def __str__(self):
        return f"{self.message[:40]}"