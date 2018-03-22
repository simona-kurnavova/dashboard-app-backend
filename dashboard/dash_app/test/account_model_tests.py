from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Account


class AccountModelTestCase(TestCase):

    def setUp(self):
        user0 = User.objects.create(username='user0', password='password', email='hello@world.com')
        user1 = User.objects.create(username='user1', password='password', email='hello@world.com')
        user2 = User.objects.create(username='user2', password='password', email='hello@world.com')

        Account.objects.create(owner=user0, type='type0', name='name0', token='token0', info='info0')
        Account.objects.create(owner=user1, type='type1', name='name1', token='token1', info='info1')
        Account.objects.create(owner=user2, type='type2', name='name2', token='token2', info='info2')
        Account.objects.create(owner=user2, type='type2', name='name2', token='token2', info='info2')

    def test_create(self):
        self.assertIsInstance(Account.objects.create(
            owner=User.objects.get(username='user0'), type='type3', name='name3', token='token3'
        ), Account)
        self.assertIsInstance(Account.objects.create(
            owner=User.objects.get(username='user0'), type='type4', name='name4', token='token4', info='info4'
        ), Account)

    def test_get(self):
        self.assertIsInstance(Account.objects.get(type='type0'), Account)
        self.assertIsInstance(Account.objects.get(name='name1'), Account)
        self.assertIsInstance(Account.objects.get(info='info0'), Account)
        self.assertRaises(Account.DoesNotExist, Account.objects.get, name='unknown')

    def test_filter(self):
        self.assertEqual(Account.objects.filter(info='non existent').__len__(), 0)
        self.assertEqual(Account.objects.filter(type='type0').__len__(), 1)
        self.assertEqual(Account.objects.filter(name='name2').__len__(), 2)

    def test_delete(self):
        account = Account.objects.get(owner=User.objects.get(username='user0'))
        self.assertNotEqual(account, None)
        self.assertIsInstance(account, Account)
        account.delete()
        self.assertRaises(Account.DoesNotExist, Account.objects.get, owner=User.objects.get(username='user0'))

    def test_update(self):
        account = Account.objects.get(owner=User.objects.get(username='user1'))
        id = account.id
        account.owner = User.objects.get(username='user2')
        account.save()
        self.assertEqual(Account.objects.get(id=id), account)
        self.assertEqual(Account.objects.get(id=id).owner, User.objects.get(username='user2'))