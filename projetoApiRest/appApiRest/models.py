from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Biblioteca(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='bibliotecas')
    jogo = models.ForeignKey('Jogo', on_delete=models.CASCADE, related_name='usuarios')

    def __str__(self):
         return f"{self.usuario.nome} - {self.jogo.nome}"

class Jogo(models.Model):
    id_externo = models.IntegerField(unique=True)
    nome = models.CharField(max_length=100)
    imagem = models.CharField(max_length=100)

    def __str__(self):
        return self.nome