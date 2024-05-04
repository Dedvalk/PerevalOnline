from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Users, Coords, Levels, Pereval
from .serializers import PerevalSerializer

class SubmitDataTestCase(APITestCase):

    @classmethod
    def setUp(self):

        testuser1 = Users.objects.create(email='testuser1@test.com', fam='testuser1', name='testuser1', otc='testuser1',
                                        phone='11111111111')
        testuser2 = Users.objects.create(email='testuser2@test.com', fam='testuser2', name='testuser2', otc='testuser2',
                                        phone='22222222222')
        coords1 = Coords.objects.create(latitude=11.11, longitude=11.11, height=1111)
        coords2 = Coords.objects.create(latitude=22.22, longitude=22.22, height=2222)
        coords3 = Coords.objects.create(latitude=33.33, longitude=33.33, height=3333)
        level1 = Levels.objects.create(spring='1А', summer='', autumn='', winter='1Б')
        level2 = Levels.objects.create(spring='', summer='2А', autumn='2Б', winter='')
        self.pereval1 = Pereval.objects.create(title='pereval1', beauty_title='pereval1', other_titles='pereval1',
                                          user=testuser1, coords=coords1, level=level1)
        self.pereval2 = Pereval.objects.create(title='pereval2', beauty_title='pereval2', other_titles='pereval2',
                                          user=testuser2, coords=coords2, level=level2)
        self.pending_pereval = Pereval.objects.create(title='pereval3', beauty_title='pereval3', other_titles='pereval3',
                                          user=testuser1, coords=coords3, level=level1, status='pending')
    def test_get_object_by_id(self):

        expected = PerevalSerializer(self.pereval1).data
        url = reverse('pereval-detail', args=(self.pereval1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_post_object(self):

        pass

    def test_post_pending_object(self):

        pass