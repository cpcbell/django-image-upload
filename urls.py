from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^blank/$', 'imagestorage.views.blank', name='blank'),
    url(r'^testupload/$', 'imagestorage.views.testUpload', name='testUpload'),
    url(r'^saveFileUpload/$', 'imagestorage.views.saveFileUpload', name='saveFileUpload'),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
