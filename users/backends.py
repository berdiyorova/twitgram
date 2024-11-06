from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import UserModel

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(
                Q(username=username) | Q(email=username)
            )
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None