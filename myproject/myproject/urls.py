"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from game import views
from myproject import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from game.views import IndexView, PlayGameView, BestScoresView, CheckAnswersView, ComposeCommentView, CommentsView, \
    CommentDeleteView, CommentEditView
from nbp.views import EuroToday
from user.views import LoginView, AddUserView, LogoutView

router = routers.DefaultRouter()
router.register(r'scores', views.ScoresViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('add', AddUserView.as_view()),
    path('play', PlayGameView.as_view()),
    path('best_scores', BestScoresView.as_view()),
    path('check_answers', CheckAnswersView.as_view()),
    path('compose_comments', ComposeCommentView.as_view()),
    path('comments', CommentsView.as_view(), name='comments_list'),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name='delete_comment'),
    path('comment/<int:pk>/edit', CommentEditView.as_view(), name='edit_comment'),
    path('euro_today', EuroToday.as_view(), name='euro'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
