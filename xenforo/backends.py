from django.db import connections

from django.contrib.auth import get_user_model

import phpserialize

from .conf import settings
from .utils import dictfetchall


class XFAuthBackend(object):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        """
        We're here either beacause the user was not found in the Django's user
        model, or the password did not match.  This authentication will create
        or update the Django row and reattempt authentication.
        """
        print('In XFAuthBackend.authenticate')

        if username is None:
            return None

        UserModel = get_user_model()

        cursor = connections[settings.XENFORO_DATABASE].cursor()
        cursor.execute("""SELECT u.user_id, u.username, auth.scheme_class, auth.data
                          FROM {prefix}user AS u, {prefix}user_authenticate AS auth
                          WHERE u.username = %s
                            AND auth.user_id = u.user_id""".format(prefix=settings.XENFORO_TABLE_PREFIX),
                       username)
        try:
            row = dictfetchall(cursor)[0]
        except IndexError:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
            return None
        finally:
            cursor.close()

        user, created = UserModel.objects.get_or_create(**{
            UserModel.USERNAME_FIELD: username,
            'defaults': {'pk': row['user_id'],
                         'is_staff': True,
                         'is_superuser': True,
                         'password': 'xenforo_core12${0}'.format(phpserialize.unserialize(row['data'], decode_strings=True)['hash'])
                        }
        })

        if not created:
            user.password = 'xenforo_core12${0}'.format(phpserialize.unserialize(row['data'], decode_strings=True)['hash'])
            user.save()

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
