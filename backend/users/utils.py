from django.core.exceptions import ValidationError


def username_validator(username):
    stop_word = ['me']
    if username.lower() in stop_word:
        raise ValidationError(
            'имя пользователя находится в списке запрещенных')
