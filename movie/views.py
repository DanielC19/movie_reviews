from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from .models import Movie

def home(request) :
    # return render(request, 'home.html', { 'name': 'Daniel Correa' })
    searchTerm = request.GET.get('searchMovie')
    if searchTerm :
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else :
        movies = Movie.objects.all()

    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request) :
    return render(request, 'about.html')

def signup(request) :
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request) :
    matplotlib.use('Agg')

    movies = Movie.objects.all()

    movie_count_by_year = {}
    movie_count_by_genre = {}

    for movie in movies :
        # Search by year
        year = movie.year if movie.year else 'None'

        if year in movie_count_by_year :
            movie_count_by_year[year] += 1
        else :
            movie_count_by_year[year] = 1

        # Search by genre
        genre = movie.genre if movie.genre else 'None'
        genre = genre.split(',')[0]

        if genre in movie_count_by_genre :
            movie_count_by_genre[genre] += 1
        else :
            movie_count_by_genre[genre] = 1

    bar_positions_year = range(len(movie_count_by_year))

    plt.bar(bar_positions_year, movie_count_by_year.values(), width=0.5, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_year, movie_count_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png)
    graphic_year = graphic_year.decode('utf-8')

    bar_positions_genre = range(len(movie_count_by_genre))

    plt.bar(bar_positions_genre, movie_count_by_genre.values(), width=0.5, align='center')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, movie_count_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png)
    graphic_genre = graphic_genre.decode('utf-8')

    return render(request, 'statistics.html', {'graphic_year': graphic_year, 'graphic_genre': graphic_genre})