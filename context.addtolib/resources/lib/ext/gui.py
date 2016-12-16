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
from base import *
from un import addon


### Defaults ...
defCaption = addon.name
defScript  = TAG_PAR_SCRIPT_ID

### Message ...
notInfo    = xbmcgui.NOTIFICATION_INFO
notWarning = xbmcgui.NOTIFICATION_WARNING
notError   = xbmcgui.NOTIFICATION_ERROR

#msg       = lambda title,    text=Empty,                                 : xbmc.executebuiltin('Notification(%s,%s)' % (title, text))
msg       = lambda title,    text=Empty,                                 : xbmcgui.Dialog().notification(title, text)
msgf      = lambda title,    text=Empty, nottype=notInfo                 : xbmcgui.Dialog().notification(title, text, nottype)

### Dialogs ...
dlgOk     = lambda text1,   text2=Empty, title=defCaption                : dlgOkX(text1, text2, title if title else defCaption) if addon.USESKINS else xbmcgui.Dialog().ok(title if title else defCaption, text1, text2)
dlgYn     = lambda text1,   text2=Empty, title=defCaption                : dlgYesNoX(text1, text2, title if title else defCaption).yes if addon.USESKINS else xbmcgui.Dialog().yesno(title if title else defCaption, text1, text2) 
dlgIn     = lambda                       title=defCaption, default=Empty : xbmcgui.Dialog().input(title if title else defCaption, default)
dlgInnum  = lambda                       title=defCaption, default=Empty : xbmcgui.Dialog().numeric(0, title if title else defCaption, default)

def dlgSelNoSkin (sargs, title=defCaption) : return xbmcgui.Dialog().select(title if title else defCaption, sargs) 

def dlgSel (sargs, title=defCaption, lnmsg=Empty, itmPos=0):
    if not title : title = defCaption
    if addon.USESKINS: 
        if lnmsg : return dlgSelX(lnmsg, title, sargs).position
        else     : return dlgSelXSub(title, sargs, setItmPos=itmPos).position
    else : return xbmcgui.Dialog().select(title, sargs)


def dlgResume (sargs, title=defCaption): 
    return dlgSelXSub(title if title else defCaption, sargs, XML=TAG_PAR_XMLW_RESUMEDLG).position if addon.USESKINS else xbmcgui.Dialog().select(title if title else defCaption, sargs)
    

def dlgSelmul (sargs, selMark, title=defCaption, selDef=None, resetItm=Empty):
    if not title : title = defCaption
    marksList = dict()
    resList   = []
    selAppr   = 0  
    
    if resetItm:
        sargs = [resetItm] + sargs
        selAppr = 1 
    
    if selDef:
        for idx, itm in enumerate(sargs):
            if itm in selDef : marksList.update({idx:selMark}); resList.append(idx-selAppr) 
    
    idx = 0 
    
    while idx != -1:
        sargsList = []
        for aidx, arg in enumerate(sargs) : sargsList.append(marksList.get(aidx, Empty) + arg)
        
        idx = dlgSel(sargsList, title, itmPos=idx)  
        if idx == len(sargsList) - 1 : idx = -1
        elif idx == 0 and resetItm:
            isUnselect = True if marksList else False 
            marksList.clear()
            resList = []
            if not isUnselect:
                for sidx, itm in enumerate(sargs[1:-1]): 
                    marksList.update({sidx+1:selMark})
                    resList.append(sidx)  
         
        if idx != -1 :
            if idx == 0 and resetItm : continue
            if  marksList.get (idx, False):
                resList.remove(idx-selAppr)
                marksList.pop (idx)
            else:
                resList.append(idx-selAppr)
                marksList.update({idx:selMark})
             
    return resList

### Actions ...
conok       = lambda      : xbmc.executebuiltin('Action(Ok)', True)
back        = lambda      : xbmc.executebuiltin('Action(Back)', True)
refresh     = lambda      : xbmc.executebuiltin('Container.Refresh')
#libUpdate   = lambda      : xbmc.executebuiltin('UpdateLibrary(video)', True)
#libClean    = lambda      : xbmc.executebuiltin('CleanLibrary(video)', True)
openSet     = lambda      : xbmc.executebuiltin('Addon.OpenSettings(%s)' % (defScript), False)
goTarget    = lambda link : xbmc.executebuiltin('container.update(%s)' % (link))
closeDlgs   = lambda      : xbmc.executebuiltin('Dialog.Close(all, true)')


