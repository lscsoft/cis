#!/usr/bin/env python

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

import glob
from setuptools import (find_packages, setup)

from utils import version

VERSION_PY = 'cis/version.py'

# set version information
vcinfo = version.GitStatus()
vcinfo(VERSION_PY)

PACKAGENAME = 'cis'
DESCRIPTION = 'LIGO Channel Information System Client'
LONG_DESCRIPTION = ''
AUTHOR = 'Brian Moe, Chris Pankow, Duncan Macleod'
AUTHOR_EMAIL = None
LICENSE = 'GPLv3'

# VERSION should be PEP386 compatible (http://www.python.org/dev/peps/pep-0386)
VERSION = vcinfo.version

# Indicates if this version is a release version
RELEASE = vcinfo.version != vcinfo.id and 'dev' not in VERSION

# Use the find_packages tool to locate all packages and modules
packagenames = find_packages(exclude=['utils'])

# find all scripts
scripts = glob.glob('bin/*')

setup(name=PACKAGENAME,
      version=VERSION,
      description=DESCRIPTION,
      scripts=scripts,
      packages=packagenames,
      ext_modules=[],
      requires=['numpy', 'glue', 'kerberos'],
      provides=[PACKAGENAME],
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      long_description=LONG_DESCRIPTION,
      zip_safe=False,
      use_2to3=True
      )
