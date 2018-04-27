from django.db import models


class App(models.Model):
    """
    Stores data of Applications available
    """
    name = models.CharField(max_length=40, unique=True,
                            help_text="Unique name of the app, represents base of Angular component name")
    description = models.CharField(max_length=300, blank=True, null=True,  help_text="Brief description of the app")


class Account(models.Model):
    """
    Represents Account of any available application, owned by the user and storing access token
    """
    owner = models.ForeignKey('auth.User', related_name='accounts', on_delete=models.CASCADE, blank=True, null=True,
                              help_text="User that owns the account")
    type = models.CharField(max_length=40, help_text="Type of account, usually application name")
    name = models.CharField(max_length=40, help_text="Type of account in readable form")
    token = models.CharField(max_length=300, help_text="Access token to application")
    info = models.CharField(max_length=300, blank=True, null=True,  help_text="Any info about the account or app")


class Dashboard(models.Model):
    """
    Represents dashboard which holds widgets
    """
    owner = models.ForeignKey('auth.User', related_name='dashboards', on_delete=models.CASCADE, blank=True, null=True,
                              help_text="User that owns the Dashboard")


class Widget(models.Model):
    """
    Represents widget on the dashboard with its characteristics
    """
    dashboard = models.ForeignKey('Dashboard', related_name='widgets', on_delete=models.CASCADE,
                                  help_text="Dashboard widget is located at")
    app = models.ForeignKey('App', related_name='widgets', on_delete=models.CASCADE,
                            help_text="Application it is representing")
    account = models.ForeignKey('Account', related_name='widgets', on_delete=models.SET_NULL, blank=True, null=True,
                                help_text="Account associated with the widget")
    position_x = models.IntegerField(help_text="X coordinate of the widget on dashboard")
    position_y = models.IntegerField(help_text="Y coordinate of the widget on dashboard")
    size_x = models.IntegerField(help_text="Width of the widget on dashboard")
    size_y = models.IntegerField(help_text="Height of the widget on dashboard")

