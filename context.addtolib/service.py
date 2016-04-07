#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2016 Taifxx
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.

# modules
import os
import time
import xbmc
import xbmcaddon
import xbmcvfs
import lib.common

### get addon info
__addon__        = lib.common.__addon__
__addonpath__    = lib.common.__addonpath__
__localize__     = lib.common.__localize__
__addonname__    = lib.common.__addonname__
__version__      = lib.common.__version__
__addonprofile__ = lib.common.__addonprofile__

#import libraries
#from lib.settings import get
#from lib.utils import log
#setting = get()

# starts update/sync
def autostart(): pass             

if (__name__ == "__main__"): autostart()