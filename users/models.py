from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ManyToManyField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from movies.models import Movie


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    movies = ManyToManyField(Movie, verbose_name="List of Movies")

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
