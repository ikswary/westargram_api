import json

from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from .models import Comment
from user.models import User


class CommentWriteView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if data['user_id'] == '' or data['comment'] == '':
                return JsonResponse({'messages': 'EMPTY_ARGUMENT_PASSED'}, status=400)

            Comment(
                user=User.objects.get(user_id=data['user_id']),
                comment=data['comment']
            ).save()
        except KeyError:
            return JsonResponse({'messages': 'ARGUMENT_NOT_PASSED'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'messages': 'INVALID_USER'}, status=404)
        return HttpResponse(status=200)

class 