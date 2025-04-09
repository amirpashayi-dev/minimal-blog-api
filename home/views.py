from rest_framework.response import Response
from rest_framework.views import APIView


class MainPageView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to Minimal Blog API ✌️"})