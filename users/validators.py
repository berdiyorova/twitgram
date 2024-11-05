import re

from rest_framework.exceptions import ValidationError


class GmailValidator:
    def __call__(self, value):
        pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")

        if not re.match(pattern, value):
            raise ValidationError('Invalid email format.')

        if not value.endswith('@gmail.com'):
            raise ValidationError("Email must end with '@gmail.com'.")
