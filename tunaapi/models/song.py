from django.db import models
from .artist import Artist

class Song(models.Model):
  title = models.CharField(max_length=50)
  artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
  album = models.CharField(max_length=50)
  length = models.IntegerField()
  
  def __str__(self):
    return self.title