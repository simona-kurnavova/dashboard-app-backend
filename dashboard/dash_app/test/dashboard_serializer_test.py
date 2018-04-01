from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Dashboard
from ..serializers import DashboardSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO


class DashboardSerializerTestCase(TestCase):

    def setUp(self):
        self.user0 = User.objects.create(username='user0', password='password', email='hello@world.com')
        self.user1 = User.objects.create(username='user1', password='password', email='hello@world.com')

        self.dash0 = Dashboard.objects.create(owner=self.user0)
        self.dash1 = Dashboard.objects.create(owner=self.user1)

    def test_create(self):
        serializer = DashboardSerializer(self.dash0)
        dashboard0_string = {
            'owner': self.dash0.owner.id,
            'id': self.dash0.id
        }
        self.assertEqual(serializer.data, dashboard0_string)

    def test_edit(self):
        new_owner = {
            'owner': self.user1.id,
        }

        new_dash0_string = {
            'owner': self.user1.id,
            'id': self.dash0.id
        }
        serializer = DashboardSerializer(instance=self.dash0, data=new_owner, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(serializer.data, new_dash0_string)

    def test_json(self):
        serializer = DashboardSerializer(self.dash1)
        content = JSONRenderer().render(serializer.data)
        json_string = b'{"id":2,"owner":2}'
        self.assertEqual(content, json_string)

    def test_from_json(self):
        json_string = b'{"owner":"1"}'
        stream = BytesIO(json_string)
        data = JSONParser().parse(stream)
        serializer = DashboardSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        dash_string = {
            'owner': 1,
        }
        self.assertEqual(serializer.data, dash_string)
