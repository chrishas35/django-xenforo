from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

default_app_config = 'xenforo.apps.XenforoConfig'