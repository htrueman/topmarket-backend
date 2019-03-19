from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class News(models.Model):

    avatar = models.ImageField()
    name = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=True, editable=False, blank=True)
    text = models.TextField(blank=True, null=True)


class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
