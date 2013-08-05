from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from example.views import SendMailView
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', SendMailView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
