﻿# -*- coding: utf-8 -*-
#
#     Copyright (C) 2016 Taifxx
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
########## LIB:

import resources.lib.dos   as DOS

### Set library folders names ...
class libPaths:
    
    def __init__(self, addon, libFolder):
        self.addon     = addon
        self.libFolder = libFolder 
        
    @property 
    def lib  (self) : return DOS.join(self.addon.libpath, self.libFolder)
    @property 
    def mov  (self) : return DOS.join(self.addon.libpath, self.libFolder, self.addon.movFolder)
    @property 
    def tvsf (self) : return DOS.join(self.addon.libpath, self.libFolder, self.addon.tvsFolder) 
    
    tvs = lambda self, path : DOS.join(self.tvsf, path)
