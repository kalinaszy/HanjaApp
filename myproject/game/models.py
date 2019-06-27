from django.contrib.auth.models import User
from django.db import models




class Guess(models.Model):
    #image_character = models.ImageField(upload_to="gallery", null=True)
    char_character = models.CharField(max_length=10, null=True)
    guessed_right = models.CharField(max_length=256)
    guessed_wrong1 = models.CharField(max_length=256)
    guessed_wrong2 = models.CharField(max_length=256)

    # def get_char(self):
    #     return self.char_character or self.image_character


class Score(models.Model):
    games_number = models.IntegerField(default=0)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    players_score = models.IntegerField(default=0)
    when = models.DateTimeField(auto_now_add=True)
    question = models.ManyToManyField(Guess, blank=True, through='Answer')

    def take_answer(self, puzzle, correct):
        if correct:
            self.players_score += 1
        if self.games_number <= 10:
            self.games_number += 1
            Answer.objects.create(task=puzzle, game=self, correct=correct)
        self.save()


class Answer(models.Model):
    game = models.ForeignKey(Score, on_delete=models.CASCADE)
    task = models.ForeignKey(Guess, on_delete=models.CASCADE)
    correct = models.BooleanField()


class Comment(models.Model):
    comment_content = models.TextField()
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    date_sent = models.DateTimeField(auto_now_add=True)

