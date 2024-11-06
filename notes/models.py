from django.db import models

from users.models import UserModel


class NoteModel(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='notes')
