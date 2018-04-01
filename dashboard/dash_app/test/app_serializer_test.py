from django.test import TestCase
from ..models import App
from ..serializers import AppSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO


class AppSerializerTestCase(TestCase):

    def setUp(self):
        self.app0 = App.objects.create(name='test0', description='description')
        self.app1 = App.objects.create(name='test1', description='description')

    def test_create(self):
        serializer = AppSerializer(self.app0)
        app0_string = {
            'description': self.app0.description,
            'name': self.app0.name,
            'id': self.app0.id
        }
        self.assertEqual(serializer.data, app0_string)

    def test_edit(self):
        new_name = {
            'name': 'new name',
            'description': 'new description'
        }

        new_app0_string = {
            'description': 'new description',
            'name': 'new name',
            'id': self.app0.id
        }
        serializer = AppSerializer(instance=self.app0, data=new_name, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(serializer.data, new_app0_string)

    def test_json(self):
        serializer = AppSerializer(self.app1)
        content = JSONRenderer().render(serializer.data)
        json_string = b'{"id":2,"name":"test1","description":"description"}'
        self.assertEqual(content, json_string)

    def test_from_json(self):
        json_string = b'{"name":"test","description":"description"}'
        stream = BytesIO(json_string)
        data = JSONParser().parse(stream)
        serializer = AppSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        app_string = {
            'description': 'description',
            'name': 'test',
        }
        self.assertEqual(serializer.data, app_string)
