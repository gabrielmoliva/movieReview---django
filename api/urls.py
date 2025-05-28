from django.urls import path
from . import views

urlpatterns = [
    path('movies', views.getAllMovies),
    path('movies/add', views.addMovie),
    path('movies/review', views.review),
    path('movies/<int:movie_id>', views.getMovie),
    path('movies/<int:movie_id>/reviews', views.getAllReviews),
    path('actors', views.getAllActors),
    path('actors/add', views.addActor),
    path('movies/<int:movie_id>/addActor/<int:actor_id>', views.addActorToMovie),
    path('movies/<int:movie_id>/actors', views.getMovieActors)
]
