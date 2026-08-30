from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.nome

class Biblioteca(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='bibliotecas')
    jogo = models.ForeignKey('Jogo', on_delete=models.CASCADE, related_name='usuarios')
    nota = models.IntegerField(null=True,blank=True,  validators=[MinValueValidator(0),MaxValueValidator(10)])

    def __str__(self):
         return f"{self.usuario.nome} - {self.jogo.nome}"

class Jogo(models.Model):
    id_externo = models.IntegerField(unique=True)
    nome = models.CharField(max_length=100)
    imagem = models.URLField(null=True, blank=True)
    metacritic_link = models.CharField(max_length=200, null=True, blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    metacritic_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nome