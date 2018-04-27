from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from dash_app import views

# Routing for the application
# Generated urls for the modelViewSets of django rest framework

# schema_view = get_schema_view(title='API')

router = DefaultRouter()

router.register(r'apps', views.AppViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'widgets', views.WidgetViewSet)
router.register(r'dashboards', views.DashboardViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # url(r'^schema/$', schema_view),
    url(r'^', include(router.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^users/register', views.CreateUserView.as_view())
]

urlpatterns += [
    url(r'^onenote/token', views.OneNoteTokenView.as_view()),
]