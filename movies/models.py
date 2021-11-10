from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    poster = models.ImageField()
    has_seen = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "movies"

    def __str__(self):
        return self.title
