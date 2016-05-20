#!/usr/bin/python
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

### Import modules ...

#from resources.lib.ext import *
import context 

log = lambda event : context.xbmc.log('[%s] >> %s' % (context.addon.id, event))

### Action class ...
class CAction:
    
    def __init__(self, actID, startup, skip, eventTime, logMsg, *args):
        self.timer     = 0
        self.actID     = actID
        self.logMsg    = logMsg
        self.startup   = startup
        self.skip      = skip
        self.eventTime = eventTime
        self.args      = args
    
    
    def __call__(self):
        
        if self.timer >= self.eventTime() * 6 or self.startup:
            
            if self.skip() : return
             
            self.timer   = 0
            self.startup = False
            
            for arg in self.args:
                if not arg() : return
                
            log(self.logMsg)
            context.plgMain(self.actID)
        
        else : self.timer += 1 

### Skip functions ... 
def skip():
    if context.DOS.exists(context.DOS.join(context.addon.profile, context.TAG_PAR_LIB_FOLDER, context.TAG_PAR_LOCKF))   : return True
    if context.DOS.exists(context.DOS.join(context.addon.profile, context.TAG_PAR_LIB_FOLDER, context.TAG_PAR_STRARTF)) : return True
    if context.DOS.exists(context.DOS.join(context.addon.profile, context.TAG_PAR_LIB_FOLDER, context.TAG_PAR_STRARTAF)): return True
    return False


### Main ...
def service():
    
    monitor = context.xbmc.Monitor()
    shadowupd = CAction(10201, context.addon.STARTUPSHAD, skip, context.addon.getautime, 'Background scanning started ...', context.addon.getshad, context.addon.getsilent)
    backup    = CAction(10209, context.addon.BKUPSTARTUP, skip, context.addon.getbcktime, 'Backup creating started ...', context.addon.getabck)
    
    log('Service started ...')
    
    ## Start on timer ...
    while not monitor.abortRequested():
        if monitor.waitForAbort(10) : break

        if context.DOS.exists(context.DOS.join(context.addon.profile, '.nos'))   : break
        if context.DOS.exists(context.DOS.join(context.addon.profile, '.cont'))  : continue
        
        backup()
        shadowupd()

        
    ## End ...    
    del shadowupd, backup
    log('Service stoped ...') 


### Start main ...
if (__name__ == "__main__"): service()