from django.core.exceptions import ValidationError

# в core вынести не смог, ловлю ошибку из за from recipes.models import RecipeIngredient
# куда валидацтю лучше спрятать ?
def username_validator(username):
    stop_word = ['admin', 'superuser', 'root']
    if username.lower() in stop_word:
        raise ValidationError('имя пользователя находится в списке запрещенных')