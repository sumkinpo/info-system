from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^records/', views.records_list, name='records_lsit'),
    url(r'^record/(?P<id>\d+)/$', views.record_detail, name='record_detail'),
    url(r'^search/', views.search_record, name='search_record'),
]
