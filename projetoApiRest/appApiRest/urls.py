from django.urls import path
from .views import ApiStatusView, BuscarJogosView, AdicionarJogoABiblioteca, ListarBiblioteca, ExcluirJogoDaBiblioteca, AlterarNotaDeJogo
from .views import CriarNovoUsuario, LoginView
from .views import (ApiStatusView, BuscarJogosView,AdicionarJogoABiblioteca,ListarBiblioteca,ExcluirJogoDaBiblioteca,AlterarNotaDeJogo,CriarNovoUsuario,LoginView,)


urlpatterns = [
    path('status/', ApiStatusView.as_view(), name='api-status'),
    path('jogos/buscar/', BuscarJogosView.as_view()),
    path('biblioteca/adicionar/jogo', AdicionarJogoABiblioteca.as_view()),
    path('biblioteca/me', ListarBiblioteca.as_view()),
    path('biblioteca/alterar/nota', AlterarNotaDeJogo.as_view()),
    path('biblioteca/jogo/<int:jogo_id>/', ExcluirJogoDaBiblioteca.as_view()),
    path('usuario/cadastrar/', CriarNovoUsuario.as_view()),
    path('usuario/login/', LoginView.as_view()),
]
