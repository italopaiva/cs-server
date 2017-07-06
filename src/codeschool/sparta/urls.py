from django.conf.urls import include, url
from . import views

# Basic URLS
urlpatterns = [
    url(r'^$', views.index, name='sparta_index'),
    url(r'^activities$', views.activities, name='sparta_activities'),
    url(r'^rate$', views.rating, name='sparta_rating'),
    url(r'^(?P<activity_id>[0-9]+)/uploadcsv$', views.uploadcsv, name='sparta_uploadcsv'),
]
