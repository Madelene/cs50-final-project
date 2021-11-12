import json
import math

import requests
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from moviesiveseen.settings import OMDB
from users.models import User

from .models import Movie

BASE_URL = "http://www.omdbapi.com/"
URL = f"{BASE_URL}{OMDB['api_key']}"


def main_request(query, page):
    '''Initial request to the OMDB API'''
    request_url = f"{URL}&s={query}&page={page}"
    response = requests.get(request_url)
    return response.json()


def get_total_pages(movies):
    """Gets total number of pages, based on the value in totalResults"""
    total_results = int(movies['totalResults'])
    return math.ceil(total_results / 10)


def search(request):
    """Search the OMDB database (http://www.omdbapi.com/)."""

    if not request.user.is_authenticated:
        return redirect('users:movies_login')

    if request.method == 'POST':
        query = request.POST.get('q')
        movies = main_request(query, 1)

        movies_list = []
        for page in range(1, get_total_pages(movies) + 1):
            movies = main_request(query, page)
            movies_list.append(movies['Search'])
        # movies_list returns a list of lists of objects.
        # Needed to flatten that list
        flat_movies_list = [item for sublist in movies_list for item in sublist]
        print(flat_movies_list)
        print(len(flat_movies_list))
        context = {
            'movies': flat_movies_list,
        }

        watched_movies = request.POST.getlist('watched')
        json_str = [m.replace("\'", "\"") for m in watched_movies]

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
