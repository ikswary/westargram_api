from django.db import models


class UserData(models.Model):
    user_id    = models.CharField(max_length=50)
    password   = models.CharField(max_length=400)
    email      = models.EmailField(max_length=400)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
