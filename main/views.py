from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from usuarios.models import *
import json




def home_view(request):
   # if request.user.is_authenticated:
   #     now = timezone.now()
   #     if request.user.first_login:
    #        days_since_first_login = (now - request.user.first_login).days
    #        if days_since_first_login < 1:
    #            return render(request, 'core/playlists1.html')
    #        elif days_since_first_login < 7:
    #            return render(request, 'core/playlists2.html')
    #        else:
    #            return render(request, 'core/playlists.html')
    #    else:
    #        # Adicione um retorno aqui para cobrir a situação onde request.user.first_login é None
    #        return render(request, 'core/playlists.html')
    #else:
        return render(request, 'core/registro.html')

def update_saldo(request):
    user = request.user
    user.saldo += 5
    user.save()
    return JsonResponse({'status': 'success'})

def playlists(request):
    if request.user.is_authenticated:
        user = request.user
        now = timezone.now()

        # Verifica se é o primeiro login atualizando o campo first_login
        if user.first_login is None:
            user.first_login = now
            user.save(update_fields=['first_login'])
            template_name = 'core/playlists.html'  # Template para o primeiro login
        else:
            template_name = 'core/playlists2.html'  # Template para logins subsequentes

        context = {
            'user': user,
            'first_login': user.first_login,
        }
        return render(request, template_name, context)
    else:
        return render(request, 'core/playlists2.html')

def bonus(request):
    
    user = request.user
    if user.is_authenticated:
        saldo_atual = float(user.saldo) if user.saldo else 0
        saldo_atualizado = saldo_atual + 50
        user.saldo = str(saldo_atualizado)
        user.save()
        # Agora o usuário tem seu saldo atualizado
    # Resto da sua lógica...
    return render(request, 'core/novoSaque.html')




@csrf_exempt
def update_data(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            data = json.loads(request.body)

            # Atualiza os campos com os dados recebidos
            user.elapsed_time = data.get('elapsedTime', user.elapsed_time)
            user.saldo = data.get('saldoUser', user.saldo)

            # Converter largura_barra para número
            largura_barra_str = data.get('larguraBarra', str(user.largura_barra)).replace('%', '')
            try:
                user.largura_barra = float(largura_barra_str)
            except ValueError:
                return JsonResponse({'status': 'invalid data for larguraBarra'}, status=400)

            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'user not authenticated'}, status=401)
    else:
        return JsonResponse({'status': 'invalid request'}, status=400)


def saque(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user

    context = {
        'user':user
    }

    return render(request, 'core/saqueNovo12.html', context)


def main_page(request):
    return render(request, 'core/main_page.html')


def loading(request):
    return render(request, 'core/loading.html')


def novaPlaylist(request):
    return render(request, 'core/novaPlaylist.html')


def prevideo(request):
    return render(request, 'core/prevideo.html')

def vsl(request):
    return render(request, 'core/vsl.html')

def sertanejo(request):
    return render(request, 'core/sertanejo.html')

def funk(request):
    return render(request, 'core/funk.html')


def rap(request):
    return render(request, 'core/rap.html')


def sacar_saldo(request):
    user = request.user
    user.saldo = 0
    user.save()
    return redirect('playlists')
