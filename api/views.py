from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Movie, Review, Actor
from .serializers import MovieSerializer, MoviePostSerializer, ReviewSerializer, ActorSerializer, ActorPostSerializer
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

@api_view(['GET'])
def getAllReviews(request, movie_id):
    try:
        reviews = Review.objects.filter(movie_id=movie_id)
    except Movie.DoesNotExist:
        return Response({'detail': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ReviewSerializer(reviews, many=True)
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

@api_view(['GET'])
def getAllActors(request):
    actors = Actor.objects.all()
    serializer = ActorSerializer(actors, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def addActor(request):
    serializer = ActorPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def addActorToMovie(request, movie_id, actor_id):
    try:
        movie = Movie.objects.filter(pk=movie_id).get()
    except Movie.DoesNotExist:
        return Response({'detail': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        actor = Actor.objects.filter(pk=actor_id).get()
    except Actor.DoesNotExist:
        return Response({'detail': 'Actor not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        movie.addActor(actor)
        actor.incrementMovies()
        return Response({'detail': 'Actor added to movie.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)