from django.http import Http404
from dash_app.serializers import *
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, response, status
from rest_framework.views import APIView
from rest_framework.response import Response


class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    # TODO: get object, delete and update only by owner

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
        widgets.sort(key=lambda x: (x.position_y, x.position_x))  # order by position y and x
        return widgets

    def destroy(self, request, pk=None, **kwargs):
        ''' Returns 204 status after successful delete, 404 if doesn't exists and 403 if access is forbidden. '''
        try:
            widget = Widget.objects.get(id=pk)
            if widget.dashboard.owner != self.request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            widget.delete()
        except Widget.DoesNotExist:
            raise Http404
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        serializer = WidgetSerializer(Widget.objects.get(id=pk), request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        serializer = UserSerializer(User.objects.get(id=pk), request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
