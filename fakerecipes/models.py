from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from s3direct.fields import S3DirectField


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        user = self.create_user(
            username,
            password,
            **extra_fields,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class AppUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='username', unique=True, max_length=32)
    email = models.EmailField(verbose_name='email address', unique=True)
    name = models.CharField(verbose_name='name', max_length=32)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'name']

    objects = UserManager()

    def __str__(self):
        return self.username

class Ingredient(models.Model):
    name = models.CharField(verbose_name='name', max_length=32)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    class Meta:
        ordering = ('created_at',)
    DifficultyTypes = models.TextChoices('DifficultyType', 'Easy Medium Hard')
    title= models.CharField('title', max_length=128)
    description= models.TextField('description', max_length=10240)
    difficulty=models.CharField('difficulty', blank=False, choices=DifficultyTypes.choices, max_length=16)
    created_by= models.ForeignKey(AppUser, verbose_name='created by', on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredients')
    image = S3DirectField(dest="main", verbose_name="image")