def libUpdate (path=Empty):
    if path : uscr = 'UpdateLibrary(video, %s)' % path 
    else    : uscr = 'UpdateLibrary(video)' 
    xbmc.executebuiltin(uscr, True)
    
def libClean (path=Empty):
    if path : uscr = 'CleanLibrary(video, %s)' % path 
    else    : uscr = 'CleanLibrary(video)' 
    xbmc.executebuiltin(uscr, True)
    

#closeDlgs   = lambda      : xbmc.executebuiltin('Dialog.Close(%s, true)' % (str(xbmcgui.getCurrentWindowDialogId())))

### Service ...
serviceOn   = lambda      : xbmc.executebuiltin('RunScript(%s)' % (TAG_PAR_SERVICE), False)

### Player ...
seekPlay    = lambda pos  : xbmc.executebuiltin('seek(%s)' % (pos), True)
stopPlay    = lambda      : xbmc.executebuiltin('PlayerControl(Stop)', True)
FocusPayer  = lambda      : xbmc.executebuiltin('ActivateWindow(12005)')
FocusPayerC = lambda      : xbmc.executebuiltin('ActivateWindow(12901)')

PlayMedia   = lambda media, offset=0 : xbmc.executebuiltin('PlayMedia(%s, playoffset=%s)' % (media, offset))

    
#### NEW GUI ...

### Dialogs tmpl ...
class CAltDTmpl:
    def __init__(self, xmlFile, modal=True, defSkin=False):
        skin = 'Default' if defSkin else addon.SKIN  
        if modal : self._CAltDTmpl (xmlFile, addon.path, skin, parent=self).doModal()
        else     : self._CAltDTmpl (xmlFile, addon.path, skin, parent=self).start()
        
    
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
        if not addon.DIMBCKG : xml.getControl(90).setVisible(False) 
        if self.lnmsg != Empty: 
            xml.getControl(150).setLabel(TAG_PAR_MNUCOLORFORMAT % (addon.COLOR, self.lnmsg) if addon.COLORIZE else self.lnmsg)
        xml.setFocusId(200)
            
    
    def onClick(self, controlID, xml): 
        self.position = xml.getControl(200).getSelectedPosition()
        xml.getControl(2).setVisible(False)
        self.resetback(xml)
        xml.stop()
    
    def onAction(self, action, xml):
        ## ESC, BackSpace action ...
        navBack = [10, 92]
        ## Left, Right action ...
        navL = 1     
        navR = 2
        
        cId = action.getId() 
        if cId in navBack : self.position = len(self.sargs) - 1 
        elif cId == navL : xml.getControl(200).selectItem(0) 
        elif cId == navR : xml.getControl(200).selectItem(xml.getControl(200).size()-1)
        self.resetback(xml)
        xml.reAction(action)
    
    def resetback(self, xml):
        if self.position == len(self.sargs) - 1 : xml.getControl(1).setVisible(False)


class dlgSelXSub (CAltDTmpl):
    def __init__(self, caption, sargs, XML=TAG_PAR_XMLW_SELDLGSUB, setItmPos=0):
        self.caption  = caption
        self.sargs    = sargs     
        self.position = -1
        self.setItmPos = setItmPos
        CAltDTmpl.__init__(self, xmlFile=XML)
    
    def onInit(self, xml):
        xml.getControl(100).setLabel(TAG_PAR_MNUCOLORFORMAT % (addon.COLOR, self.caption) if addon.COLORIZE else self.caption)
        xml.getControl(200).addItems(self.sargs)
        if not addon.DIMBCKG : xml.getControl(90).setVisible(False)
        size = xml.getControl(200).size()
        selpos = self.setItmPos+5 if self.setItmPos+5 < size else size-1
        setpos = self.setItmPos+1 if self.setItmPos+1 < size else size-1 
        xml.getControl(200).selectItem(selpos)
        xml.setFocusId(200)
        xml.getControl(200).selectItem(setpos)    
            
    def onClick(self, controlID, xml): 
        self.position = xml.getControl(200).getSelectedPosition()
        xml.stop()
    
    def onAction(self, action, xml):
        ## ESC, BackSpace action ...
        navBack = [10, 92]
        ## Left, Right action ...
        navL = 1     
        navR = 2
        
        cId = action.getId() 
        if cId in navBack : self.position = len(self.sargs) - 1
        elif cId == navL : xml.getControl(200).selectItem(0) 
        elif cId == navR : xml.getControl(200).selectItem(xml.getControl(200).size()-1)
        xml.reAction(action)


