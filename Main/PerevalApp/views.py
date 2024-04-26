from django.shortcuts import render
from rest_framework import viewsets

from .models import Pereval, Coords
from .serializers import PerevalSerializer, CoordsSerializer


class PerevalViewset(viewsets.ModelViewSet):

    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

class CoordsViewSet(viewsets.ModelViewSet):

    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer