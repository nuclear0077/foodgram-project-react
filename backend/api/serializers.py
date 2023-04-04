import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from recipes.models import Recipe, Tag, RecipeIngredient, Ingredient, Follow, ShoppingCard, Favorite

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class UserWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')


class UserReadSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'is_subscribed')

    def get_is_subscribed(self, user):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        follow = Follow.objects.filter(user=request.user, author=user).first()
        if not follow:
            return False
        return True


class AuthTokenSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)  # serializers.(max_length=254, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, attrs):
        user = User.objects.filter(
            email=attrs.get('email'),
            password=attrs.get('password')
        ).first()
        if not user:
            raise serializers.ValidationError('Неверные учетные данные. Пожалуйста, попробуйте снова.')
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return {'auth_token': token.key}


class SetPasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(source='password', required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('current_password', 'new_password')

    def validate(self, attrs):
        if not self.context.get('request').user.password == attrs.get('password'):
            raise serializers.ValidationError('Неверный пароль. Пожалуйста, попробуйте снова.')
        return attrs


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class SubscriptionRecipeSerializerRead(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    username = serializers.ReadOnlyField(source='author.username')
    email = serializers.ReadOnlyField(source='author.email')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, user):
        return True

    def validate(self, attrs):
        user = self.context.get('request').user
        author = self.context.get('user')
        if author == user:
            raise serializers.ValidationError({'error': 'Нельзя подписываться на самого себя'}, code=400)
        if Follow.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError({'error': 'Вы уже подписаны на данного автоора'}, code=400)
        return attrs

    def get_recipes(self, attrs):
        author = attrs.author
        all_recipes = Recipe.objects.filter(author=author)
        return SubscriptionRecipeSerializerRead(all_recipes, many=True).data

    def get_recipes_count(self, attrs):
        author = attrs.author
        all_recipes = Recipe.objects.filter(author=author)
        return all_recipes.count()


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializerRead(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserReadSerializer(many=False, read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True, source='recipe_ingredients')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
                  'cooking_time', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_card.filter(recipe=recipe).exists()


class RecipeIngredientInWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = RecipeIngredientInWriteSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('tags', 'ingredients', 'author', 'name', 'text', 'image', 'cooking_time')
        read_only_fields = ('author',)

    def validate(self, attrs):
        ingredients = attrs.get('ingredients', [])
        ingredients_id = []
        if not attrs.get('cooking_time') > 0:
            raise serializers.ValidationError({"cooking_time": "cooking_time должно быть больше 0"})
        for elem in ingredients:
            current_id = elem.get('id')
            amount = elem.get('amount')
            if current_id not in ingredients_id:
                ingredients_id.append(current_id)
            else:
                raise serializers.ValidationError({"id": "ингредиент должен быть уникальным"})
            if not amount > 0:
                raise serializers.ValidationError({"amount": "значение amount должно быть > 0"})
        return attrs

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.add(*tags)
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient=ingredient.get('id'),
                recipe=recipe,
                amount=ingredient.get('amount'))
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.tags.add(*tags)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        for field, value in validated_data.items():
            setattr(instance, field, value)
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient=ingredient.get('id'),
                recipe=instance,
                amount=ingredient.get('amount'))
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializerRead(instance, context=context).data


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'cooking_time', 'image')

    def validate(self, attrs):
        user = self.context.get('request').user
        recipe = self.context.get('recipe')
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError({'error': 'рецепт уже в избранном'}, code=400)
        return attrs


class ShoppingCardSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingCard
        fields = ('id', 'name', 'cooking_time', 'image')

    def validate(self, attrs):
        user = self.context.get('request').user
        recipe = self.context.get('recipe')
        if ShoppingCard.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError({'error': 'рецепт уже в списке покупок'}, code=400)
        return attrs
