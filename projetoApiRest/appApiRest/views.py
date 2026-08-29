from django.shortcuts import render
from rest_framework.views import APIView
from requests import Response

class  ApiStatusView(APIView):
    def get(self, request):
        return Response({
            "status": "online",
            "message": "API esta rodando normalmente"
        })
