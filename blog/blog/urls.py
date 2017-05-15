
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from myblog.upload import *
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'uploads/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT,},),
    url(r'^admin/upload/(?P<dir_name>[^/]+)$',upload_image,name='upload_image'),
    url(r'^',include('myblog.url'))
    ]

