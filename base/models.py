from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class Actor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, blank=False, max_length=200)
    numberMovies = models.IntegerField(default=0)

    def incrementMovies(self):
        self.numberMovies+=1
        self.save()

class Movie(models.Model):
    RATING_CHOICES = [
        ('G', 'General Public'),
        ('PG', 'Parental Guidance Suggested'),
        ('R', 'Restricted')
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    launchDate = models.DateField(null=False, blank=False)
    score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MinValueValidator(10.0)])
    numberOfVotes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    language = models.CharField(default='?', max_length=20)
    rating = models.CharField(choices=RATING_CHOICES, max_length=2, null=False, blank=False)
    country = models.CharField(max_length=35, null=False, blank=False)
    director = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(default='')
    actors = models.ManyToManyField(Actor)

    def updateScore(self, newReviewScore):
        old_total = self.score * self.numberOfVotes
        self.numberOfVotes += 1
        self.score = (old_total + newReviewScore) / self.numberOfVotes
        self.save()

    def addActor(self, actor):
        self.actors.add(actor)
        self.save()

    def containsActor(self, actor):
        return self.actors.contains(actor)
    
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    email = models.CharField(max_length=50, null=False, blank=False, unique=True) # Field used for login
    password = models.CharField(max_length=20, null=False, blank=False)

    def create(self, username, email):
        self.username=username
        self.email = email
        return self

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    score = models.FloatField(null=False, validators=[MinValueValidator(0.0), MinValueValidator(10.0)])
    reviewText = models.TextField(null=False, blank=False, max_length=500)
    reviewDate = models.DateTimeField(auto_created=True, auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
