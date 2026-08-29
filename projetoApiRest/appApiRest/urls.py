from django.urls import path
from .views import ApiStatusView, BuscarJogosView, AdicionarJogoABiblioteca, ListarBiblioteca, ExcluirJogoDaBiblioteca, AlterarNotaDeJogo
from .views import CriarNovoUsuario


urlpatterns = [
    path('status/', ApiStatusView.as_view(), name='api-status'),
    path('jogos/buscar/', BuscarJogosView.as_view()),
    path('biblioteca/adicionar/', AdicionarJogoABiblioteca.as_view()),
    path('biblioteca/<int:user_id>/', ListarBiblioteca.as_view()),
    path('biblioteca/alterar/nota', AlterarNotaDeJogo.as_view()),
    path('biblioteca/<int:user_id>/jogo/<int:jogo_id>/', ExcluirJogoDaBiblioteca.as_view()),
    path('usuario/cadastrar/', CriarNovoUsuario.as_view()),
]
