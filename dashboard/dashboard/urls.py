from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

# General routing
# Administration url and include from the dash_app application

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('dash_app.urls')),  # include of urls from dash_app
]

urlpatterns += [
    url(r'^api/', include('rest_framework.urls')),
]