class dlgOkX (CAltDTmpl):
    def __init__(self, text1, text2, caption):
        self.caption  = caption
        self.text     = text1+NewLine+text2 if text2 else text1      
        CAltDTmpl.__init__(self, xmlFile=TAG_PAR_XMLW_OKDLG)
    
    def onInit(self, xml):
        xml.getControl(100).setLabel(TAG_PAR_MNUCOLORFORMAT % (addon.COLOR, self.caption) if addon.COLORIZE else self.caption)
        xml.getControl(200).setText(self.text)
        if not addon.DIMBCKG : xml.getControl(90).setVisible(False)
            
    def onClick(self, controlID, xml): 
        xml.stop()       


class dlgYesNoX (CAltDTmpl):
    def __init__(self, text1, text2, caption):
        self.caption  = caption 
        self.text     = text1+NewLine+text2 if text2 else text1
        self.yes      = False      
        CAltDTmpl.__init__(self, xmlFile=TAG_PAR_XMLW_YESNODLG)
    
    def onInit(self, xml):
        xml.getControl(100).setLabel(TAG_PAR_MNUCOLORFORMAT % (addon.COLOR, self.caption) if addon.COLORIZE else self.caption)
        xml.getControl(200).setText(self.text)
        xml.getControl(250).setLabel(addon.tlraw(TAG_MNU_NO))
        xml.getControl(260).setLabel(addon.tlraw(TAG_MNU_YES))
        if not addon.DIMBCKG : xml.getControl(90).setVisible(False)
            
    def onClick(self, controlID, xml):
        if controlID == 261 : self.yes = True  
        xml.stop()


def dlgDropbox(opr=0, authorize_url=Empty):
    if opr == 0:
        result = dlgDropboxX().result
        if not result : return Empty
        if result in [1, 2]: 
            if result == 2: clipCopy(authorize_url)
            else          : webbrowser.open(authorize_url)
            code = Empty
            while True: 
                result, code = dlgDropboxX(2, code).rescode
                if not result  : return Empty
                if result == 1 : code = dlgIn()
                if result == 3 : 
                    if not code : code = addon.tlraw(TAG_DLG_DBXPEC) 
                    else        : return code 
                
    elif opr == 1 : dlgDropboxX(3)
    elif opr == 2 : dlgDropboxX(4)
    elif opr == 3 : dlgDropboxX(5)
    
    return Empty


