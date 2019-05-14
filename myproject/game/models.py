from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# class User(models.User):
#     username = models.CharField(max_length=30, null=False)
#     email = models.EmailField(null=False)
#     password = models.CharField(null=False)

class Guess(models.Model):
    image_character = models.ImageField()
    guessed_right = models.CharField(max_length=50)
    guessed_wrong1 = models.CharField(max_length=50)
    guessed_wrong2 = models.CharField(max_length=50)

class Score(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    players_score = models.IntegerField()
    when = models.DateTimeField()

class Answer(models.Model):
    game = models.ForeignKey(Score, on_delete=models.CASCADE)
    task = models.ForeignKey(Guess, on_delete=models.CASCADE)
    correct = models.BooleanField()

