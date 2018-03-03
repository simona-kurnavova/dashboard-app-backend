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
        fields = ('id', 'dashboard', 'app', 'account', 'position_x', 'position_y', 'size_x', 'size_y')


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = ('id', 'owner')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user