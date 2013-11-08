# -*- coding: utf-8 -*-
# Copyright (C) Duncan Macleod (2013)
#
# This file is part of LIGO-CIS
#
# LIGO-CIS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LIGO-CIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LIGO-CIS.  If not, see <http://www.gnu.org/licenses/>

"""This module provides LIGO.ORG authenticated HTML queries
"""

import os
import stat
import urllib2
import tempfile
import cookielib

from glue.auth.saml import HTTPNegotiateAuthHandler

from . import version

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'
__credits__ = 'Scott Koranda <scott.koranda@ligo.org>'
__version__ = version.__version__

TMPDIR = tempfile.gettempdir()

COOKIE_JAR = os.path.join(TMPDIR, '%s_cookies' % os.getenv('USER'))
LIGO_LOGIN_URL = 'login.ligo.org'


def request(url, debug=False):
    """Request the given URL using LIGO.ORG SAML authentication.

    This requires an active Kerberos ticket for the user, to get one:

    .. code:: bash

       kinit albert.einstein@LIGO.ORG

    Parameters
    ----------
    url : `str`
        URL path for request
    debug : `bool`, optional
        Query in verbose debugging mode, default: `False`

    Returns
    -------
    response : `str`
        output of HTTP request
    """
    # set debug to 1 to see all HTTP(s) traffic
    debug = int(debug)

    # need an instance of HTTPS handler to do HTTPS
    httpshandler = urllib2.HTTPSHandler(debuglevel=debug)

    # use a cookie jar to store session cookies
    jar = cookielib.LWPCookieJar()

    # if a cookier jar exists open it and read the cookies
    # and make sure it has the right permissions
    if os.path.exists(COOKIE_JAR):
        os.chmod(COOKIE_JAR, stat.S_IRUSR | stat.S_IWUSR)

        # set ignore_discard so that session cookies are preserved
        jar.load(COOKIE_JAR, ignore_discard=True)

    # create a cookie handler from the cookier jar
    cookiehandler = urllib2.HTTPCookieProcessor(jar)
    # need a redirect handler to follow redirects
    redirecthandler = urllib2.HTTPRedirectHandler()

    # need an auth handler that can do negotiation.
    # input parameter is the Kerberos service principal.
    principal = 'HTTP@%s' % LIGO_LOGIN_URL
    authhandler = HTTPNegotiateAuthHandler(service_principal=principal)

    # create the opener.
    opener = urllib2.build_opener(authhandler, cookiehandler, httpshandler,
                                  redirecthandler)

    # prepare the request object
    req = urllib2.Request(url)

    # use the opener and the request object to make the request.
    response = opener.open(req)

    # save the session cookies to a file so that they can
    # be used again without having to authenticate
    jar.save(COOKIE_JAR, ignore_discard=True)

    return response