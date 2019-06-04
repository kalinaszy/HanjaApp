import random
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView, UpdateView

from game.forms import MessageForm
from game.models import Answer, Score, Guess, Comment


class IndexView(View):
#tu krocej templatka
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
            return render(
                request, 'play.html', {

# Create your models here.

# class User(models.User):
#     username = models.CharField(max_length=30, null=False)
#     email = models.EmailField(null=False)
#     password = models.CharField(null=False)               'list_answers': list_answers,
                'image': image,
                'puzzle_id': puzzle.id,
                'score': players_score,
                'score_games_number': score_games_number
                }
            )

        def post(self, request):
            if not request.user.is_authenticated:
                return redirect('/login')
            puzzle_id = request.POST.get('puzzle_id')
            answer = request.POST.get('answer')
            try:
                puzzle = Guess.objects.get(id=puzzle_id)
            except puzzle.DoesNotExist:
                raise FileNotFoundError
            score = Score.objects.filter(player=request.user, games_number__lt=10).first()
            if score is None:
                score = Score.objects.create(player=request.user)
            if puzzle.guessed_right == answer:
                score.players_score += 1
                correct = True
            else:
                correct = False
            Answer.objects.create(task=puzzle, game=score, correct=correct)
            score.games_number += 1
            score.save()
            if score.games_number == 10:
                return HttpResponseRedirect('/check_answers')
            return HttpResponseRedirect('/play')


class CheckAnswersView(View):

    def get(self, request):
        answers = Answer.objects.filter(game=Score.objects.latest('pk'))
        return render(request, 'check_answers.html', {'answers': answers})



class ComposeCommentView(View):

        def get(self, request):
            if request.user.is_authenticated:
                form = MessageForm()
                return render(request, 'compose_comment.html', {'form':form})
            else:
                message = "You need to log in first to add comments!"
                return render(request, 'login.html', {'message': message, 'action':'/login'})

        def post(self, request):
            form = MessageForm(request.POST) #user jest automatyczny od User
            if form.is_valid():
                user_logged = request.user
                form.instance.sent_by = user_logged #a dlaczego nie form.cleaned data?
                form.save()
                return HttpResponseRedirect('/comments')
            else:
                return HttpResponseRedirect('compose_comments')


class CommentsView(ListView):
    model = Comment
    template_name = 'comments_view.html'
    paginate_by = 10


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'delete.html'
    success_url = reverse_lazy('comments_list')


class CommentEditView(UpdateView):
    model = Comment
    template_name = 'comment_update_form.html'
    fields = ['comment_content']
    success_url = reverse_lazy('comments_list')


class BestScoresView(View):

    def get(self, request):
        all_scores = Score.objects.order_by('-players_score')
        paginator = Paginator(all_scores, 10)
        page = request.GET.get('page')
        all_scores = paginator.get_page(page)
        return render(request, 'best_scores.html', {'all_scores': all_scores})
