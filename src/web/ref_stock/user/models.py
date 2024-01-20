from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):

        if not username:
            raise ValueError(_("You must provide a username"))
        if not email:
            raise ValueError(_("You must provide an email"))

        username = AbstractBaseUser.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') != True:
            raise ValueError(_('Superuser must be assigned to is_staff=True'))
        if extra_fields.get('is_superuser') != True:
            raise ValueError(_('Superuser must be assigned to is_superuser=True'))
        
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return self.username
