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

    data = serializers.URLField()

    class Meta:
        model = Images
        fields = ['data', 'title']

class PerevalSerializer(WritableNestedModelSerializer):

    coords = CoordsSerializer()
    level = LevelsSerializer()
    user = UsersSerializer()
    images = ImagesSerializer(many=True)
    status = serializers.CharField(read_only=True)
    add_time = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S', read_only=True)

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
                  'images',
                  'status'
                  )

    def create(self, validated_data, **kwargs):

        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        user, created = Users.objects.get_or_create(**user)

        coords = Coords.objects.create(**coords)
        level = Levels.objects.create(**level)
        pereval = Pereval.objects.create(**validated_data, user=user, coords=coords, level=level, status='new')

        for image in images:
            data = image.pop('data')
            title = image.pop('title')
            Images.objects.create(title=title, data=data, pereval=pereval)

        return pereval