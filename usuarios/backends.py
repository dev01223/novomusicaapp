from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned
from .models import CustomUser

class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            return None


from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class CPFBackend(BaseBackend):
    def authenticate(self, request, username=None, **kwargs):
        UserModel = get_user_model()
        if not username:
            return None
        try:
            user = UserModel.objects.get(username=username)
            # Aqui, assumimos que o usuário é válido apenas com o CPF
            # Como não há senha, retornamos o usuário diretamente
            return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None