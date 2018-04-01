from django.contrib.auth.models import User
from django.test import TestCase
from dash_app.models import Dashboard


class DashboardModelTestCase(TestCase):

    def setUp(self):
        User.objects.create(username='user0', password='password', email='hello@world.com')
        User.objects.create(username='user1', password='password', email='hello@world.com')
        User.objects.create(username='user2', password='password', email='hello@world.com')

        Dashboard.objects.create(owner=User.objects.get(username='user0'))
        Dashboard.objects.create(owner=User.objects.get(username='user0'))
        Dashboard.objects.create(owner=User.objects.get(username='user1'))
        Dashboard.objects.create(owner=User.objects.get(username='user2'))

    def test_create(self):
        self.assertIsInstance(Dashboard.objects.create(owner=User.objects.get(username='user0')), Dashboard)
        self.assertIsInstance(Dashboard.objects.create(owner=User.objects.get(username='user0')), Dashboard)
        self.assertIsInstance(Dashboard.objects.create(owner=User.objects.get(username='user1')), Dashboard)

    def test_get(self):
        dashboard = Dashboard.objects.get(owner=User.objects.get(username='user1'))
        self.assertIsInstance(dashboard, Dashboard)
        self.assertEqual(dashboard.owner, User.objects.get(username='user1'))

    def test_filter(self):
        self.assertEqual(Dashboard.objects.filter(owner=User.objects.get(username='user1')).__len__(), 1)
        self.assertEqual(Dashboard.objects.filter(owner=User.objects.get(username='user0')).__len__(), 2)

    def test_delete(self):
        dashboard = Dashboard.objects.get(owner=User.objects.get(username='user1'))
        self.assertNotEqual(dashboard, None)
        self.assertIsInstance(dashboard, Dashboard)
        dashboard.delete()
        self.assertRaises(Dashboard.DoesNotExist, Dashboard.objects.get, owner=User.objects.get(username='user1'))

    def test_update(self):
        dashboard = Dashboard.objects.get(owner=User.objects.get(username='user2'))
        id = dashboard.id
        dashboard.owner = User.objects.get(username='user1')
        dashboard.save()
        self.assertEqual(Dashboard.objects.get(id=id), dashboard)
        self.assertEqual(Dashboard.objects.get(id=id).owner, User.objects.get(username='user1'))

