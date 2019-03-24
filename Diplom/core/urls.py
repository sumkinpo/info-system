from django.conf.urls import url, include
from .api import entitys_view


urlpatterns = [
    # url(r'^entitys/$', entitys_view.entity_list, name='entitys_list'),
    # url(r'^entity/(?P<id>\d+)/$', entitys_view.entity_detail, name='entity'),
    url(r'^api/', include('core.api.urls')),
    url(r'^frontend/', include('core.api.frontend.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^api-auth/', include('rest_framework.urls')),
]
