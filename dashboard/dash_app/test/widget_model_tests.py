from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Widget, Dashboard, App, Account


class WidgetModelTestCase(TestCase):
    def setUp(self):
        user0 = User.objects.create(username='user0', password='password', email='hello@world.com')
        user1 = User.objects.create(username='user1', password='password', email='hello@world.com')

        dashboard0 = Dashboard.objects.create(owner=user0)
        dashboard1 = Dashboard.objects.create(owner=user1)

        app0 = App.objects.create(name='test0', description='description')
        app1 = App.objects.create(name='test1', description='description')

        account0 = Account.objects.create(owner=user0, type='type0', name='name0', token='token0', info='info0')
        account1 = Account.objects.create(owner=user1, type='type1', name='name1', token='token1', info='info1')

        Widget.objects.create(dashboard=dashboard0, app=app0, account=account0, position_x=0, position_y=0, size_x=2,
                              size_y=2)
        Widget.objects.create(dashboard=dashboard1, app=app1, account=account1, position_x=0, position_y=1, size_x=7,
                              size_y=4)

    def test_create(self):
        self.assertIsInstance(
            Widget.objects.create(dashboard=Dashboard.objects.get(owner=User.objects.get(username='user0')),
                                  app=App.objects.get(name='test1'),
                                  account=Account.objects.get(owner=User.objects.get(username='user0')),
                                  position_x=1,
                                  position_y=1,
                                  size_x=4,
                                  size_y=8),
            Widget
        )

    def test_get(self):
        self.assertIsInstance(Widget.objects.get(account=Account.objects.get(name='name0')), Widget)
        self.assertIsInstance(Widget.objects.get(size_x=7), Widget)
        self.assertRaises(Widget.DoesNotExist, Widget.objects.get, position_x=100)

    def test_filter(self):
        self.assertEqual(Widget.objects.filter(size_x=0).__len__(), 0)
        self.assertEqual(Widget.objects.filter(position_x=0).__len__(), 2)

    def test_delete(self):
        widget = Widget.objects.get(account=Account.objects.get(type='type0'))
        self.assertNotEqual(widget, None)
        self.assertIsInstance(widget, Widget)
        widget.delete()
        self.assertRaises(Widget.DoesNotExist, Widget.objects.get, account=Account.objects.get(type='type0'))

    def test_update(self):
        widget = Widget.objects.get(account=Account.objects.get(type='type1'))
        id = widget.id
        widget.account = Account.objects.get(type='type0')
        widget.save()
        self.assertEqual(Widget.objects.get(id=id), widget)
        self.assertEqual(Widget.objects.get(id=id).account, Account.objects.get(type='type0'))