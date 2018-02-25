from django.db import models


class App(models.Model):
    name = models.CharField(max_length=40, unique=True)  # unique identifying name of an app, component name
    description = models.CharField(max_length=300, blank=True, null=True)
    required_account = models.CharField(max_length=40, blank=True, null=True)  # type of account


class Account(models.Model):
    owner = models.ForeignKey('auth.User', related_name='accounts', on_delete=models.CASCADE)
    type = models.CharField(max_length=40)  # type of account: google, facebook, slack
    name = models.CharField(max_length=40)  # type of account: in readable form
    token = models.CharField(max_length=300)
    info = models.CharField(max_length=300, blank=True, null=True)


class Dashboard(models.Model):
    owner = models.ForeignKey('auth.User', related_name='dashboards', on_delete=models.CASCADE)


class Widget(models.Model):
    dashboard = models.ForeignKey('Dashboard', related_name='widgets', on_delete=models.CASCADE)
    app = models.ForeignKey('App', related_name='widgets', on_delete=models.CASCADE)
    account = models.ForeignKey('Account', related_name='widgets', on_delete=models.CASCADE)
    position_x = models.IntegerField()  # X position of left upper corner on dashboard
    position_y = models.IntegerField()  # Y position of left upper corner on dashboard
