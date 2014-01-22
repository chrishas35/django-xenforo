from socket import inet_ntoa
from struct import pack
from time import time

from django.db import connection

import phpserialize


class XFSessionMiddleware(object):
    def process_request(self, request):
        request.xf_session_id = request.COOKIES.get('xf_session', None) # TODO: Setting for cookie name
        request.xf_session = None

        if not request.xf_session_id:
            return

        # TODO: pluggable SessionStores
        # TODO: Setting for table prefix
        # TODO: Setting for custom database
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM xf_session WHERE session_id = %s AND expiry_date >= %s", [request.xf_session_id, int(time())])
        row = cursor.fetchone()

        if row:
            request.xf_session = phpserialize.unserialize(row[1])


class XFAuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'xf_session'), "The XenForo authentication middleware requires the XF session middleware to be installed."

        request.xf_user_id = None
        request.xf_user = None

        if not request.xf_session:
            return

        xf_session_ip = inet_ntoa(pack("!L", request.xf_session.get('ip', None)))

        if xf_session_ip != request.META['HTTP_X_REAL_IP']: #TODO: Setting for IP matching
            return

        lookup_user_id = int(request.xf_session.get('user_id', None))
        # TODO: Setting for table prefix
        # TODO: Setting for custom database
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM xf_user WHERE user_id = %s", [lookup_user_id])

        request.xf_user = cursor.fetchone() # TODO: Convert list to dict

        if request.xf_user:
            request.xf_user_id = int(request.xf_user[0])
