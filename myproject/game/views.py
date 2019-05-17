from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
import random

# Create your views here.
from game.models import Answer, Score, Guess


class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')



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
            list_answers.append(answer1)
            list_answers.append(answer2)
            list_answers.append(answer3)
            random.shuffle(list_answers)
            score = Score.objects.filter(player=request.user, games_number__lt=10).first()
            players_score = 0 if score is None else score.players_score
            score_games_number = 0 if score is None else score.games_number
            return render(request, 'play.html', {
                'list_answers': list_answers, 'image': image, 'puzzle_id': puzzle.id, 'score': players_score,\
                'score_games_number': score_games_number})

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
                Answer.objects.create(task=puzzle, game=score, correct=True)
            else:
                Answer.objects.create(task=puzzle, game=score, correct=False)
            score.games_number += 1
            score.save()
            if score.games_number == 10:
                return HttpResponseRedirect('/check_answers')
            return HttpResponseRedirect('/play')




class CheckAnswersView(View):


    def get(self, request):
        answers = Answer.objects.filter(game=Score.objects.latest('pk'))
        return render(request, 'check_answers.html', {'answers': answers})




class BestScoresView(View):


    def get(self, request):
        all_scores = Score.objects.order_by('-players_score')
        paginator = Paginator(all_scores, 10)
        page = request.GET.get('page')
        all_scores = paginator.get_page(page)
        return render(request, 'best_scores.html', {'all_scores': all_scores})
