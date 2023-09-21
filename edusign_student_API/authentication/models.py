from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from enum import Enum

class UserStatus(Enum):
    STUDENT = 'student'
    INTERVENING = 'intervening'
    ADMINISTRATOR = 'administrator'

class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None, status=UserStatus.STUDENT.value, **extra_fields):
        if not email:
            raise ValueError('L\'adresse email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, status=status, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='email_address')
    first_name = models.CharField(max_length=100, verbose_name='first_name')
    last_name = models.CharField(max_length=100, verbose_name='last_name')
    status = models.CharField(max_length=15, choices=[(status.value, status.value) for status in UserStatus], default=UserStatus.STUDENT.value, verbose_name='user_status')
    promotion = models.ForeignKey(
        'Promotion', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='related_promotion',
        related_name='users_s_promotion'
    )
    is_active = models.BooleanField(default=True, verbose_name='is_user_active')
    is_staff = models.BooleanField(default=False, verbose_name='is_user_staff')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Promotion(models.Model):
    name = models.CharField(max_length=128, verbose_name='promotion_name')

    def __str__(self):
        return self.name
