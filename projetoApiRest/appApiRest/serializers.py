from rest_framework import serializers


class AdicionarJogoSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    nome_jogo = serializers.CharField(max_length=100)
    nota_jogo = serializers.IntegerField(min_value=0, max_value=10)


class AdicionarJogoResponseSerializer(serializers.Serializer):
    mensagem = serializers.CharField()
    jogo = serializers.CharField()
    nota = serializers.IntegerField()

class AlterarNotaSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    jogo_id = serializers.IntegerField()
    nota = serializers.IntegerField(min_value=0,max_value=10)

class AlterarNotaResponseSerializer(serializers.Serializer):
    mensagem = serializers.CharField()
    jogo = serializers.CharField()


class ExcluirJogoDaBibliotecaSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    jogo_id = serializers.IntegerField()

class CriarNovoUsuarioSerializer(serializers.Serializer):
    nome = serializers.CharField()
    email = serializers.EmailField()
    senha = serializers.CharField()
    senha_repetida = serializers.CharField()