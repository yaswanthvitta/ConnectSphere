from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import uuid

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
    
class Postpic(models.Model):
    title = models.CharField(max_length=200)
    caption=models.TextField()
    image = models.ImageField(upload_to='post_images')
    date_posted=models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

    # def __str__(self):
    #     return self.title

    # def get_absolute_url(self):
    #     return reverse('post-detail',kwargs={'pk':self.pk})