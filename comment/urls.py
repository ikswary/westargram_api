from django.urls import path

from .views import CommentWriteView

urlpatterns = [
    path('', CommentWriteView.as_view())
]
