import json

from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from .models import Comment
from user.models import User


class WriteCommentView(View):
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


class ShowCommentView(View):
    def get(self, request, target=None):
        all_comments = []
        if target is None:
            comments = Comment.objects.values()
        elif target is not None:
            target_user = get_object_or_404(User, user_id=target)
            comments = Comment.objects.filter(user_id=target_user.id)
        if not len(comments):
            return HttpResponse(status=404)

        print(comments)
        for each in comments:
            print(each)
            all_comments.append(each.comment)
        return JsonResponse({'messages': all_comments}, status=200)