from django.conf.urls import url
from onenote import views

urlpatterns = [
    url(r'onenote/token', views.OneNoteTokenView.as_view()),
    url(r'onenote/refresh_token', views.OneNoteTokenRefreshView.as_view())
]
