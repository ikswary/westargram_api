from django.urls import path

from .views import CommentView

urlpatterns = [
    path('<str:target>', CommentView.as_view()),
    path('', CommentView.as_view()),
]