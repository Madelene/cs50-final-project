import json

import requests
from django.contrib import messages
from django.shortcuts import redirect, render
from moviesiveseen.settings import OMDB
from users.models import User

from .models import Movie

BASE_URL = "http://www.omdbapi.com/"
URL = f"{BASE_URL}{OMDB['api_key']}"


def search(request):
    """Search the OMDB database (http://www.omdbapi.com/)."""

    if not request.user.is_authenticated:
        return redirect('users:movies_login')

    if request.method == 'POST':
        query = request.POST.get('q')
        request_url = f"{URL}&s={query}"
        response = requests.get(request_url)
        movies = response.json()
        total_results = int(movies['totalResults'])

        context = {
            'movies': movies['Search']
        }

        movies = request.POST.getlist('watched')
        json_str = [m.replace("\'", "\"") for m in movies]

        user = User.objects.get(username=request.user.username)

        for m in json_str:
            title = json.loads(m)['Title']
            poster = json.loads(m)['Poster']

            movie = Movie.objects.create(
                title=title,
                poster=poster,
                has_seen=True,
            )
            user.movies.add(movie)
            user.save()
            msg = f"{title} is saved to your watched list."
            messages.success(request, msg)
        return render(request, 'search_results.html', context)

    return render(request, 'search.html')


def watched(request):
    """Grab and displays movies that have been watched."""
    if request.method == 'GET':
        movies_seen = request.user.movies.all().order_by('title')
        context = {
            'movies': movies_seen
        }
    return render(request, 'watched.html', context)
