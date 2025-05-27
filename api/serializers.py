from rest_framework import serializers
from base.models import Movie, Vote

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MoviePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('name', 'launchDate', 'language', 'rating', 'country', 'director', 'description')

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'