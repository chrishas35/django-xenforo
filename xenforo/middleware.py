from socket import inet_ntoa
from struct import pack
from time import time

from django.db import connections

import phpserialize

from .conf import settings


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


class XFSessionMiddleware(object):
    def process_request(self, request):
        request.xf_session_id = request.COOKIES.get(settings.XENFORO_COOKIE_PREFIX + 'session', None)
        request.xf_session = None

        if not request.xf_session_id:
            return

        # TODO: pluggable SessionStores
        cursor = connections[settings.XENFORO_DATABASE].cursor()
        cursor.execute("SELECT session_id, session_data, expiry_date FROM " + settings.XENFORO_TABLE_PREFIX + "session WHERE session_id = %s AND expiry_date >= %s",
            [request.xf_session_id, int(time())])
        row = cursor.fetchone()
        cursor.close()

        if row:
            request.xf_session = phpserialize.unserialize(row[1], decode_strings=True)


class XFAuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'xf_session'), "The XenForo authentication middleware requires the XF session middleware to be installed."

        request.xf_user_id = None
        request.xf_user = None

        if not request.xf_session:
            return

        if 'user_id' not in request.xf_session:
            return

        if 'ip' not in request.xf_session:
            return

        xf_session_ip = inet_ntoa(pack("!L", request.xf_session.get('ip')))

        if xf_session_ip != request.META[settings.XENFORO_IP_ADDRESS_KEY]:
            return

        lookup_user_id = int(request.xf_session.get('user_id'))

        cursor = connections[settings.XENFORO_DATABASE].cursor()
        cursor.execute("SELECT * FROM " + settings.XENFORO_TABLE_PREFIX + "user WHERE user_id = %s",
            [lookup_user_id])

        request.xf_user = dictfetchall(cursor)[0]
        cursor.close()

        if request.xf_user:
            request.xf_user_id = int(request.xf_user['user_id'])
