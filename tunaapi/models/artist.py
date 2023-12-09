from django.db import models
from .genre import Genre

class Artist(models.Model):
  name = models.CharField(max_length=100)
  age = models.IntegerField()
  bio = models.TextField()
  genre = models.ForeignKey(Genre, on_delete=models.CASCADE,related_name='artists', default=1)
  
  def __str__(self):
    return self.name
