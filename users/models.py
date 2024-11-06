import random
from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import GmailValidator


class UserModel(AbstractUser):
    email = models.EmailField(unique=True, validators=[GmailValidator])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def create_verify_code(self):
        code = "".join(str(random.randint(0, 100) // 10) for _ in range(4))
        expiration_time = datetime.now() + timedelta(minutes=5)

        UserConfirmModel.objects.create(
            code=code,
            expiration_time=expiration_time,
            user=self,
        )
        return code


class UserConfirmModel(models.Model):
    code = models.CharField(max_length=4)
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='verify_codes')

    def __str__(self):
        return self.user.__str__()
