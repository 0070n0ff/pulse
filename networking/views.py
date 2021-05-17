from django.db.models import QuerySet
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Network
from .serializers import NetworkSerializer,NetworkDetailSerializer


# Create your views here.
class NetworkList(APIView):
    def get(self, request):
        networks: QuerySet[Network] =Network.objects.filter(is_active=True)
        serializer = NetworkSerializer(networks, many=True)
        return Response(serializer.data)

class NetworkDetailView(APIView):
    def get(self, request,pk):
        networks = Network.objects.get(id=pk, is_active=True)
        serializer = NetworkDetailSerializer(networks)
        return Response(serializer.data)
