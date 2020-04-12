import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist

from .models import User


class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if data['user_id'] == '' or data['password'] == '' or data['email'] == '':
                return JsonResponse({'messages': 'EMPTY_ARGUMENT_PASSED'}, status=400)

            if User.objects.filter(user_id=data['user_id']).exists():
                return JsonResponse({'messages': 'DUPLICATED_USER_ID'}, status=400)

            validate_email(data['email'].email)
            User(
                user_id=data['user_id'],
                password=data['password'],
                email=data['email']
            ).save()
            return HttpResponse(status=201)

        except KeyError:
            return JsonResponse({'messages': 'ARGUMENT_NOT_PASSED'}, status=400)

        except ValidationError:
            return JsonResponse({'messages': 'INVALID_EMAIL'})


class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            this_user = User.objects.get(user_id=data['user_id'])
            if this_user.password == data['password']:
                return HttpResponse(status=200)

            return HttpResponse(status=401)
        except KeyError:
            return JsonResponse({'messages': 'ARGUMENT_NOT_PASSED'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'messages': 'INVALID_USER'}, status=404)
