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
########## HLP:

### Import modules ...
import xbmcgui, xbmc

from resources.lib.ext       import *


##### Show help ...
class showHelp(xbmcgui.WindowDialog):

    def __init__(self):
    
        xbmcgui.WindowDialog.__init__(self)
    
        border        = TAG_PAR_HLPBORDERSIZE
        Lng           = tl(TAG_LNG_ID)
        HelpFile      = TAG_PAR_HELPFILE + tl(TAG_LNG_ID)
        hPath         = DOS.join(addon.path, TAG_PAR_RESFOLDER, TAG_PAR_HLPFOLDER)
        bkgImgPath    = DOS.join(addon.path, TAG_PAR_RESFOLDER, TAG_PAR_IMGFOLDER, TAG_PAR_BKG)
        bkgImgLnPath  = DOS.join(addon.path, TAG_PAR_RESFOLDER, TAG_PAR_IMGFOLDER, TAG_PAR_LN)
        
        self.helpText = DOS.file(HelpFile, hPath, fType=FRead)
        
        self.pos      = 0
        self.scrstep  = TAG_PAR_HLPSCROLL
        self.lncount  = self.helpText.count(NewLine)-1
        
        xE = TAG_PAR_RESX   
        yE = TAG_PAR_RESY
        
        x = border 
        y = border + 45
        
        width  = xE - x - border
        height = yE - y - border 
        
        bkgImg              = xbmcgui.ControlImage(0, 0,   xE, yE,  bkgImgPath)
        bkgImgLine          = xbmcgui.ControlImage(0, -15, xE, 134, bkgImgLnPath)
        
        self.txtControl     = xbmcgui.ControlTextBox(x, y, width, height)
        self.btnControlOk   = xbmcgui.ControlButton(border, 10, 100, 40,     tl(TAG_DLG_OK),  alignment=6)
        self.btnControlPrev = xbmcgui.ControlButton(border+105, 10, 100, 40, tl(TAG_DLG_PR),  alignment=6)
        self.btnControlNext = xbmcgui.ControlButton(border+210, 10, 100, 40, tl(TAG_DLG_NX),  alignment=6)
        self.lblPos         = xbmcgui.ControlLabel (border+550, 10, 150, 40, Empty,           alignment=6)
        
        self.addControl(bkgImg)
        self.addControl(bkgImgLine)
        
        self.addControl(self.txtControl)
        self.addControl(self.btnControlOk)
        self.addControl(self.btnControlNext)
        self.addControl(self.btnControlPrev)
        self.addControl(self.lblPos)
        
        self.txtControl.setText(self.helpText)
        self.setlblpos()
        
        bkgImg.setAnimations([('windowopen', 'effect=fade start=0 end=100 time=400',), ('windowclose', 'effect=fade start=100 end=0 easing=in time=400',)])
        bkgImgLine.setAnimations([('windowopen', 'effect=fade start=0 end=100 time=400 delay=200',), ('windowclose', 'effect=fade start=100 end=0 easing=in time=400',)])
        
        self.btnControlOk.setAnimations([('windowopen', 'effect=fade start=0 end=100 time=400 delay=100',), ('windowclose', 'effect=fade start=100 end=0 easing=in time=400',)])  
        self.btnControlPrev.setAnimations([('windowopen', 'effect=fade start=0 end=100 time=400 delay=100',), ('windowclose', 'effect=fade start=100 end=0 easing=in time=400',)])
        self.btnControlNext.setAnimations([('windowopen', 'effect=fade start=0 end=100 time=400 delay=100',), ('windowclose', 'effect=fade start=100 end=0 easing=in time=400',)])
        self.lblPos.setAnimations([('windowopen', 'effect=fade start=0 end=100 time=400 delay=100',), ('windowclose', 'effect=fade start=100 end=0 easing=in time=400',)])        
        
        self.txtControl.setAnimations([('windowopen', 'effect=fade start=0 end=100 time=400 delay=300',), ('windowclose', 'effect=fade start=100 end=0 easing=in time=400',)]) 
        
        self.doModal()
        
        
    def setlblpos(self):
        self.lblPos.setLabel(tl(TAG_TTL_POSHLP) % (self.pos, self.lncount))    
    
    
    def onControl(self, control):
        if   control == self.btnControlPrev: 
            if self.pos > self.scrstep : self.pos -= self.scrstep
            elif self.pos > 0 : self.pos = 0
            self.txtControl.scroll(self.pos)
            self.setlblpos()
                
        elif control == self.btnControlNext: 
            if self.pos < self.lncount - self.scrstep : self.pos += self.scrstep
            elif self.pos < self.lncount : self.pos = self.lncount
            self.txtControl.scroll(self.pos)
            self.setlblpos() 
                
        else: 
            self.close()  