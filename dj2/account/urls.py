from django.conf.urls import url, include
from .views import *

urlpatterns = [
    # url(r'^test/', Test, name='test'),
    # url(r'^registration/', Registration, name='registration'),
    url(r'^/update-info', UpdateInfoView, name='update_info'),
    # url(r'^(?P<k_type_slug>[-\w]+)/$', ServeTheme),
    # url(r'^$', ServeType, name='kitchen')
]
