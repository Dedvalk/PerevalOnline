from rest_framework import serializers

from .models import Pereval, Coords, Levels, Users, Images
from drf_writable_nested import WritableNestedModelSerializer

class CoordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Levels
        fields = ['winter', 'summer', 'autumn', 'spring']


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['email', 'fam', 'name', 'otc', 'phone']

class ImagesSerializer(serializers.ModelSerializer):

    #data = serializers.CharField()
    class Meta:
        model = Images
        fields = ['data', 'title']

class PerevalSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):

    coords = CoordsSerializer()
    level = LevelsSerializer()
    user = UsersSerializer()
    images = ImagesSerializer(many=True)

    class Meta:

        model = Pereval
        fields = ('title',
                  'beauty_title',
                  'other_titles',
                  'connect',
                  'add_time',
                  'user',
                  'coords',
                  'level',
                  'images'
                  )

