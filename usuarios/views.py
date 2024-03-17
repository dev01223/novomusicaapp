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



# Create your views here.
# Create your views here.
# Função unificada para registro e login
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # Tenta buscar o usuário pelo username
        try:
            user = CustomUser.objects.get(username=username)
            # Se o usuário existir, tenta fazer o login
            password = request.POST.get('password')  # Garanta que este campo exista em seu formulário
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Usuário logado com sucesso!")
                return redirect('playlists')
            else:
                messages.error(request, "Senha incorreta.")
                return redirect('register')
        except CustomUser.DoesNotExist:
            # Se o usuário não existir, tenta criar um novo
            form = ClienteRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_unusable_password()  # Assumindo que não está usando senha para autenticar
                user.save()
                # Faz login do novo usuário
                auth_login(request, user)
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('playlists')
            else:
                messages.error(request, form.errors)
    else:
        form = ClienteRegistrationForm()

    return render(request, 'core/registro.html', {'form': form})