from django.conf.urls import include, url
from . import views

# Basic URLS
urlpatterns = [
    url(r'^$', views.index, name='sparta_index'),
    url(r'^activities$', views.activities, name='sparta_activities'),
    url(r'^membersrating$', views.rating, name='sparta_rating'),
    url(r'^(?P<activity_id>[0-9]+)/uploadcsv$', views.uploadcsv, name='sparta_uploadcsv'),
    url(r'^(?P<activity_id>[0-9]+)/user_grade$', views.user_grade_view, name='sparta_user_grades'),
    url(r'^(?P<activity_id>[0-9]+)/user_grade/update$', views.user_grade_view, name='sparta_update_user_grades'),
    url(r'^(?P<activity_id>[0-9]+)/user_grade/new$', views.NewUserGradeView.as_view(), name='sparta_new_user_grade'),
    url(r'^(?P<user_grade_id>[0-9]+)/user_grade/delete$', views.delete_user_grade_view, name='sparta_delete_user_grade'),
]
