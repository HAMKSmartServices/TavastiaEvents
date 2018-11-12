from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from events.models import Event, Place, Keyword, Image
from events.api import PlacePostSerializer

"""
def minimal_event_dict(location_id):
    return {
        'name': {'fi': TEXT},
        'start_time': DATETIME,
        'location': {'@id': location_id},
        'keywords': [
            {'@id': keyword_id('test')},
        ],
        'short_description': {'fi': 'short desc', 'sv': 'short desc sv', 'en': 'short desc en'},
        'description': {'fi': 'desc', 'sv': 'desc sv', 'en': 'desc en'},
        'offers': [
            {
                'is_free': False,
                'price': {'en': TEXT, 'sv': TEXT, 'fi': TEXT},
                'description': {'en': TEXT, 'sv': TEXT, 'fi': TEXT},
                'info_url': {'en': URL, 'sv': URL, 'fi': URL}
            }
        ]
    }
"""

class PlaceTests(APITestCase):
    def test_get_place_list(self):
        #response = self.client.post(url, data, format='json')
        #print(response.content)
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(Event.objects.count(), 1)
        url = '/v1/place/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Place.objects.count(), 0)

    def test_post_place(self):
        url = '/v1/place/'
        data = {
            'id': 'test_location',
            'position': {
                "latitude": 60.000,
                "longitude": 40.000
            },
            "street_address": {
                "fi": "Osoite"
            },
            "address_locality": {
                "fi": "Kaupunki"
            }
        }
        #return Place.objects.create(
        #id='test_location',
        #data_source=data_source,
        #publisher=organization,
        #position=Point(50, 50),
        #name='Place 1'
        #)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Place.objects.count(), 1)

def place():
    return Place.objects.create(
        id='test_location',
        position=Point(50, 50),
        name='Place 1',
        street_address='Osoite',
        address_locality='Kaupunki'
    )

def location_id(place):
    obj_id = reverse(PlacePostSerializer().view_name, kwargs={'pk': place.id})
    return obj_id

class EventsTests(APITestCase):
    def test_get_keyword_list(self):
        url = '/v1/keyword/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Keyword.objects.count(), 0)
    
    def test_get_place_list(self):
        url = '/v1/place/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Place.objects.count(), 0)

    def test_get_events(self):
        url = '/v1/event/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.count(), 0)

    """
    def test_event_post(self):
        url = '/v1/event/'

        data = {
            'name': {
                "fi": "testi"
            },
            "pin": "1234",
            "accessible": True,
            'location': {'@id': location_id}
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
    """

class ImageTests(APITestCase):
    def test_get_image_list(self):
        url = '/v1/image/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Image.objects.count(), 0)


