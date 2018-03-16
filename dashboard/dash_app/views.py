from itertools import chain

from django.db.models import QuerySet
from django.http import HttpResponse
from rest_framework.decorators import detail_route
from dash_app.serializers import *
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user.id)


class WidgetViewSet(viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer

    def get_queryset(self):
        ''' Finds out which dashboards are owned by user and returns only widgets from them. '''
        dashboards = self.request.user.dashboards.all()
        widgets = []
        for dashboard in dashboards:
            temp = Widget.objects.filter(dashboard=dashboard.id)
            for widget in temp:
                widgets.append(widget)
        return widgets


class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Dashboard.objects.filter(owner=self.request.user.id)


class CreateUserView(APIView):
    ''' Standard view for creating new user only. Without authentication or permissions. '''
    authentication_classes = ()
    permission_classes = ()
    model = User
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        # TODO: Access denied
        pass
