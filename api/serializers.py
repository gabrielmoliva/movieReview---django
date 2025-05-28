from rest_framework import serializers
from base.models import Movie, Review, Actor

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MoviePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('name', 'launchDate', 'language', 'rating', 'country', 'director', 'description')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class ActorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('name', )