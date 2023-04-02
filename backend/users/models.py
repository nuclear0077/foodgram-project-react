from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.TextChoices):
    USER = 'user'
    ADMIN = 'admin'


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        verbose_name='Firstname'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Lastname'
    )
    username = models.CharField(
        max_length=150,
        verbose_name='Username',
        unique=True
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254
    )
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER,

    )

    @property
    def is_admin(self):
        return (
            self.role == Roles.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_user(self):
        return self.role == Roles.USER

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_username_email'
            )
        ]