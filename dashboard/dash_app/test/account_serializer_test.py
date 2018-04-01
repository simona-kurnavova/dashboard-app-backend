from django.contrib.auth.models import User
from django.test import TestCase
from dash_app.models import Account
from dash_app.serializers import AccountSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO


class AccountSerializerTestCase(TestCase):

    def setUp(self):
        self.user0 = User.objects.create(username='user0', password='password', email='hello@world.com')
        self.user1 = User.objects.create(username='user1', password='password', email='hello@world.com')

        self.account0 = Account.objects.create(owner=self.user0, type='type0', name='name0', token='token0', info='info0')
        self.account1 = Account.objects.create(owner=self.user1, type='type1', name='name1', token='token1', info='info1')

    def test_create(self):
        serializer = AccountSerializer(self.account0)
        dashboard0_string = {
            'id': self.account0.id,
            'owner': self.account0.owner.id,
            'type': self.account0.type,
            'name': self.account0.name,
            'token': self.account0.token,
            'info': self.account0.info
        }
        self.assertEqual(serializer.data, dashboard0_string)

    def test_edit(self):
        new_attr = {
            'type': 'new type',
            'name': 'new name',
            'token': 'new token',
            'info': 'new info'
        }

        new_account0_string = {
            'id': self.account0.id,
            'owner': self.account0.owner.id,
            'type': 'new type',
            'name': 'new name',
            'token': 'new token',
            'info': 'new info'
        }
        serializer = AccountSerializer(instance=self.account0, data=new_attr, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(serializer.data, new_account0_string)

    def test_json(self):
        serializer = AccountSerializer(self.account0)
        content = JSONRenderer().render(serializer.data)
        json_string = b'{"id":1,"owner":1,"type":"type0","name":"name0","token":"token0","info":"info0"}'
        self.assertEqual(content, json_string)

    def test_from_json(self):
        json_string = b'{"owner":1,"type":"type","name":"name","token":"token","info":"info"}'
        stream = BytesIO(json_string)
        data = JSONParser().parse(stream)
        serializer = AccountSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        account_string = {
            'owner': 1,
            'type': 'type',
            'name': 'name',
            'token': 'token',
            'info': 'info'
        }
        self.assertEqual(serializer.data, account_string)
