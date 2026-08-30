from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import Usuario

class UsuarioJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        usuario_id = validated_token.get("usuario_id")

        if not usuario_id:
            raise AuthenticationFailed("Token não possui usuario_id")

        try:
            return Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            raise AuthenticationFailed("Usuário não encontrado")