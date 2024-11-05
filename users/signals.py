import threading

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from Config.settings import EMAIL_HOST_USER
from users.models import UserModel


@receiver(post_save, sender=UserModel)
def send_code_to_email(sender, instance, created, **kwargs):
    if created:
        code = instance.create_verify_code()
        subject = "Welcome to TwitGram!"
        message = f"Hi, {instance.username}, Your verification code is: {code}."

        t = threading.Thread(target=send_mail, args=(subject, message, EMAIL_HOST_USER, [instance.email]))
        t.start()
