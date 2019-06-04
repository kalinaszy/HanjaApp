from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Guess(models.Model):
    image_character = models.ImageField(upload_to="gallery")
    guessed_right = models.CharField(max_length=50)
    guessed_wrong1 = models.CharField(max_length=50)
    guessed_wrong2 = models.CharField(max_length=50)


class Score(models.Model):
    games_number = models.IntegerField(default=0)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    players_score = models.IntegerField(default=0)
    when = models.DateTimeField(auto_now_add=True)
    question = models.ManyToManyField(Guess, blank=True, through='Answer')


class Answer(models.Model):
    game = models.ForeignKey(Score, on_delete=models.CASCADE)
    task = models.ForeignKey(Guess, on_delete=models.CASCADE)
    correct = models.BooleanField()


class Comment(models.Model):
    comment_content = models.TextField()
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    date_sent = models.DateTimeField(auto_now_add=True)

