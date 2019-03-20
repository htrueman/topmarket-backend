from django.db import models

# Create your models here.


class KnowledgeBase(models.Model):

    question = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)

