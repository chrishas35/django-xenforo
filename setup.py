#!/usr/bin/env python
from setuptools import setup, find_packages

import versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = 'xenforo/_version.py'
versioneer.versionfile_build = 'xenforo/_version.py'
versioneer.tag_prefix = '' # tags are like 1.2.0
versioneer.parentdir_prefix = 'xenforo-' # dirname like 'myproject-1.2.0'


setup(
	name = 'django-xenforo',
	version=versioneer.get_version(),
	description = 'A Django library to integrate with a XenForo forum.',

	author = 'Chris Hasenpflug',
	author_email = 'chris@hasenpflug.net',
	url = 'https://bitbucket.org/chrishas35/django-xenforo/overview',

	install_requires = [
		'Django>=1.5',
		'phpserialize',
		'django-appconf==0.6',
	],
	tests_require = [
		'pytest==2.5.1',
		'mock',
		'bcrypt==1.0.2',
	],
	test_suite = 'runtests.runtests',
	packages=find_packages(),
	zip_safe = False,
	cmdclass=versioneer.get_cmdclass(),

	classifiers = [
		'Development Status :: 2 - Pre-Alpha',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.3',
		'Topic :: Utilities',
		'Framework :: Django',
	]
)
