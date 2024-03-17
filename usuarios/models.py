from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from datetime import datetime
import logging
from django.utils import timezone
from django.utils.timezone import timedelta
from django.utils.translation import gettext_lazy as _
import uuid
from django import forms
from PIL import Image
import requests
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        # Não é mais necessário exigir um email para criar um usuário comum
        if email:
            email = self.normalize_email(email)
            user = self.model(email=email, username=username, **extra_fields)
        else:
            user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        # Superusuários ainda exigirão um email
        if not email:
            raise ValueError(_('Superuser must have an email.'))
        return self.create_user(username, email, password, **extra_fields, is_staff=True, is_superuser=True)




class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), blank=True, null=True, unique=False)
    username = models.CharField(_('usuario'), max_length=30, unique=True)
    saldo = models.CharField(max_length=700, blank=True, null=True, default=400)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_staff = models.BooleanField(_('staff status'), default=False)
    first_login = models.DateTimeField(_('first login'), null=True, blank=True)
    elapsed_time = models.CharField(max_length=9000, blank=True, null=True)
    largura_barra = models.IntegerField(default=0)



    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')