import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist

from .models import User


class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if data['user_id'] == '' or data['password'] == '' or data['email'] == '':
                return JsonResponse({'messages': 'EMPTY_ARGUMENT_PASSED'}, status=400)

            this_user = User(
                user_id=data['user_id'],
                password=data['password'],
                email=data['email']
            )
        except KeyError:
            return JsonResponse({'messages': 'ARGUMENT_NOT_PASSED'}, status=400)

        try:
            validate_email(this_user.email)
        except ValidationError:
            return JsonResponse({'messages': 'INVALID_EMAIL'})

        if User.objects.filter(user_id=this_user.user_id).exists():
            return JsonResponse({'messages': 'DUPLICATED_USER_ID'}, status=400)

        this_user.save()
        return HttpResponse(status=201)


class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if data['user_id'] == '' or data['password'] == '':
                return JsonResponse({'messages': 'EMPTY_ARGUMENT_PASSED'}, status=400)

            this_user = User.objects.get(user_id=data['user_id'])
        except KeyError:
            return JsonResponse({'messages': 'ARGUMENT_NOT_PASSED'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'messages': 'INVALID_USER'}, status=404)

        if this_user.password == data['password']:
            return HttpResponse(status=200)
        print(this_user.password, data['password'])
        return HttpResponse(status=401)