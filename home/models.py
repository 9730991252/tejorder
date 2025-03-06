from django.db import models

# Create your models here.
class Visitors(models.Model):
    count = models.IntegerField(default=300)