from django.contrib.auth.models import User
from django.test import TestCase
from dash_app.models import Widget, App, Account, Dashboard
from dash_app.serializers import WidgetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO


class WidgetSerializerTestCase(TestCase):

    def setUp(self):
        self.user0 = User.objects.create(username='user0', password='password', email='hello@world.com')
        self.user1 = User.objects.create(username='user1', password='password', email='hello@world.com')

        self.dashboard0 = Dashboard.objects.create(owner=self.user0)
        self.dashboard1 = Dashboard.objects.create(owner=self.user1)

        self.app0 = App.objects.create(name='test0', description='description')
        self.app1 = App.objects.create(name='test1', description='description')

        self.account0 = Account.objects.create(owner=self.user0, type='type0', name='name0', token='token0', info='info0')
        self.account1 = Account.objects.create(owner=self.user1, type='type1', name='name1', token='token1', info='info1')

        self.widget0 = Widget.objects.create(dashboard=self.dashboard0, app=self.app0, account=self.account0, position_x=0, position_y=0, size_x=2,
                              size_y=2)
        self.widget1 = Widget.objects.create(dashboard=self.dashboard1, app=self.app1, account=self.account1, position_x=0, position_y=1, size_x=7,
                              size_y=4)

    def test_create(self):
        serializer = WidgetSerializer(self.widget0)
        widget0_string = {
            'id': self.widget0.id,
            'dashboard': self.widget0.dashboard.id,
            'app': self.widget0.app.id,
            'account': self.widget0.account.id,
            'position_x': self.widget0.position_x,
            'position_y': self.widget0.position_y,
            'size_x': self.widget0.size_x,
            'size_y': self.widget0.size_y
        }
        self.assertEqual(serializer.data, widget0_string)

    def test_edit(self):
        new_attr = {
            'dashboard': self.dashboard1.id,
            'app': self.app1.id,
            'account': self.account1.id,
            'position_x': 7,
            'position_y': 0,
            'size_y': 20,
            'size_x': 10
        }

        new_widget0_string = {
            'id': self.widget0.id,
            'dashboard': self.dashboard1.id,
            'app': self.app1.id,
            'account': self.account1.id,
            'position_x': 7,
            'position_y': 0,
            'size_y': 20,
            'size_x': 10
        }
        serializer = WidgetSerializer(instance=self.widget0, data=new_attr, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(serializer.data, new_widget0_string)

    def test_json(self):
        serializer = WidgetSerializer(self.widget0)
        content = JSONRenderer().render(serializer.data)
        json_string = b'{"id":1,"dashboard":1,"app":1,"account":1,"position_x":0,"position_y":0,"size_x":2,"size_y":2}'
        self.assertEqual(content, json_string)

    def test_from_json(self):
        json_string = b'{"dashboard":1,"app":1,"account":1,"position_x":0,"position_y":0,"size_x":0,"size_y":0}'
        stream = BytesIO(json_string)
        data = JSONParser().parse(stream)
        serializer = WidgetSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        account_string = {
            'dashboard': 1,
            'app': 1,
            'account': 1,
            'position_x': 0,
            'position_y': 0,
            'size_x': 0,
            'size_y': 0
        }
        self.assertEqual(serializer.data, account_string)
