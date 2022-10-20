from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app.views import IFSC_Search, Leaderboard, Statistics, IFSCHits, URLSHits


# create your url tests here.

class TestUrls(SimpleTestCase):
    
    # ifsc_search url test.
    def test_ifsc_search_resolves(self):
        url = reverse('ifsc_search')    
        self.assertEquals(resolve(url).func.view_class, IFSC_Search)

    # leaderboard url test.
    def test_leaderboard_resolves(self):
        url = reverse('leaderboard')    
        self.assertEquals(resolve(url).func.view_class, Leaderboard)

    # statistics url test. 
    def test_statistics_resolves(self):
        url = reverse('statistics')    
        self.assertEquals(resolve(url).func.view_class, Statistics)

    # ifsc_hits url test.
    def test_ifsc_hits_resolves(self):
        url = reverse('ifsc_hits')    
        self.assertEquals(resolve(url).func.view_class, IFSCHits)

    # url_hits url test.
    def test_url_hits_resolves(self):
        url = reverse('url_hits')    
        self.assertEquals(resolve(url).func.view_class, URLSHits)
