from django.urls import path
from .views import *

def sites(url):
	return '{}/{}'.format('sites/(?P<site_id>[-\d]+)', url)

urlpatterns = [
    path(sites('pages/<str:page_key>/texts/'), TextView.as_view(), name='text-list'),
    path(sites('pages/<str:page_key>/texts/<str:key>/'), TextView.as_view(), name='text-obj'),
    path(sites('pages/<str:key>/'), PageView.as_view(), name='page-list'),
    path(sites('pages/'), PageView.as_view(), name='page-obj'),
    path(sites('files'), FileUploadView.as_view(), name = 'file_upload'),
	path(sites('files/signed'), SignedUrlView.as_view(), name = 'get_signed'),
    path(sites('images/upload'), ImageUploadView.as_view(), name = 'image_upload'),
]
