from django.urls import path
from .views import ApiStatusView, BuscarJogosView, AdicionarJogoABiblioteca


urlpatterns = [
    path('status/', ApiStatusView.as_view(), name='api-status'),
    path('jogos/buscar/', BuscarJogosView.as_view()),
    path('biblioteca/adicionar/', AdicionarJogoABiblioteca.as_view()),
]