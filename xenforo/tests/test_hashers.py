# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase, skipUnless

from django.contrib.auth.hashers import (is_password_usable,
    check_password, load_hashers, make_password, identify_hasher)

try:
    import bcrypt
except ImportError:
    bcrypt = None

class TestHashers(TestCase):
    def test_xenforo_sha256(self):
        encoded = make_password('lètmein', 'seasalt', 'xenforo_sha256')
        self.assertEqual(encoded,
            'xenforo_sha256$seasalt$38d61fda7efdc4122b3a5a36f2a548ec72bd013a9ce05b4404f412b00089517a')
        self.assertTrue(is_password_usable(encoded))
        self.assertTrue(check_password('lètmein', encoded))
        self.assertFalse(check_password('lètmeinz', encoded))
        self.assertEqual(identify_hasher(encoded).algorithm, 'xenforo_sha256')

    def test_xenforo_sha1(self):
        encoded = make_password('lètmein', 'seasalt', 'xenforo_sha1')
        self.assertEqual(encoded,
            'xenforo_sha1$seasalt$ccb1e9f3865a8f03a26b8d7f76139268f5d1e9e6')
        self.assertTrue(is_password_usable(encoded))
        self.assertTrue(check_password('lètmein', encoded))
        self.assertFalse(check_password('lètmeinz', encoded))
        self.assertEqual(identify_hasher(encoded).algorithm, 'xenforo_sha1')

    def test_vbulletin_md5(self):
        encoded = make_password('lètmein', 'seasalt', 'vbulletin_md5')
        self.assertEqual(encoded,
            'vbulletin_md5$seasalt$6716dd6290166333cdac9748cd33b326')
        self.assertTrue(is_password_usable(encoded))
        self.assertTrue(check_password('lètmein', encoded))
        self.assertFalse(check_password('lètmeinz', encoded))
        self.assertEqual(identify_hasher(encoded).algorithm, 'vbulletin_md5')

    @skipUnless(bcrypt, "bcrypt not installed")
    def test_xenforo_core12(self):
        encoded = make_password('lètmein', hasher='xenforo_core12')
        self.assertTrue(is_password_usable(encoded))
        self.assertTrue(encoded.startswith('xenforo_core12$'))
        self.assertTrue(check_password('lètmein', encoded))
        self.assertFalse(check_password('lètmeinz', encoded))
        self.assertEqual(identify_hasher(encoded).algorithm, "xenforo_core12")

        # XenForo generated hash
        self.assertTrue(check_password('lètmein',
            'xenforo_core12$$2a$10$EnvKvs.royUb7HV2lBGAROLdwbghtS4KBlaDrkFoFa3sIAmPn6gk6'))
