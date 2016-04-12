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
########## INFO:

### Import modules ...
import xbmc
import xbmcaddon

from resources.lib.deecode import *
from resources.lib.tags    import *

### Addon info ...
addon          = xbmcaddon.Addon(id=TAG_PAR_SCRIPT_ID)
profile        = de(xbmc.translatePath(addon.getAddonInfo('profile')))
localize       = addon.getLocalizedString
name           = addon.getAddonInfo('name')
id             = addon.getAddonInfo('id')
author         = addon.getAddonInfo('author')
version        = addon.getAddonInfo('version')
path           = de(addon.getAddonInfo('path'))
icon           = addon.getAddonInfo('icon')


### Translate tag to languare string ...
tlraw = lambda tag : e(localize(tag))   
    

### Convert string True result ...
_sbool = lambda sval : True if sval == 'true' else False

COLORIZE       = _sbool(addon.getSetting('colorize'))
UPDAFTER       = _sbool(addon.getSetting('updafter'))
ADDUPD         = _sbool(addon.getSetting('addupd'))
BGUPD          = _sbool(addon.getSetting('bgupd'))
LNKTIMEOUT     = int(addon.getSetting('lnktimeout'))
MNUITMNUM      = int(addon.getSetting('mnuitmnum'))
SETPAGE        = int(addon.getSetting('setpage'))
CALLURL        = _sbool(addon.getSetting('callurl'))

PLAYBCONT      = _sbool(addon.getSetting('playbcont'))         
POSUPD         = int(addon.getSetting('posupd'))   
POSSLEEP       = int(addon.getSetting('possleep')) 
WCHF           = _sbool(addon.getSetting('wchf'))   
WPERC          = int(addon.getSetting('wperc'))    
AUTORES        = _sbool(addon.getSetting('autores'))  
RESDLG         = _sbool(addon.getSetting('resdlg'))

SEEKAFTERBUF   = _sbool(addon.getSetting('seekafterbuf')) 

DETVIDEXT      = _sbool(addon.getSetting('detvidext'))  

movFolder      = addon.getSetting('fldrmov')
tvsFolder      = addon.getSetting('fldrtvs')

def getlib() : return addon.getSetting('fldrmov'), addon.getSetting('fldrtvs')
    
    