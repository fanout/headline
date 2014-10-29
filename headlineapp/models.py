from django.db import models

class Headline(models.Model):
    type = models.CharField(max_length=64)
    title = models.CharField(max_length=200)
    text = models.TextField()
