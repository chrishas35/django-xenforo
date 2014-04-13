from __future__ import unicode_literals

from unittest import TestCase

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

from ..middleware import XFAuthenticationMiddleware, XFSessionMiddleware
from ..conf import settings


class TestXFSessionMiddleware(TestCase):
    def setUp(self):
        self.middleware = XFSessionMiddleware()
        self.request = Mock()

    def test_no_xenforo_session_cookie(self):
        self.request.COOKIES = dict()
        self.middleware.process_request(self.request)
        self.assertEqual(self.request.xf_session_id, None)
        self.assertEqual(self.request.xf_session, None)

    def test_expired_or_nonexistant_session(self):
        self.request.COOKIES = {'%ssession' % settings.XENFORO_COOKIE_PREFIX: '123456abcdef'}
        with patch('xenforo.middleware.connections') as mockdb:
            mockdb[settings.XENFORO_DATABASE].cursor().fetchone.return_value = None
            self.middleware.process_request(self.request)
            self.assertEqual(self.request.xf_session_id, '123456abcdef')
            self.assertEqual(self.request.xf_session, None)

    def test_xf_session(self):
        self.request.COOKIES = {'%ssession' % settings.XENFORO_COOKIE_PREFIX: '123456abcdef'}
        with patch('xenforo.middleware.connections') as mockdb:
            mockdb[settings.XENFORO_DATABASE].cursor().fetchone.return_value = [b'123456abcdef', b'a:1:{s:7:"user_id";i:123;}', 1390352607] #TODO: Add IP address
            self.middleware.process_request(self.request)
        self.assertEqual(self.request.xf_session_id, '123456abcdef')
        self.assertEqual(self.request.xf_session.get('user_id'), 123)


class TestXFAuthenticationMiddleware(TestCase):
    def setUp(self):
        self.middleware = XFAuthenticationMiddleware()
        self.request = Mock()

    def test_no_xf_session_middleware(self):
        self.request = {}
        with self.assertRaises(Exception):
            self.middleware.process_request(self.request)

    def test_no_xf_session(self):
        self.request.xf_session = None
        self.middleware.process_request(self.request)
        self.assertEqual(self.request.xf_user_id, None)
        self.assertEqual(self.request.xf_user, None)

    def test_valid_session(self):
        self.request.META = {settings.XENFORO_IP_ADDRESS_KEY: '192.0.2.30',}
        self.request.xf_session = {'user_id': 123, 'ip': 3221226014}
        with patch('xenforo.middleware.connections') as mockdb:
            mockdb[settings.XENFORO_DATABASE].cursor().fetchall.return_value = ([123, 'TestUser'],)
            mockdb[settings.XENFORO_DATABASE].cursor().description = (('user_id', 3, None, 10, 10, 0, 0), ('username', 253, None, 50, 50, 0, 0),)
            self.middleware.process_request(self.request)
        self.assertEqual(self.request.xf_user_id, 123)
        self.assertEqual(self.request.xf_user, {'user_id': 123, 'username': 'TestUser'})

    def test_ip_mismatch(self):
        self.request.META = {settings.XENFORO_IP_ADDRESS_KEY: '192.0.2.31',}
        self.request.xf_session = {'user_id': 123, 'ip': 3221226014}
        with patch('xenforo.middleware.connections') as mockdb:
            mockdb[settings.XENFORO_DATABASE].cursor().fetchall.return_value = ([123, 'TestUser'],)
            mockdb[settings.XENFORO_DATABASE].cursor().description.return_value = (('user_id',),('username',))
            self.middleware.process_request(self.request)
        self.assertEqual(self.request.xf_user_id, None)
        self.assertEqual(self.request.xf_user, None)

    def test_no_xf_user_row(self):
        self.request.META = {settings.XENFORO_IP_ADDRESS_KEY: '192.0.2.30',}
        self.request.xf_session = {'user_id': 123, 'ip': 3221226014}
        with patch('xenforo.middleware.connections') as mockdb:
            mockdb[settings.XENFORO_DATABASE].cursor().fetchall.return_value = ()
            mockdb[settings.XENFORO_DATABASE].cursor().description.return_value = (('user_id',),('username',))
            self.middleware.process_request(self.request)
        self.assertEqual(self.request.xf_user_id, None)
        self.assertEqual(self.request.xf_user, None)
