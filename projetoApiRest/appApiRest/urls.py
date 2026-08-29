from django.urls import path
from .views import ApiStatusView
from .views import BuscarJogosView

urlpatterns = [
    path('status/', ApiStatusView.as_view(), name='api-status'),
    path('jogos/buscar/', BuscarJogosView.as_view()),
]