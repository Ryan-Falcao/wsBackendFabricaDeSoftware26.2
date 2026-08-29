from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .services.cheapshark_service import CheapSharkService

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