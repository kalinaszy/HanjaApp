from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
import random

# Create your views here.
from game.models import Answer, Score, Guess

from user.forms import LoginForm


class PlayGameView(View):

        def get(self, request):
            if not request.user.is_authenticated:
                return redirect('/login')
            list_answers = []
            puzzle = Guess.objects.order_by('?').first()
            image = puzzle.image_character
            answer1 = puzzle.guessed_right
            answer2 = puzzle.guessed_wrong1
            answer3 = puzzle.guessed_wrong2
            #to zmienic pozniej na ladnie:
            list_answers.append(answer1)
            list_answers.append(answer2)
            list_answers.append(answer3)
            random.shuffle(list_answers)
            score = Score.objects.filter(player=request.user, games_number__lt=10).first()
            players_score = 0 if score is None else score.players_score
            return render(request, 'play.html', {'list_answers':list_answers, 'image': image, 'puzzle_id': puzzle.id, 'score':\
                                                 players_score})

        def post(self, request):
            if not request.user.is_authenticated:
                return redirect('/login')
            puzzle_id = request.POST.get('puzzle_id')
            answer = request.POST.get('answer')
            puzzle = Guess.objects.get(id=puzzle_id)
            score = Score.objects.filter(player=request.user, games_number__lt=10).first()
            if score is None:
                score = Score.objects.create(player=request.user)
            if puzzle.guessed_right == answer:
                score.players_score += 1
            score.games_number += 1
            score.save()
            return HttpResponseRedirect('/play')


class BestScoresView(View):

    def get(self, request):
        all_scores = Score.objects.order_by('-players_score')
        return render(request, 'best_scores.html', {'all_scores':all_scores})

