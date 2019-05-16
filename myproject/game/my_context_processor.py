def my_cp(request):
    ctx = {
        'zalogowany': request.user.is_authenticated,
        'user': request.user.username if request.user.is_authenticated else "Anonymous User",
    }
    return ctx