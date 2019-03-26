from django.conf.urls import url, include


urlpatterns = [
    url(r'^api/', include('core.api.urls')),
    url(r'^frontend/', include('core.api.frontend.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^api-auth/', include('rest_framework.urls')),
]
