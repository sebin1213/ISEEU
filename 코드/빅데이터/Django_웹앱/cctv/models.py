from django.db import models

class Road(models.Model):
    road_info = models.CharField(max_length=200)
    road_st_time = models.DateTimeField(null=False)
    road_end_time = models.DateTimeField(null=False)

class News(models.Model):
    News_title = models.CharField(max_length=200)
    News_content = models.CharField(max_length=200)
    News_href = models.CharField(max_length=200)
    News_writer = models.CharField(max_length=200)
    News_write_time = models.DateTimeField(null=False)
    News_area = models.CharField(max_length=10)

class Fire(models.Model):
    Fire_loc = models.CharField(max_length=200)
    Fire_time = models.DateTimeField(null=False)
    Fire_state = models.CharField(max_length=200)
    Fire_area = models.CharField(max_length=10)