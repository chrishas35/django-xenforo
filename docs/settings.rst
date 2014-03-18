.. _settings:

Settings
========

.. currentmodule:: django.conf.settings

Django-XenForo has a number of settings that control its behavior. They've been
given defaults that match a standard XenForo install. If you've altered your
XenForo config, then you'll want to modify these as appropriate in your
project's settings.py.

.. attribute:: COOKIE_PREFIX

	:default: ``'xf_'``
	:type: String

	The prefix of the XenForo cookie.

	This is used by ``middleware.XFSessionMiddleware`` to fetch the user's
	session cookie.

.. attribute:: DATABASE

	:default: ``'default'``
	:type: String

	The :django:setting:`DATABASES` connection to use for querying the
	XenForo database.

.. attribute:: IP_ADDRESS_KEY

	:default: ``'HTTP_X_REAL_IP'``
	:type: String

	The HTTP Header is looked at for IP address comparison in
	``middleware.XFAuthenticationMiddleware``.

.. attribute:: TABLE_PREFIX

	:default: ``'xf_'``
	:type: String

	The prefix for tables in the XenForo database.

	Used throughout the app for querying against the XenForo database.