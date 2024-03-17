from django.shortcuts import render
from usuarios.forms import *
from .models import *
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
import logging
import googlemaps
from django.contrib import messages
import logging
from django.contrib.auth import authenticate, login as auth_login

# Configura o logger para a sua aplicação
logger = logging.getLogger(__name__)


# Create your views here.
# Create your views here.
# Função unificada para registro e login
# Função unificada para registro e login
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            # Tenta logar o usuário diretamente
            auth_login(request, user, backend='usuarios.backends.CPFBackend')  # Use o backend de autenticação sem senha
            messages.success(request, "Usuário logado com sucesso!")
            return redirect('playlists')
        except CustomUser.DoesNotExist:
            form = ClienteRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_unusable_password()  # Não usar senha para autenticar
                user.save()
                # Loga o novo usuário imediatamente após o registro
                auth_login(request, user, backend='usuarios.backends.CPFBackend')  # Especifique o backend aqui também
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('playlists')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        logger.error(f'Erro no campo {field}: {error}')
                messages.error(request, form.errors)
    else:
        form = ClienteRegistrationForm()

    return render(request, 'core/registro.html', {'form': form})