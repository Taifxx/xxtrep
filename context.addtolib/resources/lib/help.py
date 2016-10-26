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
from ext import *


##### Show help ...
class showHelp (GUI.CAltDTmpl):
    def __init__(self):
    
        self.helpText = DOS.file(TAG_PAR_HELPFILE + tl(TAG_LNG_ID), DOS.join(addon.path, *TAG_PAR_HELPPATH), fType=FRead)
        
        lines      = CMP.compsRemtag(self.helpText).split(NewLine)
        linescount = self.helpText.count(NewLine)
        # for line in lines:
        #     linescount += int(len(line) / 340.0) 
         
        self.tblen    = 300
        self.tbpos    = 0  
        
        GUI.CAltDTmpl.__init__(self, xmlFile=TAG_PAG_HELPXML)
    
    
    def onInit(self, xml):
        xml.getControl(100).setLabel(tl(TAG_TTL_HELP))
        xml.getControl(200).setText (decolor(self.helpText))
        
    
    
    def onClick(self, controlID, xml):
        if controlID == 150 : xml.stop()
    
    
    def onAction(self, action, xml):
        actID = action.getId()
        if actID == 105 : 
            if self.tbpos < self.tblen : self.tbpos += 1; xml.getControl(200).scroll(self.tbpos)         
        if actID == 104 : 
            if self.tbpos > 0          : self.tbpos -= 1; xml.getControl(200).scroll(self.tbpos)
        
        xml.reAction(action)
  