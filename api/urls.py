from django.urls import path
from . import views

urlpatterns = [
    path('movies', views.getMovies),
    path('movies/add', views.addMovie),
    path('movies/review', views.review)
]
