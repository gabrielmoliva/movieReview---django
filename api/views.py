from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from base.models import Movie, Review, Actor, User
from .serializers import MovieSerializer, MoviePostSerializer, ReviewCreateSerializer, ActorSerializer, ActorPostSerializer, UserSerializer, RegisterUserSerializer, ReviewGetSerializer
from rest_framework import status
from .authentication import CustomBasicAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login as django_login, logout as django_logout, authenticate

# authentication
@api_view(["POST"])
@authentication_classes([CustomBasicAuthentication, SessionAuthentication])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        django_login(request, user)
        return Response(UserSerializer(user).data)
    else:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    django_logout(request)
    return Response({})

@api_view(["GET"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)

@api_view(['POST'])
def register(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# authentication

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def getAllMovies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def getMovie(request, movie_id):
    try:
        movie = Movie.objects.filter(pk=movie_id).get()
    except Movie.DoesNotExist:
        return Response({'detail': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def getReviewsByMovie(request, movie_id):
    try:
        reviews = Review.objects.filter(movie_id=movie_id)
    except Movie.DoesNotExist:
        return Response({'detail': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ReviewGetSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def getReviewsByUser(request, user_id):
    try:
        reviews = Review.objects.filter(user_id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ReviewGetSerializer(reviews, many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def review(request):
    serializer = ReviewCreateSerializer(data=request.data)
    if serializer.is_valid():
        movie_id = serializer.validated_data['movie'].id
        newVoteScore = serializer.validated_data['score']
        movie = Movie.objects.filter(pk=movie_id).get()
        movie.updateScore(newVoteScore)
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def addMovie(request):
    serializer = MoviePostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def getAllActors(request):
    actors = Actor.objects.all()
    serializer = ActorSerializer(actors, many=True)

    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def addActor(request):
    serializer = ActorPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def addActorToMovie(request, movie_id, actor_id):
    try:
        movie = Movie.objects.filter(pk=movie_id).get()
    except Movie.DoesNotExist:
        return Response({'detail': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        actor = Actor.objects.filter(pk=actor_id).get()
    except Actor.DoesNotExist:
        return Response({'detail': 'Actor not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if movie.containsActor(actor):
        return Response({'detail': 'Actor is already in the movie.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        movie.addActor(actor)
        actor.incrementMovies()
        return Response({'detail': 'Actor added to movie.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def getMovieActors(request, movie_id):
    try:
        movie = Movie.objects.filter(pk=movie_id).get()
    except Movie.DoesNotExist:
        return Response({'detail': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    actors = movie.actors
    serialier = ActorSerializer(actors, many=True)
    return Response(serialier.data)