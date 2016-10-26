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
########## LI2 (JSP):

### Import modules ...
from base import *

DETVIDEXT = False

### Items ...
currentItemPos = lambda : inte(xbmc.getInfoLabel('Container.CurrentItem'))
itemsCount     = lambda : inte(xbmc.getInfoLabel('Container.NumItems'))

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

getTitleF      = lambda            idx=currentItemPos() : getLi('Label',           idx)
# def getTitleF (idx=currentItemPos()):
#     tmpTitle = getTitle(idx)
#     tmpFname = getFname(idx)
#     return tmpFname if tmpFname else tmpTitle     

def isFolder (idx=currentItemPos()): 
    if DETVIDEXT and isVidExt(getTitle(idx)) : return False
    return True if getLi('Property(IsPlayable)',idx) in ('false', Empty) and not getFname(idx) else False
    
def isVidExt(name):
    for itm in TAG_PAR_VIDEOSEXT:
        if name.endswith(itm) : return True
    return False 
    
### JSP functions ...
_listdircmd = '{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"properties": ["file", "title"], "directory":"%s", "media":"files"}, "id": "1"}'

def getJsp(dirPath, srcName):
    _itmList = eval(xbmc.executeJSONRPC(_listdircmd % (dirPath)))['result']['files']
    _jsp     = struct()
    
    _jsp.link    = dirPath
    _jsp.name    = srcName
    _jsp.itmList = _itmList
    _jsp.count   = len(_itmList)
        
    return _jsp 

jsp_getLabel    = lambda jsp, idx=0 : jsp.itmList[idx]['label']
jsp_getLink     = lambda jsp, idx=0 : jsp.itmList[idx]['file']

def jsp_isFolder(jsp, idx):
    if jsp.itmList[idx]['filetype'] != 'folder' : return False
    return True

### Listitems Object ...
class vidItems:

    def __init__(self, dirPath=Empty, srcName=Empty):
        if not dirPath : self.norm_init()
        else           : self.jsp_init (dirPath, srcName)
    
    
    def jsp_init(self, dirPath, srcName):
    
        jsp = getJsp(dirPath, srcName)
        #import resources.lib.gui as GUI
        #GUI.dlgOk(str( jsp.count ))
    
        ## Current jsp data ...
        self.vidFolderNameDef = Empty
        self.vidCPath         = jsp.link
        self.vidCName         = jsp.name
        self.vidIsEmpty       = True
        self.vidFolCount      = jsp.count
        ## Local items list...
        self.vidListItems     = []
        self.vidListItemsRaw  = []
            
        ## Create items list ...
        for idx in range(0, self.vidFolCount):
            self.vidListItemsRaw.append([jsp_getLabel(jsp, idx), jsp_getLink(jsp, idx)])
            if jsp_isFolder(jsp, idx) : continue
            self.vidListItems.append([jsp_getLabel(jsp, idx), jsp_getLink(jsp, idx)])
            
        if self.vidListItems : 
            self.vidIsEmpty = False
            ## Set as default first nofolder item ...
            self.vidFolderNameDef = self.vidListItems[0][0] 
    
    
    def norm_init(self):
        
        ## Current listitem data ...
        self.vidFolderNameDef = Empty
        self.vidCurr          = getTitleF()
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
        self.vidListItemsRaw  = []
        
        ## If current item is not a folder, set it as default ...
        if not self.vidIsFolder : self.vidFolderNameDef = self.vidCurr
            
        ## Create items list ...
        for idx in range(1, self.vidFolCount+1):
            self.vidListItemsRaw.append([getTitleF(idx), getLink(idx)])
            if isFolder(idx) : continue
            self.vidListItems.append([getTitleF(idx), getLink(idx)])
            
        if self.vidListItems : 
            self.vidIsEmpty = False
            ## Set as default first nofolder item, if current item is a folder ...
            if self.vidFolderNameDef == Empty : self.vidFolderNameDef  = self.vidListItems[0][0] 
        
    def setmanually(self, manlist):
        self.vidListItems  = [itm for idx, itm in enumerate(self.vidListItemsRaw) if idx in manlist]
    
    def reverse(self):
        self.vidListItems.reverse()
        self.vidListItemsRaw.reverse()
    
    def getOnlyNexts(self):
        nexts = False
        retList = []
        for itm in self.vidListItems:
            if itm[0] == self.vidCurr : nexts = True; continue
            if not nexts : continue
            retList.append(itm[1])
        
        return retList 
             