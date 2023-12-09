from django.db import models
from .artist import Artist
from .genre import Genre

class Song(models.Model):
  title = models.CharField(max_length=50)
  artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
  album = models.CharField(max_length=50)
  length = models.IntegerField()
  genre = models.ForeignKey(Genre, on_delete=models.CASCADE,related_name='song', default=1)
  
  def __str__(self):
    return self.title
