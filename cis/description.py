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

"""This module defines the `Description` object.

All `Channel` name components can be annotated and described via edits
and extensions on the Channel Information System web interface.

The `Description` object extends a simple string name component with
the text included by a user of the CIS.
"""

from cis import version

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'
__version__ = version.__version__

import urllib2
import urlparse
import datetime
import dateutil.parser
import json
import textwrap

from . import connect

__all__ = ['Description', 'DescriptionDict']

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict


class Description(object):
    """Annotated `Channel` name component
    """
    def __init__(self, name, description=None, text=None, editor=None,
                 apiurl=None, cisid=None, modified=None, created=None):
        if isinstance(name, self.__class__):
            description = description or name.description
            text = text or name.text
            editor = editor or name.editor
            apiurl = apiurl or name.apiurl
            cisid = cisid or name.cisid
            modified = modified or name.modified
            created = created or name.created
        self.name = name
        self.description = description
        self.text = text
        self.editor = editor
        self.apiurl = apiurl
        self.cisid = cisid
        self.modified = modified
        self.created = created

    # ------------------------------------------------------------------------
    # -

    @property
    def name(self):
        """Name of this `Description`.

        :type: `str`
        """
        return self._name

    @name.setter
    def name(self, n):
        self._name = n and str(n) or None

    @property
    def description(self):
        """Human-readable (short) explanation of this `Description`.

        :type: `str`
        """
        return self._description

    @description.setter
    def description(self, desc):
        self._description = desc and str(desc) or None

    @property
    def text(self):
        """Extended explanation of this `Description`.

        :type: `str`
        """
        return self._text

    @text.setter
    def text(self, t):
        self._text = t and str(t) or None

    @property
    def editor(self):
        """Kerberos identity of author of last edit to this
        `Description`.

        :type: `str`
        """
        return self._editor

    @editor.setter
    def editor(self, ed):
        self._editor = ed and str(ed) or None

    @property
    def apiurl(self):
        """CIS web API URL for this `Description`.

        :type: `str`
        """
        return self._apiurl

    @apiurl.setter
    def apiurl(self, u):
        if u is not None:
            pieces = urlparse.urlparse(u)
            if not pieces.scheme or not pieces.netloc or not pieces.path:
                raise ValueError("Description API url '%s' invalid" % u)
        self._apiurl = u

    @property
    def cisid(self):
        """CIS unique identifier for this `Description`.

        :type: `int`
        """
        return self._cisid

    @cisid.setter
    def cisid(self, id_):
        self._cisid = id_ is not None and int(id_) or None

    @property
    def modified(self):
        """Last modified date for this `Description`.

        :type: :class:`datetime.datetime`
        """
        return self._modified

    @modified.setter
    def modified(self, date):
        if date is None:
            self._modified = date
        elif isinstance(date, datetime.datetime):
            self._modified = datetime
        else:
            self._modified = dateutil.parser.parse(date)

    @property
    def created(self):
        """Creation date for this `Description`.

        :type: :class:`datetime.datetime`
        """
        return self._created

    @created.setter
    def created(self, date):
        if date is None:
            self._created = date
        elif isinstance(date, datetime.datetime):
            self._created = datetime
        else:
            self._created = dateutil.parser.parse(date)

    # ------------------------------------------------------------------------
    # Description getters

    @classmethod
    def request(cls, url, debug=False):
        """Request information about a `Description` from the CIS

        Parameters
        ----------
        url : `str`
            HTTPS url for a description in the CIS
        debug : `bool`
            print HTTP information for debugging purposes,
            default: `False`

        Returns
        -------
        description : `Description`
            structured `Description` downloaded from CIS
        """
        try:
            response = connect.request(url, debug=debug)
        except urllib2.HTTPError:
            raise ValueError("No description found with URL '%s'" % url)
        reply = json.loads(response.read())
        return cls.from_json(reply)

    @classmethod
    def from_json(cls, jdata):
        """Construct a new `Description` from a JSON data `dict`

        Parameters
        ----------
        jdata : `dict`
            dict of (key, value) pairs of JSON data

        Returns
        -------
        description : `Description`
            structure `Description` formed from JSON data
        """
        name = jdata.pop('name', None)
        desc = jdata.pop('desc', None)
        cisid = jdata.pop('id', None)
        apiurl = jdata.pop('url', None)
        return Description(name, description=desc, cisid=cisid,
                           apiurl=apiurl, **jdata)

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.name:
            ind = ' ' * (len(self.__class__.__name__) + len(self.name) + 19)
            desc = self.description and "'%s'" % self.description or 'None'
            return textwrap.fill("<%s('%s', description=%s)>"
                                 % (self.__class__.__name__, self.name, desc),
                                 subsequent_indent=ind)
        else:
            return '<Description(None)>'


class DescriptionDict(OrderedDict):
    """Container for a set of (name, description) pairs describing
    a `Channel`.
    """
    def __str__(self):
        subind = ' ' * 1
        items = []
        for key,val in self.iteritems():
            subind = ' ' * (len(key) + 2)
            if val.text:
                desc = textwrap.fill('%s: %s,\n%s%s'
                                     % (key, val.description, subind, val.text),
                                     subsequent_indent=subind,
                                     replace_whitespace=False)
            else:
                desc = textwrap.fill('%s: %s' % (key, val.description),
                                     subsequent_indent=subind,
                                     replace_whitespace=False)

            items.append(desc)
        return '\n'.join(items)
