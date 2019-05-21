from game.forms import MessageForm


def my_cp(request):
    ctx = {
        'zalogowany': request.user.is_authenticated,
        'myuser': request.user.username if request.user.is_authenticated else "Anonymous User",
        'comment_form': MessageForm(),
    }
    return ctx