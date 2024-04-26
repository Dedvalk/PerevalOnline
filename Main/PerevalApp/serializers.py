from rest_framework import serializers

from .models import Pereval, Coords


class PerevalSerializer(serializers.ModelSerializer):
    class Meta:

        model = Pereval
        fields = ('title',
                  'beauty_title',
                  'other_title',
                  'connect',
                  'add_time',
                  'user',
                  'coords',
                  'level'
                  )

class CoordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']