from rest_framework import serializers
from base.models import Movie, Review

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