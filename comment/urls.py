from django.urls import path

from .views import WriteCommentView, ShowCommentView

urlpatterns = [
    path('/show', ShowCommentView.as_view()),
    path('', WriteCommentView.as_view()),
]