class dlgDropboxX (CAltDTmpl):
    def __init__(self, page=1, code=Empty):
        self.result  = 0
        self.page    = page
        self.code    = code
        self.caption = addon.tlraw(TAG_TTL_DBXTTL)
        if   self.page == 1: 
            self.text = addon.tlraw(TAG_DLG_DBXP1) % (NewLine, NewLine, NewLine)
            self.b0   = addon.tlraw(TAG_TTL_DBXCANCEL)
            self.b1   = addon.tlraw(TAG_TTL_DBXOPEN)
            self.b2   = addon.tlraw(TAG_TTL_DBXCOPY)
            self.b3   = Empty
        elif self.page == 2:
            self.text = addon.tlraw(TAG_DLG_DBXP2) % (NewLine)
            self.b0   = addon.tlraw(TAG_TTL_DBXCANCEL)
            self.b1   = addon.tlraw(TAG_TTL_DBXKEYB)
            self.b2   = addon.tlraw(TAG_TTL_DBXPASTE)
            self.b3   = addon.tlraw(TAG_TTL_DBXOK)
        elif self.page == 3:
            self.text = addon.tlraw(TAG_DLG_DBXP3) % (NewLine)
            self.b0   = addon.tlraw(TAG_TTL_DBXOK)
            self.b1   = Empty
            self.b2   = Empty
            self.b3   = Empty
        elif self.page == 4:
            self.text = addon.tlraw(TAG_DLG_DBXP4) % (NewLine)
            self.b0   = addon.tlraw(TAG_TTL_DBXOK)
            self.b1   = Empty
            self.b2   = Empty
            self.b3   = Empty
        elif self.page == 5:
            self.text = addon.tlraw(TAG_DLG_DBXP5) % (NewLine)
            self.b0   = addon.tlraw(TAG_TTL_DBXOK)
            self.b1   = Empty
            self.b2   = Empty
            self.b3   = Empty
     
        CAltDTmpl.__init__(self, xmlFile=TAG_PAR_XMLW_DROPBOX, defSkin=True)
    
    def onInit(self, xml):
        xml.getControl(100).setLabel(self.caption)
        xml.getControl(200).setText(self.text)
        xml.getControl(701).setText(self.code)
        
        xml.getControl(250).setLabel(self.b0)
        xml.getControl(260).setLabel(self.b1)
        xml.getControl(270).setLabel(self.b2)
        xml.getControl(280).setLabel(self.b3)
        
        if self.page != 2: 
            xml.getControl(281).setVisible(False)
            xml.getControl(701).setVisible(False)
            
        if self.page == 3:
            xml.getControl(271).setVisible(False)
            xml.getControl(261).setVisible(False)
            xml.getControl(20).setVisible(False)
            xml.getControl(22).setVisible(False)
            xml.getControl(23).setVisible(False)
            
        if self.page == 4:
            xml.getControl(271).setVisible(False)
            xml.getControl(261).setVisible(False)
            xml.getControl(20).setVisible(False)
            xml.getControl(21).setVisible(False)
            xml.getControl(23).setVisible(False)
        
        if self.page == 5:
            xml.getControl(271).setVisible(False)
            xml.getControl(261).setVisible(False)
            xml.getControl(20).setVisible(False)
            xml.getControl(21).setVisible(False)
            xml.getControl(22).setVisible(False)
        
        if self.page < 3:
            xml.getControl(21).setVisible(False)
            xml.getControl(22).setVisible(False)
            xml.getControl(23).setVisible(False)
        
            
    def onClick(self, controlID, xml):
        stop = True
    
        if controlID == 261 : self.result = 1
        if controlID == 271 :
            if self.page == 2 : xml.getControl(701).setText(clipPaste()); stop = False
            else              : self.result = 2
        if controlID == 281 : self.result = 3
        if controlID == 251 : pass
        
        if stop:
            self.rescode = [self.result, xml.getControl(701).getText()]
            xml.stop()
        

class dlgNowPlayX (CAltDTmpl):
    def __init__(self, text, img=Empty, showtime=5, pretime=0, stopIf=None):
        self.text     = text
        self.showtime = showtime
        self.pretime  = pretime
        self.img      = img
        self.stopIf   = stopIf
        self.focusp   = False      
        wait(self.pretime)
        cwndd = xbmcgui.getCurrentWindowDialogId()
        cwnd  = xbmcgui.getCurrentWindowId()
        if cwndd == 12901 : back() 
        if cwnd  == 12005 : CAltDTmpl.__init__(self, xmlFile=TAG_PAR_XMLW_NOWPLAYDLG, modal=True)
    
    def onInit(self, xml):
        xml.getControl(200).setText(self.text)
        if self.img : xml.getControl(300).setImage(self.img)     
        Thrd(self.time_bomb, xml, self.showtime, self.stopIf) 
    
    def time_bomb(self, xml, showtime, stopIf):
        wtime = 0
        while True:
            if wtime > showtime : break
            if stopIf is not None and not stopIf() : break   
            wait(0.5); wtime += 0.5
            
        xml.stop()
    
    def onAction(self, action, xml):
        aid  = action.getId()
        cwnd = xbmcgui.getCurrentWindowId()
        if aid in [100, 101] : xml.stop()
        if cwnd == 12005 : FocusPayerC()
    
    def __del__(self):
        cwnd = xbmcgui.getCurrentWindowDialogId()
        if cwnd == 12901 : back() 
        

class Thrd(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self._stop = threading.Event()
        self.start()
        