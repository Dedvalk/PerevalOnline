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
    status = serializers.CharField(default='new', initial='new')
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
        pereval = Pereval.objects.create(**validated_data, user=user, coords=coords, level=level)

        for image in images:
            data = image.pop('data')
            title = image.pop('title')
            Images.objects.create(title=title, data=data, pereval=pereval)

        return pereval

    def validate(self, data):

        if self.instance is not None:
            user = data.get('user')
            instance = self.instance.user
            if any(user[attr] != getattr(instance, attr) for attr in ('fam', 'name', 'otc', 'email', 'phone')):
                raise serializers.ValidationError('Изменять данные пользователя запрещено.')

        return data


    def update(self, instance, validated_data):

        user = validated_data.pop('user', None)
        coords = validated_data.pop('coords', None)
        level = validated_data.pop('level', None)
        images = validated_data.pop('images', None)
        new_user, created = Users.objects.get_or_create(**user)
        new_coords, created = Coords.objects.get_or_create(**coords)
        new_level, created = Levels.objects.get_or_create(**level)

        instance.title = validated_data.get('title', instance.title)
        instance.beauty_title = validated_data.get('beauty_title', instance.beauty_title)
        instance.other_titles = validated_data.get('other_titles', instance.other_titles)
        instance.connect = validated_data.get('connect', instance.connect)
        instance.status = validated_data.get('status', instance.status)
        instance.user = new_user or instance.user
        instance.coords = new_coords or instance.coords
        instance.level = new_level or instance.level

        for image in images:
            print(image)
            data = image.pop('data')
            title = image.pop('title')
            new_image, created = Images.objects.get_or_create(title=title, data=data, pereval=instance)

        instance.save()

        return instance