from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('registro/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


 





    

    # Aqui estamos definindo a rota para a sua view home
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)