from django.http import Http404
from dash_app.serializers import *
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, response, status
from rest_framework.views import APIView
from rest_framework.response import Response


class AppViewSet(viewsets.ModelViewSet):
    """
    App views
    """
    queryset = App.objects.all()
    serializer_class = AppSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """
    Account views
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        """
        Adds requesting user as an owner to the serializer.
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Returns accounts owned by requesting user.
        """
        return Account.objects.filter(owner=self.request.user.id)

    def retrieve(self, request, pk=None):
        """
        Returns object of Account if user is the owner
        """
        serializer = AccountSerializer(Account.objects.get(owner=self.request.user.id, id=pk))
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, **kwargs):
        """
        Returns 204 status after successful delete, 404 if doesn't exists and 403 if access is forbidden.
        """
        try:
            account = Account.objects.get(id=pk)
            if account.owner != self.request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            account.delete()
        except Account.DoesNotExist:
            raise Http404
        return Response(status=status.HTTP_204_NO_CONTENT)


class WidgetViewSet(viewsets.ModelViewSet):
    """
    Widget views
    """
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer

    def get_queryset(self):
        """
        Finds out which dashboards are owned by user and returns only widgets from them.
        """
        dashboards = self.request.user.dashboards.all()
        widgets = []
        for dashboard in dashboards:
            temp = Widget.objects.filter(dashboard=dashboard.id)
            for widget in temp:
                widgets.append(widget)
        widgets.sort(key=lambda x: (x.position_y, x.position_x))  # order by position y and x
        return widgets

    def destroy(self, request, pk=None, **kwargs):
        """
        Returns 204 status after successful delete, 404 if doesn't exists and 403 if access is forbidden.
        """
        try:
            widget = Widget.objects.get(id=pk)
            if widget.dashboard.owner != self.request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            widget.delete()
        except Widget.DoesNotExist:
            raise Http404
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        """
        Partially updates widget information and keeps the id.
        """
        serializer = WidgetSerializer(Widget.objects.get(id=pk), request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DashboardViewSet(viewsets.ModelViewSet):
    """
    Dashboard Views
    """
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer

    def perform_create(self, serializer):
        """
        Adds requesting user as an owner to serializer.
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Returns dashboards owned by the requesting user.
        """
        return Dashboard.objects.filter(owner=self.request.user.id)


class CreateUserView(APIView):
    """
    Standard view for creating new user only. Without authentication or permissions.
    """
    authentication_classes = ()
    permission_classes = ()
    model = User
    serializer_class = UserSerializer

    def post(self, request, format=None):
       """
       Creates new user and returns 201 on success and 400 on failure.
       """
       serializer = UserSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           Dashboard.objects.create(owner=User.objects.get(id=serializer.data['id']), justification='left')
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    User view - allowed only for authenticated users
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.get_queryset().order_by('id')
    serializer_class = CurrentUserSerializer

    def get_queryset(self):
       """
       Returns only requesting user information.
       """
       return User.objects.filter(id=self.request.user.id)

    def partial_update(self, request, pk=None):
       """
       Partially updates user information and keeps the id.
       """
       serializer = UserSerializer(User.objects.get(id=pk), request.data, partial=True)
       serializer.is_valid(raise_exception=True)
       serializer.save()
       return Response(serializer.data, status=status.HTTP_201_CREATED)
