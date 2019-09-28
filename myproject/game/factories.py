import factory
from django.contrib.auth.models import User

from game.models import Guess, Score


class GuessFactory(factory.Factory):
    class Meta:
        model = Guess
    char_character = 'dhdd'
    guessed_right = 'fff'
    guessed_wrong1 = 'ffvv'
    guessed_wrong2 = 'ffet'


class UserFactory(factory.Factory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: 'user{0}'.format(n))

class ScoreFactory(factory.Factory):
    class Meta:
        model = Score
    games_number = 0
    players_score = 0
    @factory.post_generation
    def questions(selfself, create, extracted, ** kwargs):
        if not create:
        # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for topping in extracted:
                self.questions.add(question)

