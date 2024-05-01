from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Pereval, Coords
from .serializers import PerevalSerializer, CoordsSerializer
from django_filters import rest_framework


class PerevalViewset(viewsets.ModelViewSet):

    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = [
        'user__email'
    ]

    def create(self, request, *args, **kwargs):

        serializer = PerevalSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            response_data = {
                'status': status.HTTP_200_OK,
                'message': 'Успешно отправлено.',
                'id': instance.id
            }
            return Response(response_data)

        except ValidationError as e:
            response_data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': e.detail,
                'id': None
            }
            return Response(response_data)

        except Exception as e:
            response_data = {
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e),
                'id': None
            }
            return Response(response_data)


    def partial_update(self, request, *args, **kwargs):

        pereval = self.get_object()
        if pereval.status == 'new':
            serializer = PerevalSerializer(pereval, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                response_data = {
                    'status': status.HTTP_200_OK,
                    'message': 'Успешно изменено.',
                    'state': 1
                }
                return Response(response_data)

            except ValidationError as e:
                response_data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': e.detail,
                    'state': 0
                }
                return Response(response_data)

        else:
            response_data = {
                'message': 'Статус запрещает изменение',
                'state': 0
            }
            return Response(response_data)

class CoordsViewSet(viewsets.ModelViewSet):

    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer