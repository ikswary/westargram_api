import json

from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from .models import Comment
from user.models import User


class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if data['comment'] == '':
                return JsonResponse({'messages': 'EMPTY_ARGUMENT_PASSED'}, status=400)

            Comment(
                user=User.objects.get(user_id=data['user_id']),
                comment=data['comment']
            ).save()
            return HttpResponse(status=200)
        
        except KeyError:
            return JsonResponse({'messages': 'ARGUMENT_NOT_PASSED'}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({'messages': 'INVALID_USER'}, status=404)

    def get(self, request, target=None):
        if target is None:
            comments = Comment.objects.values('comment')
            print(comments)
            return JsonResponse({'messages': list(comments)}, status=200)

        target_user = get_object_or_404(User, user_id=target)
        comments = Comment.objects.filter(user_id=target_user.id).values('comment')
        return JsonResponse({'messages': list(comments)}, status=200)
