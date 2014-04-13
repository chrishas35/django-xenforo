# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

from ..utils import convert_to_django_password

class TestUtils(TestCase):

    def test_core12(self):
        scheme_class = 'XenForo_Authentication_Core12'
        data = b'a:1:{s:4:"hash";s:60:"$2a$10$EnvKvs.royUb7HV2lBGAROLdwbghtS4KBlaDrkFoFa3sIAmPn6gk6";}'
        self.assertEqual(
            convert_to_django_password(scheme_class, data),
            'xenforo_core12$$2a$10$EnvKvs.royUb7HV2lBGAROLdwbghtS4KBlaDrkFoFa3sIAmPn6gk6'
        )

    def test_core_sha256(self):
        scheme_class = 'XenForo_Authentication_Core'
        data = b'a:3:{s:4:"hash";s:64:"38d61fda7efdc4122b3a5a36f2a548ec72bd013a9ce05b4404f412b00089517a";s:4:"salt";s:7:"seasalt";s:8:"hashFunc";s:6:"sha256";}'
        self.assertEqual(
            convert_to_django_password(scheme_class, data),
            'xenforo_sha256$seasalt$38d61fda7efdc4122b3a5a36f2a548ec72bd013a9ce05b4404f412b00089517a'
        )

    def test_core_sha1(self):
        scheme_class = 'XenForo_Authentication_Core'
        data = b'a:3:{s:4:"hash";s:40:"ccb1e9f3865a8f03a26b8d7f76139268f5d1e9e6";s:4:"salt";s:7:"seasalt";s:8:"hashFunc";s:4:"sha1";}'
        self.assertEqual(
            convert_to_django_password(scheme_class, data),
            'xenforo_sha1$seasalt$ccb1e9f3865a8f03a26b8d7f76139268f5d1e9e6'
        )

    def test_vbulletin_md5(self):
        scheme_class = 'XenForo_Authentication_vBulletin'
        data = b'a:2:{s:4:"hash";s:32:"2800981dde706669ac6e5fb521e2b44b";s:4:"salt";s:3:"abc";}'
        self.assertEqual(
            convert_to_django_password(scheme_class, data),
            'vbulletin_md5$abc$2800981dde706669ac6e5fb521e2b44b'
        )
