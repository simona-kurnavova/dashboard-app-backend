from dash_app.models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ('id', 'name', 'description', 'required_account')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'owner', 'type', 'name', 'token', 'info')


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ('id', 'dashboard', 'app', 'account', 'position_x', 'position_y')


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = ('id', 'owner')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
