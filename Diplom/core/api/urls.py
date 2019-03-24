from .views import ImageList, ImageDetail, EntityList, EntityDetail, AuthorList, AuthorDetail
from django.conf.urls import url

urlpatterns = [
    url(r'^entitys/$', EntityList.as_view(), name='entitys-list'),
    url(r'^entity/(?P<pk>\d+)/$', EntityDetail.as_view(), name='entity-detail'),
    url(r'^authors/$', AuthorList.as_view(), name='authors_list'),
    url(r'^author/(?P<pk>\d+)/$', AuthorDetail.as_view(), name='author-detail'),
    url(r'^images/$', ImageList.as_view(), name='images-list'),
    url(r'^image/(?P<pk>\d+)/$', ImageDetail.as_view(), name='image-detail'),

]