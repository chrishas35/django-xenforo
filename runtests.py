#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=('django.contrib.auth', 'xenforo'),
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': os.path.join(BASE_DIR,'db_test.sqlite3')},},
        PASSWORD_HASHERS = [
            'xenforo.hashers.XenForoCore12PasswordHasher',
            'xenforo.hashers.XenForoSHA256PasswordHasher',
            'xenforo.hashers.XenForoSHA1PasswordHasher',
            'xenforo.hashers.VBulletinPasswordHasher',
        ]
    )
try:
    django.setup()
except AttributeError:
    pass

def runtests(args=None):
    import pytest

    if not args:
        args = []

    if not any(a for a in args[1:] if not a.startswith('-')):
        args.append('xenforo')

    sys.exit(pytest.main(args))


if __name__ == '__main__':
    runtests(sys.argv)
