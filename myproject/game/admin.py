from django.contrib import admin

# Register your models here.
from game.models import Guess, Score, Answer


class GuessAdmin(admin.ModelAdmin):
    pass


class ScoreAdmin(admin.ModelAdmin):
    pass


class AnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Guess, GuessAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Answer, AnswerAdmin)