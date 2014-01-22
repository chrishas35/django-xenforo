from __future__ import unicode_literals

from unittest import TestCase

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

from ..middleware import XFAuthenticationMiddleware, XFSessionMiddleware


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
        self.request.COOKIES = {'xf_session': '123456abcdef'}
        with patch('xenforo.middleware.connection') as mockdb:
            mockdb.cursor().fetchone.return_value = None
            self.middleware.process_request(self.request)
            self.assertEqual(self.request.xf_session_id, '123456abcdef')
            self.assertEqual(self.request.xf_session, None)
    
    def test_xf_session(self):
        self.request.COOKIES = {'xf_session': '123456abcdef'}
        with patch('xenforo.middleware.connection') as mockdb:
            mockdb.cursor().fetchone.return_value = ['123456abcdef', b'a:1:{s:7:"user_id";i:123;}', 1390352607] #TODO: Add IP address
            self.middleware.process_request(self.request)
        self.assertEqual(self.request.xf_session_id, '123456abcdef')
        self.assertEqual(self.request.xf_session.get(b'user_id'), 123)


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
        self.request.META = {'HTTP_X_REAL_IP': '192.0.2.30',}
        self.request.xf_session = {'user_id': 123, 'ip': 3221226014}
        with patch('xenforo.middleware.connection') as mockdb:
            mockdb.cursor().fetchone.return_value = ['123', 'TestUser']
            self.middleware.process_request(self.request)
        self.assertEqual(self.request.xf_user_id, 123)
        self.assertEqual(self.request.xf_user, ['123', 'TestUser'])

    def test_ip_mismatch(self):
        self.request.META = {'HTTP_X_REAL_IP': '192.0.2.31',}
        self.request.xf_session = {'user_id': 123, 'ip': 3221226014}
        with patch('xenforo.middleware.connection') as mockdb:
            mockdb.cursor().fetchone.return_value = ['123', 'TestUser']
            self.middleware.process_request(self.request)
        self.assertEqual(self.request.xf_user_id, None)
        self.assertEqual(self.request.xf_user, None)

    def test_no_xf_user_row(self):
        self.request.META = {'HTTP_X_REAL_IP': '192.0.2.30',}
        self.request.xf_session = {'user_id': 123, 'ip': 3221226014}
        with patch('xenforo.middleware.connection') as mockdb:
            mockdb.cursor().fetchone.return_value = None
            self.middleware.process_request(self.request)
        self.assertEqual(self.request.xf_user_id, None)
        self.assertEqual(self.request.xf_user, None)
