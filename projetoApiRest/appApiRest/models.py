from django.db import models

class Usuario(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Biblioteca(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='bibliotecas')

    def __str__(self):
        return f'Biblioteca de {self.usuario.name}'