from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
from game.models import Answer, Score

# class Guess(models.Model):
#     image_character = models.ImageField()
#     guessed_right = models.CharField(max_length=50)
#     guessed_wrong1 = models.CharField(max_length=50)
#     guessed_wrong2 = models.CharField(max_length=50)
class PlayGameView(View):



    # score = 0
    # if Answer.correct == True:
    #     score += 1
    # else:
    #     score
    # #if user.is_active:
    #
    # def CheckAnswers():
    #     pass
    #
    # def CountScoreView(View):
    #     pass


class BestScoresView(View):

    def get(self, request):
        users = User.objects.all()
        #all_scores = Score.objects.annotate(count_scores=Count('players_score').order_by('-count_scores'))
        all_scores = Score.objects.order_by('-score')[0:]
        return render(request, 'best_scores.html', {'all_scores':all_scores})












    # my_area = Area.objects.all()[0]
    # Event.objects.filter(area=my_area).count()


