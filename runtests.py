#!/usr/bin/env python
import sys

from django.conf import settings

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=('django.contrib.auth', 'xenforo'),
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
    )


def runtests(args=None):
    import pytest

    if not args:
        args = []

    if not any(a for a in args[1:] if not a.startswith('-')):
        args.append('xenforo')

    sys.exit(pytest.main(args))


if __name__ == '__main__':
    runtests(sys.argv)
