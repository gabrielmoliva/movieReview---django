from django.urls import path
from . import views

urlpatterns = [
    path('movies', views.getAllMovies),
    path('movies/add', views.addMovie),
    path('movies/review', views.review),
    path('movies/<int:movie_id>', views.getMovie)
]
