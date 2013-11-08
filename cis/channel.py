# -*- coding: utf-8 -*-
# Copyright (C) Duncan Macleod (2013)
#
# This file is part of LIGO-CIS.
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
# along with LIGO-CIS.  If not, see <http://www.gnu.org/licenses/>.

"""Representation of an instrumental LIGO signal channel
"""

import re
import os
import numpy
import json
import datetime
import dateutil.parser
import urlparse
import textwrap
from urllib2 import HTTPError

from . import (connect, version, description)

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"
__version__ = version.__version__

__all__ = ['Channel', 'ChannelList']

_re_ifo = re.compile("[A-Z]\d:")
_re_cchar = re.compile("[-_]")

DATA_TYPE_ENUM = {0: None,
                  1: numpy.int16,
                  2: numpy.int32,
                  3: numpy.int64,
                  4: numpy.float32,
                  5: numpy.double,
                  6: numpy.complex64,
                  }

CHANNEL_API_URL = 'https://cis.ligo.org/api/channel'


class Channel(object):
    """Representation of a LIGO data channel.

    Each `Channel` represents a single time-series signal generated
    during operation or characterisation of a LIGO instrument.

    Parameters
    ----------
    ch : `str`, `Channel`
        name of this Channel (or another  Channel itself).
        If a `Channel` is given, all other parameters not set explicitly
        will be copied over.
    sample_rate : `float`, optional
        number of samples per second
    unit : :class:`~astropy.units.core.Unit`, `str`, optional
        name of the unit for the data of this channel
    dtype : `numpy.dtype`, optional
        numeric type of data for this channel
    model : `str`, optional
        name of the SIMULINK front-end model that produces this `Channel`
    """
    def __init__(self, ch, sample_rate=None, unit=None, dtype=None,
                 frametype=None, model=None, url=None, apiurl=None,
                 cisid=None, description=None, descriptions=None,
                 created=None):
        # test for Channel input
        if isinstance(ch, Channel):
            sample_rate = sample_rate or ch.sample_rate
            unit = unit or ch.unit
            dtype = dtype or ch.dtype
            frametype = frametype or ch.frametype
            model = model or ch.model
            url = url or ch.url
            apiurl = apiurl or ch.apiurl
            cisid = cisid or ch.cisid
            created = created or ch.created
            description = description or ch.description
            descriptions = descriptions or ch.descriptions
            ch = ch.name
        # set attributes
        self.descriptions = descriptions
        self.name = ch
        self.description = description
        self.sample_rate = sample_rate
        self.unit = unit
        self.frametype = frametype
        self.dtype = dtype
        self.model = model
        self.url = url
        self.apiurl = apiurl
        self.cisid = cisid
        self.created = created

    @property
    def name(self):
        """Name of this `Channel`.

        This should follow the naming convention, with the following
        format: 'IFO:SYSTEM-SUBSYSTEM_SIGNAL'

        :type: `str`
        """
        return self._name

    @name.setter
    def name(self, n):
        self._name = n
        self.parse_name(n)

    @property
    def description(self):
        """Description of this `Channel`.

        :type: :class:`~cis.description.Description`
        """
        return self._description

    @description.setter
    def description(self, text):
        if text is not None:
            self._description = description.Description(text)
        else:
            self._description = text

    @property
    def ifo(self):
        """Interferometer prefix for this `Channel`, e.g `H1`.

        :type: `str`
        """
        return self._ifo

    @property
    def system(self):
        """Instrumental system for this `Channel`, e.g `PSL`
        (pre-stabilised laser).

        :type: `Description`
        """
        return self._system

    @property
    def subsystem(self):
        """Instrumental sub-system for this `Channel`, e.g `ISS`
        (pre-stabiliser laser intensity stabilisation servo).

        :type: :class:`~cis.description.Description`
        """
        return self._subsystem

    @property
    def signal(self):
        """Instrumental signal for this `Channel`, relative to the
        system and sub-system, e.g `FIXME`.

        :type: :class:`~cis.description.Description`
        """
        return self._signal

    @property
    def sample_rate(self):
        """Rate of samples (Hertz) for this `Channel`.

        :type: `float`
        """
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, rate):
        self._sample_rate = float(rate)

    @property
    def unit(self):
        """Data unit for this `Channel`.

        :type: `str`
        """
        return self._unit

    @unit.setter
    def unit(self, u):
        if u is None:
            self._unit = None
        else:
            self._unit = str(u)

    @property
    def model(self):
        """Name of the SIMULINK front-end model that defines this
        `Channel`.

        :type: `str`
        """
        return self._model

    @model.setter
    def model(self, mdl):
        self._model = mdl and mdl.lower() or mdl

    @property
    def dtype(self):
        """Numeric type for data in this `Channel`.

        :type: :class:`numpy.dtype`
        """
        return self._dtype

    @dtype.setter
    def dtype(self, type_):
        if isinstance(type_, int):
            type_ = DATA_TYPE_ENUM[type_]
        self._dtype = numpy.dtype(type_)

    @property
    def created(self):
        """Creation datetime for this `Channel`.

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

    @property
    def url(self):
        """CIS browser URL for this `Channel`.

        :type: `str`
        """
        return self._url

    @url.setter
    def url(self, u):
        if u is not None:
            pieces = urlparse.urlparse(u)
            if not pieces.scheme or not pieces.netloc or not pieces.path:
                raise ValueError("Description url '%s' invalid" % u)
        self._url = u

    @property
    def apiurl(self):
        """CIS web API URL for this `Channel`.

        :type: `str`
        """
        return self._apiurl

    @apiurl.setter
    def apiurl(self, u):
        if u is not None:
            pieces = urlparse.urlparse(u)
            if not pieces.scheme or not pieces.netloc or not pieces.path:
                raise ValueError("Description url '%s' invalid" % u)
        self._apiurl = u

    def __str__(self):
        return self.name

    def __repr__(self):
        stub = self.__class__.__name__
        indent = ' ' * (len(stub) + 2)
        name = textwrap.fill(self.name, subsequent_indent=indent)
        repr_ = '<%s("%s"' % (stub, name)
        if self.description:
            dstub = 'description='
            subind = indent + ' ' * (len(dstub) + 1)
            description = textwrap.fill('%s"%s"'
                                        % (dstub,
                                           self.description.description),
                                        initial_indent=indent,
                                        subsequent_indent=subind)
            repr_ += ',\n%s' % str(description)
        repr_ += ',\n%ssample_rate=%s' % (indent, repr(self.sample_rate))
        repr_ = '%s)>' % repr_
        if len(repr_) < 79:
            return re.sub('\n\s+', ' ', repr_)
        else:
            return repr_

    @property
    def tex_name(self):
        """Name of this `Channel` in LaTeX printable format
        """
        return str(self).replace("_", r"\_")

    @classmethod
    def query(cls, name, descriptions=True, debug=False):
        """Query the LIGO Channel Information System for the `Channel`
        matching the given name

        Parameters
        ----------
        name : `str`
            name of channel
        descriptions : `bool`
            download descriptions of all name parts for this `Channel`
        debug : `bool`, optional
            print verbose HTTP connection status for debugging,
            default: `False`

        Returns
        -------
        Channel
             a new `Channel` containing all of the attributes set from
             its entry in the CIS
        """
        channellist = ChannelList.query(name, descriptions=descriptions,
                                        debug=debug)
        if len(channellist) == 0:
            raise ValueError("No channels found matching '%s'." % name)
        if len(channellist) > 1:
            raise ValueError("%d channels found matching '%s', please refine "
                             "search, or use `ChannelList.query` to return "
                             "all results." % (len(channellist), name))
        return channellist[0]

    @classmethod
    def from_json(cls, jdata):
        """Generate a new channel from JSON data

        Parameters
        ----------
        jdata : `dict`
            dict of (key, value) pairs recovered from CIS REST request

        Returns
        -------
        channel : `Channel`
            newly formed channel with attributes mapped from ``jdata``
        """
        name = jdata.get('name', None)
        sample_rate = jdata.get('datarate', None)
        unit = jdata.get('units', None)
        dtype = jdata.get('datatype', None)
        url = jdata.get('displayurl', None)
        apiurl = jdata.get('url', None)
        model = jdata.get('source', None)
        created = jdata.get('created', None)
        return cls(name, sample_rate=sample_rate, unit=unit, dtype=dtype,
                   model=model, url=url, apiurl=apiurl, created=created)

    def parse_name(self, name):
        """Decompose a `Channel` name string into its components
        """
        if not name:
            return
        # set up Description type cast
        from .description import Description
        def as_description(attr, value):
            if not attr.startswith('_'):
                attr = '_%s' % attr
            if value is None:
                setattr(self, attr, None)
            elif self.descriptions and value in self.descriptions:
                setattr(self, attr, self.descriptions[value])
            else:
                setattr(self, attr, Description(value))
        # parse ifo
        if _re_ifo.match(name):
            ifo, name = name.split(":", 1)
            as_description('ifo', ifo)
        else:
            self._ifo = None
        # parse systems
        tags = _re_cchar.split(name, maxsplit=2)
        as_description('system', tags[0])
        if len(tags) > 1:
            as_description('subsystem', tags[1])
        else:
            self._subsystem = None
        if len(tags) > 2:
            as_description('signal', tags[2])
        else:
            self._signal = None
        return self.ifo, self.system, self.subsystem, self.signal

    def get_descriptions(self, url=None, debug=False):
        """Download all the descriptions associated with this
        `Channel`.

        Parameters
        ----------
        url : `str`
            HTTP url for the descriptions entry in the CIS API,
            default: self.url/descriptions
        debug : `bool`, optional
            print verbose HTTP connection status for debugging,
            default: `False`

        Returns
        -------
        descriptions : `list`
            a list of all descriptions associated with this `Channel`

        Notes
        -----
        If a set of descriptions is successfully downloaded from the CIS,
        the string name attributes of the host `Channel` will be replaced
        with the corresponding `Description` if possible.
        """
        from .description import Description
        if url is None:
            url = os.path.join(self.apiurl, 'descriptions')
        try:
            response = connect.request(url, debug=debug)
        except HTTPError:
            raise ValueError("No descriptions found at URL '%s'" % url)
        reply = json.loads(response.read())
        self.descriptions = description.DescriptionDict(
                                (d.name, d) for d in
                                 map(Description.from_json, reply))
        for attr in ['ifo', 'system', 'subsystem', 'signal']:
            if attr in self.descriptions:
                setattr(self, attr, self.descriptions[attr])
        namestub = self.name.split(':', 1)[1]
        if not self.description and namestub in self.descriptions:
            self.description = self.descriptions[namestub]
        try:
            ddict = self.descriptions
            self.descriptions = ddict.__class__(sorted(
                ddict.iteritems(), key=lambda (d,v): v.name in self.name
                                                     and self.name.index(v.name)
                                                     or 1000))
        except AttributeError:
            pass
        return self.descriptions


class ChannelList(list):
    """A list of Channels, with parsing/sieveing utilities.
    """
    def find(self, name):
        """Find the `Channel` with the given name in this `ChannelList`.

        Parameters
        ----------
        name : `str`
            name of the `Channel` to find

        Returns
        -------
        idx : `int`
            returns the position of the first `Channel` in self
            whose name matches the input

        Raises
        ------
        ValueError if no such element exists.
        """
        for i, chan in enumerate(self):
            if name == chan.name:
                return i
        raise ValueError(name)

    def sieve(self, name=None, sample_rate=None, sample_range=None,
              exact_match=False):
        """Find all `Channel`\_s in this list that match the specified
        criteria.

        Parameters
        ----------
        name : `str`, or regular expression
            any part of the channel name against which to match
            (or full name if `exact_match=False` is given)
        sample_rate : `float`
            rate (number of samples per second) to match exactly
        sample_range : 2-`tuple`
            `[low, high]` closed interval or rates to match within
        exact_match : `bool`
            return channels matching `name` exactly, default: `False`

        Returns
        -------
        new : `ChannelList`
            a new `ChannelList` containing the matching channels
        """
        # format name regex
        if isinstance(name, re._pattern_type):
            flags = name.flags
            name = name.pattern
        else:
            flags = 0
        if exact_match:
            name = name.startswith('\\A') and name or r"\A%s" % name
            name = name.endwith('\\Z') and name or r"%s\Z" % name
        name_regexp = re.compile(name, flags=flags)
        c = list(self)
        if name is not None:
            c = [entry for entry in c if
                 name_regexp.search(entry.name) is not None]
        if sample_rate is not None:
            c = [entry for entry in c if
                 float(entry.sample_rate) == sample_rate]
        if sample_range is not None:
            c = [entry for entry in c if
                 sample_range[0] <= float(entry.sample_rate) <=
                 sample_range[1]]

        return self.__class__(c)

    @classmethod
    def query(cls, name, descriptions=True, debug=False):
        """Query the LIGO Channel Information System a `ChannelList`
        of entries matching the given name regular expression.

        Parameters
        ----------
        name : `str`
            name of channel, or part of it.
        descriptions : `bool`
            download all descriptions from CIS along with each Channel,
            default: `True`
        debug : `bool`, optional
            print verbose HTTP connection status for debugging,
            default: `False`

        Returns
        -------
        `ChannelList`
        """
        out = cls()
        url = '%s/?q=%s' % (CHANNEL_API_URL, re.sub('[\*\s]', r'%20', name))
        more = True
        while more:
            try:
                response = connect.request(url, debug=debug)
            except HTTPError:
                raise ValueError("Channel named '%s' not found in Channel "
                                 "Information System. Please double check "
                                 "the name and try again." % name)
            reply = json.loads(response.read())
            if 'results' in reply:
                for jdata in reply[u'results']:
                    c = Channel.from_json(jdata)
                    if descriptions:
                        c.get_descriptions(debug=debug)
                        c.parse_name(c.name)
                    out.append(c)
            more = 'next' in reply and reply['next'] is not None
            if more:
                url = reply['next']
            else:
                break
        out.sort(key=lambda c: c.name)
        return out

    @property
    def ifos(self):
        return set([c.ifo for c in self])
