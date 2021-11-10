import requests
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

        return render(request, 'search_results.html', context)

    return render(request, 'search.html')
