from django.contrib import admin
from .models import Usuario, Jogo, Biblioteca

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email')

@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_externo', 'nome')

@admin.register(Biblioteca)
class BibliotecaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'jogo')
 
