from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    image = models.ImageField(upload_to='profile_images', blank=True, null=True)

class Channel(models.Model):
    name = models.CharField(max_length=255)
    subscribers = models.IntegerField(default=0)
    owner_id = models.IntegerField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Video(models.Model):
    title = models.CharField(max_length=255)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    embed_url = models.URLField()
    thumbnail = models.TextField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    popularity = models.IntegerField(default=0)

class Video_Likes(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    like = models.BooleanField()

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    author_id = models.IntegerField()
    content = models.TextField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

class Comment_Likes(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    like = models.BooleanField()

class History(models.Model):
    user_id = models.IntegerField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)