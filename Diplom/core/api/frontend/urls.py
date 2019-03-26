from .views import (
    FrontendImageList, FrontendImageDetail, ImageView, ImageOperation,
    FrontendEntityList, FrontendEntityDetail, EntityView, EntityOperation,
    FrontendAuthorList, FrontendAuthorDetail, AuthorView, AuthorOperation,
    SearchDetailView, SearchView,
)
from django.conf.urls import url

urlpatterns = [
    url(r'^entitys/$', FrontendEntityList.as_view(), name='entitys-list-front'),
    url(r'^entity/(?P<pk>\d+)/$', FrontendEntityDetail.as_view(), name='entity-detail-front'),
    url(r'^entity-operation/$', EntityView.as_view(), name='entity-add'),
    url(r'^entity-operation/(?P<pk>\d+)/$', EntityView.as_view(), name='entity-change'),
    url(r'^entity/(?P<pk>\d+)/(?P<operation>\w+)/$', EntityOperation.as_view(), name='entity-operation'),

    url(r'^authors/$', FrontendAuthorList.as_view(), name='authors_list'),
    url(r'^author/(?P<pk>\d+)/$', FrontendAuthorDetail.as_view(), name='author-detail-front'),
    url(r'^author/(?P<pk>\d+)/(?P<operation>\w+)/$', AuthorOperation.as_view(), name='author-operation'),
    url(r'^author-operation/$', AuthorView.as_view(), name='author-add'),
    url(r'^author-operation/(?P<pk>\d+)/$', AuthorView.as_view(), name='author-change'),

    url(r'^images/$', FrontendImageList.as_view(), name='images-list-front'),
    url(r'^image/(?P<pk>\d+)/$', FrontendImageDetail.as_view(), name='image-detail-front'),
    url(r'^image/(?P<pk>\d+)/(?P<operation>\w+)/$', ImageOperation.as_view(), name='image-operation'),
    url(r'^image-operation/$', ImageView.as_view(), name='image-add'),
    url(r'^image-operation/(?P<pk>\d+)/$', ImageView.as_view(), name='image-change'),

    url(r'^search-detail/$', SearchDetailView.as_view(), name='search-detail'),
    url(r'^search/$', SearchView.as_view(), name='search'),
]
