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
########## LI:

### Import modules ...
import xbmc

from resources.lib.const   import * 
from resources.lib.tools   import *

### Items ...
#currentItemPos = int(xbmc.getInfoLabel('Container.CurrentItem'))
#itemsCount     = int(xbmc.getInfoLabel('Container.NumItems'))
currentItemPos = lambda : inte(xbmc.getInfoLabel('Container.CurrentItem'))
itemsCount     = lambda : int(xbmc.getInfoLabel('Container.NumItems'))

### Container info ...
getCpath       = lambda : xbmc.getInfoLabel('Container.FolderPath')
getCname       = lambda : xbmc.getInfoLabel('Container.FolderName')
getCplug       = lambda : xbmc.getInfoLabel('Container.PluginName')

### Listitem info ...
getLi          = lambda infolabel, idx=currentItemPos() : xbmc.getInfoLabel('ListitemNoWrap(%s).%s' % (str(idx-currentItemPos()), infolabel))

getIcn         = lambda            idx=currentItemPos() : getLi('Icon',            idx)
getTbn         = lambda            idx=currentItemPos() : getLi('Thumb',           idx)
getLink        = lambda            idx=currentItemPos() : getLi('FileNameAndPath', idx)
getPath        = lambda            idx=currentItemPos() : getLi('Path',            idx)
getFname       = lambda            idx=currentItemPos() : getLi('FileName',        idx)
getFolpath     = lambda            idx=currentItemPos() : getLi('FolderPath',      idx)
getTitle       = lambda            idx=currentItemPos() : getLi('Label',           idx)

def isFolder (idx=currentItemPos()): 
    return True if getLi('Property(IsPlayable)',idx) in ('false', Empty) and not getFname(idx) else False 

### Listitems Object ...
class vidItems:

    def __init__(self):
        
        ## Current listitem data ...
        self.vidFolderNameDef = Empty
        self.vidCurr          = getTitle()
        self.vidPath          = getPath()
        self.vidIsFolder      = isFolder()
        self.vidFPath         = getFolpath()
        self.vidLink          = getLink()
        self.vidCPath         = getCpath()
        self.vidCName         = getCname()
        self.vidCPlug         = getCplug()
        self.vidIsEmpty       = True
        self.vidFolCount      = itemsCount() 
        ## Local items list...
        self.vidListItems     = []
        
        ## If current item is not a folder, set it as default ...
        if not self.vidIsFolder : self.vidFolderNameDef = self.vidCurr
            
        ## Create items list ...
        for idx in range(1, self.vidFolCount+1):
            if isFolder(idx) : continue
            self.vidListItems.append([getTitle(idx), getLink(idx)])
            
        if self.vidListItems : 
            self.vidIsEmpty = False
            ## Set as default first nofolder item, if current item is a folder ...
            if self.vidFolderNameDef == Empty : self.vidFolderNameDef = self.vidListItems[0][0] 