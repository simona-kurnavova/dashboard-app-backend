from django.test import TestCase
from .models import App


class AppTestCase(TestCase):
    def setUp(self):
        App.objects.create(name='test0', description='description', required_account='required')
        App.objects.create(name='test1', description='description', required_account='required')

    def test_get_app(self):
        app = App.objects.get(name='test0')
        self.assertEqual(app.name, 'test0')
        self.assertEqual(app.description, 'description')
        self.assertEqual(app.required_account, 'required')

    def test_filter_app(self):
        self.assertEqual(App.objects.filter(name='test0').__len__(), 1)
        self.assertEqual(App.objects.filter(description='description').__len__(), 2)
        self.assertEqual(App.objects.filter(name='test').__len__(), 0)

    def test_create(self):
        app0 = App(name='test2', description='description', required_account='none')
        app1 = App(name='test3', description='description')
        app2 = App(name='test4', required_account='none')
        app3 = App(name='test5')
        self.assertEqual(app0.save(), None)
        self.assertEqual(app1.save(), None)
        self.assertEqual(app2.save(), None)
        self.assertEqual(app3.save(), None)

    # def test_create_errors(self):
    # def test_delete(self):
    # def test_update(self):
