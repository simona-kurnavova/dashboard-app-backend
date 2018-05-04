from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from dash_app.models import App

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('dash_app.urls')),  # include of urls from dash_app
]

urlpatterns += [
    url(r'^api/', include('rest_framework.urls')),
]

apps = App.objects.filter(has_backend=True)
for app in apps:
    urlpatterns += [
        url(r'^', include(app.name + '.urls'))
    ]
