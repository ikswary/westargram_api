import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core.validators import validate_email

from .models import User


class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            this_user = User(
                user_id=data['user_id'],
                password=data['password'],
                email=data['email']
            )
        except KeyError:
            return JsonResponse({'messages': 'ARGUMENT_NOT_PASSED'}, status=400)

        if this_user.user_id == '' or this_user.password == '' or this_user.email == '':
            return JsonResponse({'messages': 'EMPTY_ARGUMENT_PASSED'}, status=400)

        try:
            validate_email(User.email)
        except ValidationError:
            return JsonResponse({'messages': 'INVALID_EMAIL'})

        if not User.objects.filter(user_id=this_user.user_id).exists():
            return JsonResponse({'messages': 'DUPLICATED_USER_ID'}, status=400)

        this_user.save()
        return HttpResponse(status=201)