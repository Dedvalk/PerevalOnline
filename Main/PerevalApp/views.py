from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Pereval, Coords
from .serializers import PerevalSerializer, CoordsSerializer


class PerevalViewset(CreateAPIView):

    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

    def create(self, request, *args, **kwargs):
        serializer = PerevalSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            response_data = {
                "status": 200,
                "message": "Успешно отправлено.",
                "id": instance.id
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except ValidationError as e:
            response_data = {
                "status": 400,
                "message": e.detail,
                "id": None
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response_data = {
                "status": 500,
                "message": str(e),
                "id": None
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CoordsViewSet(viewsets.ModelViewSet):

    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer