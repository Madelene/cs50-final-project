import json

import requests
from django.contrib import messages
from django.shortcuts import redirect, render
from moviesiveseen.settings import OMDB

from .models import Movie

BASE_URL = "http://www.omdbapi.com/"
URL = f"{BASE_URL}{OMDB['api_key']}"


def search(request):
    if request.method == 'POST':
        query = request.POST.get('q')
        request_url = f"{URL}&s={query}"
        response = requests.get(request_url)
        movies = response.json()
        context = {
            'movies': movies['Search']
        }

        movies = request.POST.getlist('watched')
        json_str = [m.replace("\'", "\"") for m in movies]

        for m in json_str:
            title = json.loads(m)['Title']
            poster = json.loads(m)['Poster']

            Movie.objects.create(
                title=title,
                poster=poster
            )
            msg = f"{title} is saved to your watched list."
            messages.success(request, msg)
        return render(request, 'search_results.html', context)

    return render(request, 'search.html')


def watched(request):
    if request.method == 'GET':
        movies_seen = Movie.objects.all().order_by('title')
        context = {
            'movies': movies_seen
        }
    return render(request, 'watched.html', context)
