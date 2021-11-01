from django.db import models

# Create your models here.
class record(models.Model):
    idx = models.AutoField(null=False, primary_key=True)
    id = models.IntegerField(null=False)
    name = models.CharField(max_length=12)
    nickname = models.CharField(max_length=12, default="unknown")
    time = models.DateTimeField(null=False)
    url = models.CharField(max_length=150, null=False)
    video_url = models.CharField(max_length=150, null=False, default="")


