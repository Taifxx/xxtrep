# -*- coding: utf-8 -*-
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
########## EXT:

### Import modules ...
import resources.lib.li      as LI
import resources.lib.dos     as DOS
import resources.lib.gui     as GUI
import resources.lib.comps   as CMP
import resources.lib.ctvsobj as CTVS
import resources.lib.addon   as addon
import resources.lib.lib     as lib 

from resources.lib.tools   import *
from resources.lib.tags    import *


### Set ...
LIB   = lib.libPaths(addon.libpath, TAG_PAR_LIB_FOLDER, addon.movFolder, addon.tvsFolder)

resetfol = lambda : LIB.setlib(addon.libpath, TAG_PAR_LIB_FOLDER, *addon.getlib())
   
### Remove tags in text ...
tl  = lambda textTag : CMP.compsRemtag(addon.tlraw(textTag)) if not addon.COLORIZE else addon.tlraw(textTag)
tla = lambda textTag : CMP.compsRemtag(addon.tlraw(textTag)) 
