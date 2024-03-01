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
def register(request):
    form = ClienteRegistrationForm()

    if request.method == 'POST':
        form = ClienteRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.set_unusable_password()
            user.save()

            login(request, user)  # Certifique-se de que esta linha está correta

            messages.success(request, 'Cadastro Realizado com sucesso!')
            return redirect('playlists')
        else:
            messages.error(request, form.errors)

    return render(request, 'core/registro.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']

        # Verificar se é um e-mail ou nome de usuário
        if '@' in username_or_email:
            # É um e-mail
            try:
                user = CustomUser.objects.get(email=username_or_email)
            except CustomUser.DoesNotExist:
                messages.error(request, "E-mail não encontrado.")
                return redirect('login')
        else:
            # É um nome de usuário
            try:
                user = CustomUser.objects.get(username=username_or_email)
            except CustomUser.DoesNotExist:
                messages.error(request, "Nome de usuário não encontrado.")
                return redirect('login')

        # Faz o login do usuário
        auth_login(request, user)
        messages.success(request, "Usuário logado com sucesso!")
        return redirect('playlists')
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})