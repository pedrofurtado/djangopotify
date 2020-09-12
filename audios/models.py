from django.db import models

class Audio(models.Model):
    name = models.CharField(max_length=255)
