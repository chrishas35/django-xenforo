from django.conf import settings

from appconf import AppConf


class XenforoConf(AppConf):
	COOKIE_PREFIX = 'xf_'
	DATABASE = 'default'
	IP_ADDRESS_KEY = 'HTTP_X_REAL_IP'
	TABLE_PREFIX = 'xf_'
	PASSWORD_ITERATIONS = 10

	class Meta:
		prefix = 'xenforo'
