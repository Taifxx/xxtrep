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
import threading
#import resources.lib.addon as addon

from resources.lib.tools   import *
from resources.lib.const   import *
from resources.lib.tags    import *
from resources.lib.addon   import CAddon as adn

### Defaults ...
#defCaption = addon.name
defCaption = adn().name
defScript  = TAG_PAR_SCRIPT_ID

### Message ...
notInfo    = xbmcgui.NOTIFICATION_INFO
notWarning = xbmcgui.NOTIFICATION_WARNING
notError   = xbmcgui.NOTIFICATION_ERROR

#msg       = lambda title,    text=Empty,                                 : xbmc.executebuiltin('Notification(%s,%s)' % (title, text))
msg       = lambda title,    text=Empty,                                 : xbmcgui.Dialog().notification(title, text)
msgf      = lambda title,    text=Empty, nottype=notInfo                 : xbmcgui.Dialog().notification(title, text, nottype)

### Dialogs ...
dlgOk     = lambda text1,   text2=Empty, title=defCaption                : dlgOkX(text1, text2, title if title else defCaption) if adn().USESKINS else xbmcgui.Dialog().ok(title if title else defCaption, text1, text2)
dlgYn     = lambda text1,   text2=Empty, title=defCaption                : dlgYesNoX(text1, text2, title if title else defCaption).yes if adn().USESKINS else xbmcgui.Dialog().yesno(title if title else defCaption, text1, text2) 
dlgIn     = lambda                       title=defCaption, default=Empty : xbmcgui.Dialog().input(title if title else defCaption, default)
dlgInnum  = lambda                       title=defCaption, default=Empty : xbmcgui.Dialog().numeric(0, title if title else defCaption, default)

def dlgSelNoSkin (sargs, title=defCaption) : return xbmcgui.Dialog().select(title if title else defCaption, sargs) 

def dlgSel (sargs, title=defCaption, lnmsg=Empty):
    if not title : title = defCaption
    if adn().USESKINS: 
        if lnmsg : return dlgSelX(lnmsg, title, sargs).position
        else     : return dlgSelXSub(title, sargs).position
    else : return xbmcgui.Dialog().select(title, sargs)

def dlgResume (sargs, title=defCaption): 
    return dlgSelXSub(title if title else defCaption, sargs, XML=TAG_PAR_XMLW_RESUMEDLG).position if adn().USESKINS else xbmcgui.Dialog().select(title if title else defCaption, sargs)
    

def dlgSelmul (sargs, selMark, title=defCaption, selDef=None):
    if not title : title = defCaption
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
conok       = lambda      : xbmc.executebuiltin('Action(Ok)', True)
back        = lambda      : xbmc.executebuiltin('Action(Back)', True)
refresh     = lambda      : xbmc.executebuiltin('Container.Refresh')
libUpdate   = lambda      : xbmc.executebuiltin('UpdateLibrary(video)', True)
libClean    = lambda      : xbmc.executebuiltin('CleanLibrary(video)', True)
openSet     = lambda      : xbmc.executebuiltin('Addon.OpenSettings(%s)' % (defScript), True)
goTarget    = lambda link : xbmc.executebuiltin('container.update(%s)' % (link))
closeDlgs   = lambda      : xbmc.executebuiltin('Dialog.Close(all, true)')

### Service ...
serviceOn   = lambda      : xbmc.executebuiltin('RunScript(%s)' % (TAG_PAR_SERVICE), False)

### Player ...
seekPlay    = lambda pos  : xbmc.executebuiltin('seek(%s)' % (pos), True)
stopPlay    = lambda      : xbmc.executebuiltin('PlayerControl(Stop)', True)
FocusPayer  = lambda      : xbmc.executebuiltin('ActivateWindow(12005)')
FocusPayerC = lambda      : xbmc.executebuiltin('ActivateWindow(10114)')

    
#### NEW GUI ...

### Dialogs tmpl ...
class CAltDTmpl:
    def __init__(self, xmlFile, modal=True): 
        if modal : self._CAltDTmpl (xmlFile, adn().path, adn().SKIN, parent=self).doModal()
        else     : self._CAltDTmpl (xmlFile, adn().path, adn().SKIN, parent=self).start()
    
    ## Reload interface ...
    def onInit(self, xml)             : xml.reInit()
    def onClick(self, controlID, xml) : xml.reClick(controlID)
    def onAction(self, action, xml)   : xml.reAction(action)
    def onFocus(self, controlID, xml) : xml.reFocus(controlID)
    def start(self, xml)              : xml.show()
    
    class _CAltDTmpl(xbmcgui.WindowXMLDialog):
        def __init__(self, *args, **kwargs):
            self.parent = kwargs.get('parent')
            xbmcgui.WindowXMLDialog.__init__(self) 
        
        def stop(self)               : self.close()
        def start(self)              : self.parent.start(self)
        def onInit(self)             : self.parent.onInit(self)
        def onClick(self, controlID) : self.parent.onClick(controlID, self)
        def onAction(self, action)   : self.parent.onAction(action, self)
        def onFocus(self, controlID) : self.parent.onFocus(controlID, self)
        
        def reAction(self, action)   : xbmcgui.WindowXMLDialog.onAction(self, action) 
        def reClick(self, controlID) : xbmcgui.WindowXMLDialog.onClick(self, controlID)
        def reFocus(self, controlID) : xbmcgui.WindowXMLDialog.onFocus(self, controlID)
        def reInit(self)             : xbmcgui.WindowXMLDialog.onInit(self)

