import factory

from game.models import Guess

class GuessFactory(factory.Factory):
    class Meta:
        model = Guess
    char_character = 'dhdd'
    guessed_right = 'fff'
    guessed_wrong1 = 'ffvv'
    guessed_wrong2 = 'ffet'