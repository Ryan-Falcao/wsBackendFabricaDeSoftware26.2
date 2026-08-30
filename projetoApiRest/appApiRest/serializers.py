from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import Usuario


class AdicionarJogoSerializer(serializers.Serializer):

    nome_jogo = serializers.CharField(max_length=100)
    nota_jogo = serializers.DecimalField( min_value=0,max_value=10,max_digits=3, decimal_places=1)


class AdicionarJogoResponseSerializer(serializers.Serializer):
    mensagem = serializers.CharField()
    jogo = serializers.CharField()
    nota = serializers.DecimalField( min_value=0,max_value=10,max_digits=3, decimal_places=1)

class AlterarNotaSerializer(serializers.Serializer):
    jogo_id = serializers.IntegerField()
    nota = serializers.DecimalField(max_digits=3,decimal_places=1,min_value=0,max_value=10)

class AlterarNotaResponseSerializer(serializers.Serializer):
    mensagem = serializers.CharField()
    jogo = serializers.CharField()


class ExcluirJogoDaBibliotecaSerializer(serializers.Serializer):

    jogo_id = serializers.IntegerField()

class CriarNovoUsuarioSerializer(serializers.Serializer):
    nome = serializers.CharField()
    email = serializers.EmailField()
    senha = serializers.CharField()
    senha_repetida = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        senha = attrs["senha"]

        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError( "Email ou senha inválidos.")

        if not check_password(senha, usuario.senha):
            raise serializers.ValidationError("Email ou senha inválidos.")

        refresh = RefreshToken()

        refresh["usuario_id"] = usuario.id
        refresh["nome"] = usuario.nome
        refresh["email"] = usuario.email

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "usuario": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
            }
        }

class OfertaFiltroSerializer(serializers.Serializer): 
    store_id = serializers.CharField(required=False) 
    page_number = serializers.IntegerField(required=False, min_value=0) 
    page_size = serializers.IntegerField(required=False, min_value=1, max_value=60) 
    sort_by = serializers.ChoiceField( 
        required=False, 
        choices=[ 
            "DealRating", 
            "Title", 
            "Savings", 
            "Price", 
            "Metacritic", 
            "Reviews", 
            "ReviewCount", 
            "Release", 
            "Store", 
            "Recent", 
            ] ) 
    desc = serializers.BooleanField(required=False) 
    lower_price = serializers.FloatField(required=False, min_value=0) 
    upper_price = serializers.FloatField(required=False, min_value=0) 
    metacritic = serializers.IntegerField( required=False, min_value=0, max_value=100 ) 
    steam_rating = serializers.IntegerField( required=False, min_value=0, max_value=100 ) 
    minimum_review_count = serializers.IntegerField( required=False, min_value=0 ) 
    max_age = serializers.IntegerField( required=False, min_value=1, max_value=2500 ) 
    steam_app_id = serializers.CharField(required=False) 
    title = serializers.CharField(required=False) 
    exact = serializers.BooleanField(required=False) 
    aaa = serializers.BooleanField(required=False) 
    steamworks = serializers.BooleanField(required=False) 
    on_sale = serializers.BooleanField(required=False)