from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .services.cheapshark_service import CheapSharkService
from .models import Jogo, Biblioteca, Usuario
from rest_framework import status

class  ApiStatusView(APIView):
    def get(self, request):
        return Response({
            "status": "online",
            "message": "API esta rodando normalmente"
        })

class BuscarJogosView(APIView):

    def get(self, request):

        titulo = request.query_params.get("titulo")

        if not titulo:
            return JsonResponse({"erro":"Informe um titulo de jogo"}, status=400)

        jogos = CheapSharkService.buscar_jogos_por_titulo(titulo)

        return JsonResponse(jogos, safe=False)


class AdicionarJogoABiblioteca(APIView): 
    def post(self, request): 
        id_jogo = request.data.get("id_externo") 
        user_id = request.data.get("user_id")
        nome_jogo = request.data.get("nome_jogo")

        if not id_jogo:
            return Response( {"erro": "O id_externo é obrigatório"}, status=status.HTTP_400_BAD_REQUEST ) 
        if not user_id:
            return Response( {"erro": "O user_id é obrigatório"}, status=status.HTTP_400_BAD_REQUEST ) 
        if not nome_jogo:
            return Response( {"erro": "nome_jogo é obrigatório"}, status=status.HTTP_400_BAD_REQUEST ) 

        usuario = Usuario.objects.get(id=user_id)


        jogo, criado = Jogo.objects.get_or_create(id_externo=id_jogo,defaults={ "nome": nome_jogo })


        if Biblioteca.objects.filter( usuario=usuario, jogo=jogo ).exists():
            return Response( {"erro": "Esse jogo já está na biblioteca"}, status=status.HTTP_400_BAD_REQUEST )

        Biblioteca.objects.create(usuario = usuario, jogo=jogo)

        return Response(
            {
                "mensagem": "Jogo adicionado à biblioteca!",
                "jogo": jogo.nome
            },
            status=status.HTTP_201_CREATED
        )

        

        
        

        

        
  