from django.db import models

class Genre(models.Model):
    description = models.CharField(max_length=240)

    def __str__(self):
        return self.description

    def song_count(self):
        return self.song_set.count()

