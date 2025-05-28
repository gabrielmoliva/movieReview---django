from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Movie, Review
from .serializers import MovieSerializer, MoviePostSerializer, ReviewSerializer
from rest_framework import status


@api_view(['GET'])
def getAllMovies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getMovie(request, movie_id):
    try:
        movie = Movie.objects.filter(pk=movie_id).get()
    except Movie.DoesNotExist:
        return Response({'detail': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

@api_view(['POST'])
def addMovie(request):
    serializer = MoviePostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def review(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        movie_id = serializer.validated_data['movie'].id
        newVoteScore = serializer.validated_data['score']
        movie = Movie.objects.filter(pk=movie_id).get()
        movie.updateScore(newVoteScore)
        serializer.save()
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)