### Dialogs ...
class dlgSelX (CAltDTmpl):
    def __init__(self, lnmsg, caption, sargs):
        self.caption  = caption
        self.sargs    = sargs
        self.lnmsg    = lnmsg     
        self.position = -1
        CAltDTmpl.__init__(self, xmlFile=TAG_PAR_XMLW_SELDLG)
    
    def onInit(self, xml):
        xml.getControl(100).setLabel(self.caption)
        xml.getControl(200).addItems (self.sargs)
        if not adn().DIMBCKG : xml.getControl(90).setVisible(False) 
        if self.lnmsg != Empty: 
            xml.getControl(150).setLabel(TAG_PAR_MNUCOLORFORMAT % (adn().COLOR, self.lnmsg) if adn().COLORIZE else self.lnmsg)
            
    
    def onClick(self, controlID, xml): 
        self.position = xml.getControl(200).getSelectedPosition()
        xml.getControl(2).setVisible(False)
        self.resetback(xml)
        xml.stop()
    
    def onAction(self, action, xml):
        ## ESC, BackSpace action ...
        navBack = [10, 92]
        
        cId = action.getId() 
        if cId in navBack : self.position = len(self.sargs) - 1 
        self.resetback(xml)
        xml.reAction(action)
    
    def resetback(self, xml):
        if self.position == len(self.sargs) - 1 : xml.getControl(1).setVisible(False)


class dlgSelXSub (CAltDTmpl):
    def __init__(self, caption, sargs, XML=TAG_PAR_XMLW_SELDLGSUB):
        self.caption  = caption
        self.sargs    = sargs     
        self.position = -1
        CAltDTmpl.__init__(self, xmlFile=XML)
    
    def onInit(self, xml):
        xml.getControl(100).setLabel(TAG_PAR_MNUCOLORFORMAT % (adn().COLOR, self.caption) if adn().COLORIZE else self.caption)
        xml.getControl(200).addItems(self.sargs)
        if not adn().DIMBCKG : xml.getControl(90).setVisible(False)
            
    def onClick(self, controlID, xml): 
        self.position = xml.getControl(200).getSelectedPosition()
        xml.stop()
    
    def onAction(self, action, xml):
        ## ESC, BackSpace action ...
        navBack = [10, 92]
        
        cId = action.getId() 
        if cId in navBack : self.position = len(self.sargs) - 1
        xml.reAction(action)


class dlgOkX (CAltDTmpl):
    def __init__(self, text1, text2, caption):
        self.caption  = caption
        self.text     = text1+NewLine+text2 if text2 else text1      
        CAltDTmpl.__init__(self, xmlFile=TAG_PAR_XMLW_OKDLG)
    
    def onInit(self, xml):
        xml.getControl(100).setLabel(TAG_PAR_MNUCOLORFORMAT % (adn().COLOR, self.caption) if adn().COLORIZE else self.caption)
        xml.getControl(200).setText(self.text)
        if not adn().DIMBCKG : xml.getControl(90).setVisible(False)
            
    def onClick(self, controlID, xml): 
        xml.stop()       


class dlgYesNoX (CAltDTmpl):
    def __init__(self, text1, text2, caption):
        self.caption  = caption 
        self.text     = text1+NewLine+text2 if text2 else text1
        self.yes      = False      
        CAltDTmpl.__init__(self, xmlFile=TAG_PAR_XMLW_YESNODLG)
    
    def onInit(self, xml):
        xml.getControl(100).setLabel(TAG_PAR_MNUCOLORFORMAT % (adn().COLOR, self.caption) if adn().COLORIZE else self.caption)
        xml.getControl(200).setText(self.text)
        xml.getControl(250).setLabel(adn().tlraw(TAG_MNU_NO))
        xml.getControl(260).setLabel(adn().tlraw(TAG_MNU_YES))
        if not adn().DIMBCKG : xml.getControl(90).setVisible(False)
            
    def onClick(self, controlID, xml):
        if controlID == 261 : self.yes = True  
        xml.stop()
        

class Thrd(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()        
