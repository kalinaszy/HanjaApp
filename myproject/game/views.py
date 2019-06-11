import random

from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DeleteView, UpdateView, FormView

from game.forms import MessageForm, EmailForm
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
            list_answers.extend([puzzle.guessed_right, puzzle.guessed_wrong1, puzzle.guessed_wrong2])
            random.shuffle(list_answers)
            score = Score.objects.filter(player=request.user, games_number__lt=10).first()
            players_score = 0 if score is None else score.players_score
            score_games_number = 0 if score is None else score.games_number
            return render(
                request, 'play.html', {
                'list_answers': list_answers,
                'image': puzzle.image_character,
                'puzzle_id': puzzle.id,
                'score': players_score,
                'score_games_number': score_games_number
                }
            )

        def find_puzzle(self, request):
            puzzle_id = request.POST.get('puzzle_id')
            try:
                puzzle = Guess.objects.get(id=puzzle_id)
            except Guess.DoesNotExist:
                raise FileNotFoundError
            return puzzle

        def post(self, request):
            if not request.user.is_authenticated:
                return redirect('/login')
            answer = request.POST.get('answer')
            puzzle = self.find_puzzle(request)

            score = Score.objects.filter(player=request.user, games_number__lt=10).first()
            if score is None:
                score = Score.objects.create(player=request.user)
            correct = puzzle.guessed_right == answer
            score.take_answer(puzzle, correct=correct)
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
            form = MessageForm(request.POST)  # user jest automatyczny od User
            if form.is_valid():
                form.instance.sent_by = request.user  # dlaczego nie form.cleaned data?
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

    def get_context_data(self, **kwargs):
        ctx = super(CommentEditView, self).get_context_data(**kwargs)
        ctx['current_time'] = timezone.now()
        return ctx


class BestScoresView(ListView):
    queryset = Score.objects.order_by('-players_score')
    paginate_by = 10
    template_name = 'best_scores.html'

class SendAnEmailView(FormView):
    form_class = EmailForm
    template_name = 'email.html'

    def post(self, request):
        send_mail(
            'Subject here',
            'Here is the message.',
            'kamil.radomski@laboratorium.ee',
            ['kalina.szymczyk@gmail.com'],
        )



