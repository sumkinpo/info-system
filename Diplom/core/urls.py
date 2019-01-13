from django.conf.urls import url
from .views import entitys_view

urlpatterns = [
    url(r'^entitys/$', entitys_view.entity_list, name='entitys_list'),
    url(r'^entity/(?P<id>\d+)/$', entitys_view.entity_detail, name='entity'),
    url(r'^search/$', entitys_view.search_entity, name='search_entity'),
]
