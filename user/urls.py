from django.urls import path
from user.views import UserView, LogInView

urlpatterns = [
    path('/register', UserView.as_view()),
    path('/login', LogInView.as_view()),
]
