from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .services.cheapshark_service import CheapSharkService
from .models import Jogo, Biblioteca, Usuario
from rest_framework import status
from .services import cheapshark_service
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
import requests
from drf_spectacular.utils import extend_schema
from .serializers import AdicionarJogoSerializer, AlterarNotaSerializer, ExcluirJogoDaBibliotecaSerializer

class  ApiStatusView(APIView):
    def get(self, request):
        return Response({
            "status": "online",
            "message": "API esta rodando normalmente"
        })
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="titulo",
            description="Título do jogo para realizar a busca",
            required=True,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
        )
    ]
)
class BuscarJogosView(APIView):

    def get(self, request):

        titulo = request.query_params.get("titulo")

        if not titulo:
            return Response({"erro":"Informe um titulo de jogo na URL (exemplo: ?titulo=Elden Ring)"}, status=400)

        jogos = CheapSharkService.buscar_jogos_por_titulo(titulo)

        return Response(jogos)

@extend_schema(
    request=AdicionarJogoSerializer,
    responses={ 201: AdicionarJogoSerializer,}
)
class AdicionarJogoABiblioteca(APIView):

    def post(self, request):

        user_id = request.data.get("user_id")
        nome_jogo = request.data.get("nome_jogo")
        nota_jogo = request.data.get("nota_jogo")

        if not user_id:
            return Response({"erro": "O user_id é obrigatório"},tatus=status.HTTP_400_BAD_REQUEST)

        if not nome_jogo:
            return Response({"erro": "nome_jogo é obrigatório"},status=status.HTTP_400_BAD_REQUEST)

        if nota_jogo is None:
            return Response({"erro": "A nota_jogo é obrigatória"},status=status.HTTP_400_BAD_REQUEST)

        usuario = Usuario.objects.get(id=user_id)

        try:
            info_jogos = CheapSharkService.buscar_jogos_por_titulo(nome_jogo)

        except requests.RequestException:
            return Response({"erro": "A API externa parece não estar funcionando no momento"},status=status.HTTP_504_GATEWAY_TIMEOUT)

        if not info_jogos:
            return Response({"erro": "Nenhum jogo encontrado"},status=status.HTTP_404_NOT_FOUND )

        info_jogo = info_jogos[0]

        jogo, _ = Jogo.objects.get_or_create(id_externo=info_jogo["id_externo"],
            defaults={
                "nome": info_jogo["nome"],
                "imagem": info_jogo["imagem"],
                "metacritic_link": info_jogo["metacritic_link"],
                "preco": info_jogo["preco"]
            }
        )

        if Biblioteca.objects.filter(usuario=usuario,jogo=jogo).exists():

            return Response({"erro": "Esse jogo já está na biblioteca"},status=status.HTTP_400_BAD_REQUEST)

        Biblioteca.objects.create(usuario=usuario,jogo=jogo,nota=nota_jogo)

        return Response(
            {
                "mensagem": "Jogo adicionado à biblioteca!",
                "jogo": jogo.nome,
                "nota": nota_jogo,
                "preco": jogo.preco,
                "metacritic_link": jogo.metacritic_link
            },
            status=status.HTTP_201_CREATED
        )



class ListarBiblioteca(APIView):

    def get(self, request, user_id):

        if not Usuario.objects.filter(id=user_id).exists():
            return Response( {"erro": "O usuário não existe"},status=status.HTTP_404_NOT_FOUND)

        biblioteca = Biblioteca.objects.filter(usuario_id=user_id)

        jogos = []

        for item in biblioteca:
            jogos.append({
                "id": item.jogo.id,
                "id_externo": item.jogo.id_externo,
                "nome": item.jogo.nome,
                "sua-nota": item.nota,
                "imagem": item.jogo.imagem
            })

        return Response(jogos)
@extend_schema(
    request=ExcluirJogoDaBibliotecaSerializer,
    responses={201 : ExcluirJogoDaBibliotecaSerializer,}
)
class ExcluirJogoDaBiblioteca(APIView):

    def post(self, request):

        user_id = request.data.get("user_id")
        jogo_id = request.data.get("jogo_id")


        if not  Biblioteca.objects.filter(usuario_id = user_id, jogo_id=jogo_id).exists():
            return Response({"erro":"esse jogo não está na sua biblioteca"}, status=status.HTTP_404_NOT_FOUND)

        jogoDeletado = Biblioteca.objects.filter(usuario_id = user_id, jogo_id=jogo_id)

        jogoDeletado.delete()

        return Response({"Jogo excluido com sucesso"}, status=status.HTTP_200_OK)

@extend_schema(
    request=AlterarNotaSerializer,
    responses={
        201: AlterarNotaSerializer,
    }

)
class AlterarNotaDeJogo(APIView):

    def put(self,request):

        user_id = request.data.get("user_id")
        jogo_id = request.data.get("jogo_id")
        nota = request.data.get("nota")

        if not user_id:
            return Response({"erro": "user_id é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)
        if not jogo_id:
            return Response({"erro": "jogo_id é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)
        if nota is None:
            return Response({"erro": "a nota é obrigatória"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            biblioteca = Biblioteca.objects.get(usuario_id = user_id, jogo_id = jogo_id)

        except Biblioteca.DoesNotExist:
            return Response( {"erro": "Esse jogo não está na biblioteca"},status=status.HTTP_404_NOT_FOUND)

        biblioteca.nota = nota
        biblioteca.save()

        return Response({
            "mensagem": "Nota atualizada com sucesso!",
            "jogo": biblioteca.jogo.nome,
            "nota": biblioteca.nota
        })





        

        
        

        

        
  