from datetime import datetime
from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model
import uuid

# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to = 'profile_images',default = 'blank-profile-picture.jpg')
    location = models.CharField(max_length=100 , blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.CharField(blank=False ,max_length=100)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='post_image')
    created_at = models.DateField(default=datetime.now)
    num_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user



class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class FollowUser(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user