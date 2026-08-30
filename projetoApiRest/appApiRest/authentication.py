from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from drf_spectacular.extensions import OpenApiAuthenticationExtension

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


class UsuarioJWTAuthenticationScheme(OpenApiAuthenticationExtension):

    target_class = 'appApiRest.authentication.UsuarioJWTAuthentication'
    name = 'BearerAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }