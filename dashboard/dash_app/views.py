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


class WidgetViewSet(viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer


class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CreateUserView(APIView):
    ''' Standard view for creating new user only. Without authentication or permissions. '''
    authentication_classes = ()
    permission_classes = ()
    model = User
    serializer_class = UserSerializer

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
