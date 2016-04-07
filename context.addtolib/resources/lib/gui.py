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
########## GUI:

### Import modules ...
import xbmc
import xbmcgui
import resources.lib.addon as addon

from resources.lib.const   import *
from resources.lib.tags    import *


### Defaults ...
defCaption = addon.name
#defCaption = Empty
defScript  = TAG_PAR_SCRIPT_ID
#defScript  = Empty

### Message ...
notInfo    = xbmcgui.NOTIFICATION_INFO
notWarning = xbmcgui.NOTIFICATION_WARNING

msg       = lambda title,    text=Empty,                                 : xbmc.executebuiltin('Notification(%s,%s)' % (title, text))
msgf      = lambda title,    text=Empty, nottype=notInfo                 : xbmcgui.Dialog().notification(title, text, nottype)

### Dialogs ...
dlgOk     = lambda text1,   text2=Empty, title=defCaption                : xbmcgui.Dialog().ok   (title, text1, text2)
dlgYn     = lambda text1,   text2=Empty, title=defCaption                : xbmcgui.Dialog().yesno(title, text1, text2) 
dlgIn     = lambda                       title=defCaption, default=Empty : xbmcgui.Dialog().input(title, default)
dlgInnum  = lambda                       title=defCaption, default=Empty : xbmcgui.Dialog().numeric(0, title, default)
dlgSel    = lambda sargs,                title=defCaption                : xbmcgui.Dialog().select(title, sargs)

def dlgSelmul (sargs, selMark, title=defCaption, selDef=None):
    idx       = 0
    marksList = dict()
    resList   = []
    
    if selDef:
        for idx, itm in enumerate(sargs):
            if itm in selDef : marksList.update({idx:selMark}); resList.append(idx) 
     
    while idx != -1:
        sargsList = []
        for aidx, arg in enumerate(sargs) : sargsList.append(marksList.get(aidx, Empty) + arg)
        
        idx = dlgSel(sargsList, title)  
        if idx == len(sargsList) - 1 : idx = -1 
        if idx != -1 :
            if  marksList.get (idx, False):
                resList.remove(idx)
                marksList.pop (idx)
            else:
                resList.append(idx)
                marksList.update({idx:selMark})
             
    return resList

### Actions ...
back      = lambda      : xbmc.executebuiltin('Action(Back)', True)
refresh   = lambda      : xbmc.executebuiltin('Container.Refresh')
libUpdate = lambda      : xbmc.executebuiltin('UpdateLibrary(video)', True)
libClean  = lambda      : xbmc.executebuiltin('CleanLibrary(video)', True)
openSet   = lambda      : xbmc.executebuiltin('Addon.OpenSettings(%s)' % (defScript), True)
goTarget  = lambda link : xbmc.executebuiltin('container.update(%s)' % (link))