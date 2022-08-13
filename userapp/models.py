from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from location.models import State, LocalGovernmentArea
from PIL import Image


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_active, is_staff, is_superuser, **extra_fields):
        if not username:
            raise ValueError('a username is required')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_active=is_active, is_staff=is_staff,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        return self._create(username, email, password, is_active=True, is_staff=False, is_superuser=False,
                            **extra_fields)

    def create_superuser(self, username, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self._create_user(username, email, password, **other_fields)


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(max_length=250, unique=True)
    username = models.CharField(max_length=250, unique=True)
    first_name = models.CharField(max_length=250, unique=False)
    last_name = models.CharField(max_length=250, unique=False)
    signup_date = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    user_image = models.ImageField(null=True, upload_to="profile_photo's")
    address = models.CharField(max_length=250, unique=False)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)
    local_government_area = models.ForeignKey(LocalGovernmentArea, on_delete=models.SET_NULL, blank=True, null=True)
    mobile_no = models.IntegerField(null=True)
    certificate_upload = models.FileField(null=True, upload_to='certificates')
    specialization = models.CharField(max_length=50, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


    def __str__(self):
        return self.username
