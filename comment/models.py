from django.db import models

from user.models import User


class Comment(models.Model):
    user       = models.ForeignKey(User, on_delete='CASCADE')
    comment    = models.CharField(max_length=1000)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'
