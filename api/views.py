from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Movie, Vote
from .serializers import MovieSerializer, MoviePostSerializer, VoteSerializer


@api_view(['GET'])
def getMovies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def addMovie(request):
    serializer = MoviePostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data)

@api_view(['POST'])
def vote(request):
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        movieId = serializer.validated_data['movie'].id
        newVoteScore = serializer.validated_data['score']
        movie = Movie.objects.filter(pk=movieId).get()
        movie.updateScore(newVoteScore)
        serializer.save()

        return Response(serializer.data)