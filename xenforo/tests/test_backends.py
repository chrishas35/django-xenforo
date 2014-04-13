# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

from django.contrib.auth.models import User

from ..backends import XFAuthBackend
from ..conf import settings


def mock_save(*args, **kwargs):
    return True

def mock_create_user(*args, **kwargs):
    user = User(username=kwargs['username'], **kwargs['defaults'])
    return (user, True)

def mock_get_existing_user(*args, **kwargs):
    user = User(username=kwargs['username'])
    user.password = 'NotThePassword'
    user.pk = kwargs['defaults']['pk']
    return (user, False)


class TestXFAuthBackend(TestCase):

    def setUp(self):
        self.backend = XFAuthBackend()

    def test_no_username(self):
        username = None
        password = None
        self.assertEqual(self.backend.authenticate(username,password), None)

    def test_invalid_user(self):
        username = 'NotFoundUser'
        password = 'lètmein'

        with patch('xenforo.backends.connections') as mockdb:
            mockdb[settings.XENFORO_DATABASE].cursor().fetchall.return_value = ()
            mockdb[settings.XENFORO_DATABASE].cursor().description = (('user_id',), ('username',), ('scheme_class',), ('data',))
            self.assertEqual(self.backend.authenticate(username,password), None)

    @patch('django.contrib.auth.models.User.save', mock_save)
    @patch('django.db.models.Manager.get_or_create', mock_create_user)
    def test_valid_user_created(self):
        username = 'TestUser'
        password = 'lètmein'

        with patch('xenforo.backends.connections') as mockdb:
            mockdb[settings.XENFORO_DATABASE].cursor().fetchall.return_value = ((123, 'TestUser', 'XenForo_Authentication_Core12', b'a:1:{s:4:"hash";s:60:"$2a$10$EnvKvs.royUb7HV2lBGAROLdwbghtS4KBlaDrkFoFa3sIAmPn6gk6";}'),)
            mockdb[settings.XENFORO_DATABASE].cursor().description = (('user_id',), ('username',), ('scheme_class',), ('data',))
            user = self.backend.authenticate(username,password)
            self.assertTrue(user)
            self.assertEqual(user.pk, 123)

    @patch('django.contrib.auth.models.User.save', mock_save)
    @patch('django.db.models.Manager.get_or_create', mock_get_existing_user)
    def test_valid_user_existing(self):
        username = 'TestUser'
        password = 'lètmein'

        with patch('xenforo.backends.connections') as mockdb:
            mockdb[settings.XENFORO_DATABASE].cursor().fetchall.return_value = ((1234, 'TestUser', 'XenForo_Authentication_Core12', b'a:1:{s:4:"hash";s:60:"$2a$10$EnvKvs.royUb7HV2lBGAROLdwbghtS4KBlaDrkFoFa3sIAmPn6gk6";}'),)
            mockdb[settings.XENFORO_DATABASE].cursor().description = (('user_id',), ('username',), ('scheme_class',), ('data',))
            user = self.backend.authenticate(username,password)
            self.assertTrue(user)
            self.assertEqual(user.password,
                'xenforo_core12$$2a$10$EnvKvs.royUb7HV2lBGAROLdwbghtS4KBlaDrkFoFa3sIAmPn6gk6')
