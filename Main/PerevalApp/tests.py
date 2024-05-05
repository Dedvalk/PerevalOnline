from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.utils import json

from .models import Users, Coords, Levels, Pereval
from .serializers import PerevalSerializer

class SubmitDataTestCase(APITestCase):

    @classmethod
    def setUp(self):

        userdata1 = {
            'email': 'testuser1@test.com',
            'fam': 'testuser1',
            'name': 'testuser1',
            'otc': 'testuser1',
            'phone': '11111111111'
        }
        userdata2 = {
            'email': 'testuser2@test.com',
            'fam': 'testuser2',
            'name': 'testuser2',
            'otc': 'testuser2',
            'phone': '22222222222'
        }
        perevaldata1 = {
            'title': 'pereval1',
            'beauty_title': 'pereval1',
            'other_titles': 'pereval1'
        }
        coordsdata = {
            'latitude': '11.11',
            'longitude': '11.11',
            'height': '1111'
        }
        leveldata = {
            'spring': '1А',
            'summer': '',
            'autumn': '',
            'winter': '1Б'
        }
        testuser1 = Users.objects.create(**userdata1)
        testuser2 = Users.objects.create(**userdata2)
        coords1 = Coords.objects.create(**coordsdata)
        coords2 = Coords.objects.create(latitude=22.22, longitude=22.22, height=2222)
        coords3 = Coords.objects.create(latitude=33.33, longitude=33.33, height=3333)
        level1 = Levels.objects.create(**leveldata)
        level2 = Levels.objects.create(spring='', summer='2А', autumn='2Б', winter='')
        self.pereval1 = Pereval.objects.create(**perevaldata1, user=testuser1, coords=coords1, level=level1)
        self.pereval2 = Pereval.objects.create(title='pereval2', beauty_title='pereval2', other_titles='pereval2',
                                          user=testuser2, coords=coords2, level=level2)
        self.pending_pereval = Pereval.objects.create(title='pereval3', beauty_title='pereval3', other_titles='pereval3',
                                          user=testuser1, coords=coords3, level=level1, status='pending')
        self.patch_data = {
            "beauty_title": "pereval0",
            "title": "pereval0",
            "other_titles": "pereval0",
            "connect": "",
            "user": userdata1,
            "coords": coordsdata,
            "level": leveldata,
            "images": []
        }
        self.patch_user = {
            **perevaldata1,
            "connect": "",
            "user": userdata2,
            "coords": coordsdata,
            "level": leveldata,
            "images": []
        }
        self.patch_pended = {
            "beauty_title": "pereval0",
            "title": "pereval0",
            "other_titles": "pereval0",
            "connect": "",
            "user": userdata1,
            "coords": coordsdata,
            "level": leveldata,
            "images": []
        }

    def test_get_object_list(self):

        expected = PerevalSerializer([self.pereval1, self.pereval2, self.pending_pereval], many=True).data
        url = reverse('pereval-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data, expected)

    def test_get_object_by_id(self):

        expected = PerevalSerializer(self.pereval1).data
        url = reverse('pereval-detail', args=(self.pereval1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_filter_object_by_user_mail(self):

        response = self.client.get('/api/v1/submitData/?user__email=testuser2@test.com' )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['name'], 'testuser2')

    def test_patch_object(self):

        url = reverse('pereval-detail', args=(self.pereval1.id,))
        response = self.client.patch(url, self.patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Успешно изменено.')
        self.assertEqual(response.data['state'], 1)

    def test_patch_object_user(self):

        url = reverse('pereval-detail', args=(self.pereval1.id,))
        response = self.client.patch(url, self.patch_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message']['non_field_errors'][0], 'Изменять данные пользователя запрещено.')
        self.assertEqual(response.data['state'], 0)

    def test_patch_pending_object(self):

        url = reverse('pereval-detail', args=(self.pending_pereval.id,))
        response = self.client.patch(url, self.patch_pended, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Статус запрещает изменение')
        self.assertEqual(response.data['state'], 0)