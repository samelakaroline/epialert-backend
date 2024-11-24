# epialert/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to EpiAlert API")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Inclui as rotas do app `users` para login e registro
    path('', home_view),  # Adiciona uma rota para a URL raiz
    path('dashboards/', include('dashboards.urls')),  # Rotas do app `dashboards`
    path('alerts/', include('alerts.urls')),  # Rotas do app `alerts`
]
