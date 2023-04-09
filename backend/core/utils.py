import base64

from django.core.files.base import ContentFile
from django.db.models import Sum
from rest_framework import mixins, serializers, viewsets

from recipes.models import RecipeIngredient


class ListRetrieveModelMixin(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    pass


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


def get_product_list(request):
    product_dict = RecipeIngredient.objects.filter(
        recipe__shopping_card__user=request.user).values(
        'ingredient__name', 'ingredient__measurement_unit').annotate(
        total_amount=Sum('amount'))
    product_list = []
    for product in product_dict:
        name, unit, amount = product.values()
        line = f'{name} {amount} {unit}\n'
        product_list.append(line)
    return ''.join(product_list)
