from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .services.cheapshark_service import CheapSharkService
from .models import Jogo, Biblioteca, Usuario
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
import requests
from drf_spectacular.utils import extend_schema
from .serializers import AdicionarJogoSerializer, AlterarNotaSerializer, ExcluirJogoDaBibliotecaSerializer, CriarNovoUsuarioSerializer,  LoginSerializer, OfertaFiltroSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import IsAuthenticated

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

@extend_schema(request=AdicionarJogoSerializer,responses={ 201: AdicionarJogoSerializer,})
class AdicionarJogoABiblioteca(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = AdicionarJogoSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

        usuario = request.user
        nome_jogo = serializer.validated_data["nome_jogo"]
        nota_jogo = serializer.validated_data["nota_jogo"]

    
        if not nome_jogo:
            return Response({"erro": "nome_jogo é obrigatório"},status=status.HTTP_400_BAD_REQUEST)

        if nota_jogo is None:
            return Response({"erro": "A nota_jogo é obrigatória"},status=status.HTTP_400_BAD_REQUEST)

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
                "imagem": jogo.imagem,
            },
            status=status.HTTP_201_CREATED
        )



class ListarBiblioteca(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        usuario = request.user

        if not Usuario.objects.filter(id=usuario.id).exists():
            return Response( {"erro": "O usuário não existe"},status=status.HTTP_404_NOT_FOUND)

        biblioteca = Biblioteca.objects.filter(usuario_id=usuario.id)

        jogos = []

        for item in biblioteca:
            jogos.append({
                "id": item.jogo.id,
                "id_externo": item.jogo.id_externo,
                "nome": item.jogo.nome,
                "sua-nota": item.nota,
                "imagem": item.jogo.imagem
            })

        if jogos == []:
            return Response(
                {"mensagem":"Você ainda não possui nenhum jogo adicionado"}
            )


        return Response(jogos)


class ExcluirJogoDaBiblioteca(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, jogo_id):

        usuario = request.user

        if not Biblioteca.objects.filter(usuario_id=usuario.id,jogo_id=jogo_id).exists():
            return Response({"erro": "Esse jogo não está na sua biblioteca"},status=status.HTTP_404_NOT_FOUND)

        Biblioteca.objects.filter(usuario_id=usuario.id,jogo_id=jogo_id).delete()

        return Response({"mensagem": "Jogo excluído com sucesso"},status=status.HTTP_200_OK)
    
@extend_schema(request=AlterarNotaSerializer,responses={201: AlterarNotaSerializer,})
class AlterarNotaDeJogo(APIView):

    

    permission_classes = [IsAuthenticated]

    def put(self,request):

        serializer = AlterarNotaSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        usuario = request.user
        jogo_id = serializer.validated_data["jogo_id"]
        nota = serializer.validated_data["nota"]

        if not jogo_id:
            return Response({"erro": "jogo_id é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)
        if nota is None:
            return Response({"erro": "a nota é obrigatória"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            biblioteca = Biblioteca.objects.get(usuario_id = usuario.id, jogo_id = jogo_id)

        except Biblioteca.DoesNotExist:
            return Response( {"erro": "Esse jogo não está na biblioteca"},status=status.HTTP_404_NOT_FOUND)

        biblioteca.nota = nota
        biblioteca.save()

        return Response({
            "mensagem": "Nota atualizada com sucesso!",
            "jogo": biblioteca.jogo.nome,
            "nota": biblioteca.nota
        })

@extend_schema(request=CriarNovoUsuarioSerializer,responses={201 : CriarNovoUsuarioSerializer})
class CriarNovoUsuario(APIView):

    def post(self,request):

        serializer = CriarNovoUsuarioSerializer(data=request.data)

        if not serializer.is_valid():
            return Response( serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        nome = serializer.validated_data["nome"]
        email = serializer.validated_data["email"]
        senha = serializer.validated_data["senha"]
        senhaRepetida = serializer.validated_data["senha_repetida"]

        if not email:
            return Response({"erro":"o campo email é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)
        if not senha:
            return Response({"erro":"o campo senha é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)
        if not senhaRepetida:
            return Response({"erro":"o campo senha-repetida é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        
        if Usuario.objects.filter(email = email).exists():
            return Response({"erro":"Esse email já possui conta"}, status=status.HTTP_400_BAD_REQUEST)

        if  senha != senhaRepetida:
            return Response({"erro": "as duas senhas devem ser iguais"}, status=status.HTTP_400_BAD_REQUEST)

        senha_hash = make_password(senha)

        usuario = Usuario.objects.create(nome = nome, email=email, senha=senha_hash)

        return Response({
            "mensagem":"Conta criada com sucesso",
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
            }, status=status.HTTP_201_CREATED)

@extend_schema(request=LoginSerializer,responses={201: LoginSerializer})
class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        

        if serializer.is_valid():
            return Response(serializer.validated_data,status=status.HTTP_200_OK)

        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)



class BuscarOfertasView(APIView):

    @extend_schema(
        parameters=[OfertaFiltroSerializer]
    )
    def get(self, request):

        serializer = OfertaFiltroSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        try:
            ofertas = CheapSharkService.buscar_ofertas(**serializer.validated_data)

            return Response({
                "Observação":"Os dados apresentados representam um histórico de ofertas encontradas pela API. Algumas promoções podem não estar mais ativas ou podem ter sofrido alterações de preço desde a última atualização.",
                "Ofertas":ofertas
                })

        except requests.RequestException:
            return Response({"erro": "A API externa parece não estar funcionando no momento"},status=status.HTTP_504_GATEWAY_TIMEOUT)








        

        
        

        

        
  