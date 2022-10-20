from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from urllib import response
import json


# create your views tests here.

class TestViews(TestCase):
    # default value
    def setUp(self):
        self.client = Client()

    # ifsc search view.
    def test_ifsc_search_get(self):
        response = self.client.get('/api/ifsc-search?ifsc_code=ABHY0065004', format='json')
        response = response.content.decode('utf8').replace("'", '"')
        response = json.loads(response)
        self.assertEquals(response.get('status'), status.HTTP_200_OK)

    # ifsc search view exception.
    def test_ifsc_search_get_wrong_ifsc(self):
        response = self.client.get('/api/ifsc-search?ifsc_code=ABHY0065004AA', format='json')
        response = response.content.decode('utf8').replace("'", '"')
        response = json.loads(response)
        self.assertEquals(response.get('status'), status.HTTP_400_BAD_REQUEST)

    # leaderboard view.
    def test_leaderboard_get(self):
        response = self.client.get('/api/leaderboard?sortorder=DESC&fetchcount=50', format='json')
        response = response.content.decode('utf8').replace("'", '"')
        response = json.loads(response)
        self.assertEquals(response.get('status'), status.HTTP_200_OK)

    # leaderboard view exception.
    def test_leaderboard_get_wrong_sort(self):
        response = self.client.get('/api/leaderboard?sortorder=desc&fetchcount=50', format='json')
        response = response.content.decode('utf8').replace("'", '"')
        response = json.loads(response)
        self.assertEquals(response.get('status'), status.HTTP_400_BAD_REQUEST)

    # statistics view.
    def test_statistics_get(self):
        response = self.client.get('/api/statistics?sortorder=DESC&fetchcount=1', format='json')
        response = response.content.decode('utf8').replace("'", '"')
        response = json.loads(response)
        self.assertEquals(response.get('status'), status.HTTP_200_OK)

    # statistics view exception.
    def test_statistics_get(self):
        response = self.client.get('/api/statistics?sortorder=DESC&fetchcount=200', format='json')
        response = response.content.decode('utf8').replace("'", '"')
        response = json.loads(response)
        self.assertEquals(response.get('status'), status.HTTP_404_NOT_FOUND)

    # per ifsc hits view.
    def test_ifsc_hits_get(self):
        response = self.client.get('/api/ifsc-hits', format='json')
        response = response.content.decode('utf8').replace("'", '"')
        response = json.loads(response)
        self.assertEquals(response.get('status'), status.HTTP_200_OK)

    # per url hits view.
    def test_url_hits_get(self):
        response = self.client.get('/api/url-hits', format='json')
        response = response.content.decode('utf8').replace("'", '"')
        response = json.loads(response)
        self.assertEquals(response.get('status'), status.HTTP_200_OK)