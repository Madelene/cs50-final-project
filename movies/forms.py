from django import forms as djforms
from movies.models import Movie


class MoviesForm(djforms.ModelForm):
    # here we only need to define the field we want to be editable
    movies = djforms.ModelMultipleChoiceField(
        queryset=Movie.objects.all(), required=False
    )
