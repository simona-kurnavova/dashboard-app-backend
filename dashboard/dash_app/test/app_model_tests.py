from django.db import IntegrityError
from django.test import TestCase
from dash_app.models import App


class AppModelTestCase(TestCase):

    def setUp(self):
        App.objects.create(name='test0', description='description')
        App.objects.create(name='test1', description='description')

    def test_create(self):
        self.assertIsInstance(App.objects.create(name='test2', description='description'), App)
        self.assertIsInstance(App.objects.create(name='test3', description='description'), App)
        self.assertIsInstance(App.objects.create(name='test4'), App)
        self.assertIsInstance(App.objects.create(name='test5'), App)
        self.assertRaises(IntegrityError, App.objects.create, name='test2')

    def test_get(self):
        app = App.objects.get(name='test0')
        self.assertIsInstance(app, App)
        self.assertEqual(app.name, 'test0')
        self.assertEqual(app.description, 'description')

    def test_filter(self):
        self.assertEqual(App.objects.filter(name='test0').__len__(), 1)
        self.assertEqual(App.objects.filter(description='description').__len__(), 2)
        self.assertEqual(App.objects.filter(name='test').__len__(), 0)

    def test_delete(self):
        app = App.objects.get(name='test0')
        self.assertNotEqual(app, None)
        self.assertIsInstance(app, App)
        app.delete()
        self.assertRaises(App.DoesNotExist, App.objects.get, name='test0')

    def test_update(self):
        app = App.objects.get(name='test1')
        id = app.id
        app.name = 'new name'
        app.description = 'new description'
        app.save()
        self.assertEqual(App.objects.get(id=id), app)
        self.assertEqual(App.objects.get(id=id).name, 'new name')
        self.assertEqual(App.objects.get(id=id).description, 'new description')
