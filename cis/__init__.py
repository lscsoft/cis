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

"""The LIGO Channel Information System (CIS) client

The CIS documents and archives information about data signals
('channels') used and recorded by the Laser Interferometer
Gravitational-wave Observatory (LIGO) instruments.

These channels are any of instrumental error and control signals, and
environmental sensor readings.

The CIS records information on naming, data rate, physical unit, and
source within the instrument. See the :class:`~cis.channel.Channel`
documentation for full details.
"""

from cis import version
__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'
__version__ = version.__version__

from .channel import *
from .description import *
