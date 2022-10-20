from django.urls import path

from .views import *

# create your urls here.

urlpatterns = [
    path('ifsc-search', IFSC_Search.as_view(), name="ifsc_search"),
    path('leaderboard', Leaderboard.as_view(), name="leaderboard"),
    path('statistics', Statistics.as_view(), name="statistics"),
    path('ifsc-hits', IFSCHits.as_view(), name="ifsc_hits"),
    path('url-hits', URLSHits.as_view(), name="url_hits"),
]
