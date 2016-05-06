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

from resources.lib.ext import *

### Base functions ...
log    = lambda event : xbmc.log('[%s] %s' % (addon.id, event))
action = lambda actid : xbmc.executebuiltin('RunScript(%s, action=%s)' % (TAG_PAR_ADDON, str(actid)), False)

### Main ...
def service():
    
    monitor = xbmc.Monitor()
    autimer = 0
    
    log('Service started ...')
    
    ## Startup ...
    if addon.STARTUPSHAD and addon.SILENTUPD : sadowupd()
    
    ## Start on timer ...
    while not monitor.abortRequested():
        if monitor.waitForAbort(10) : break
        
        if autimer >= addon.getautime() * 6:
            autimer = 0
              
            if addon.getshad() and addon.SILENTUPD : sadowupd()
            
        autimer += 1
    
    ## End ...    
    log('Service stoped ...')


### Actions ...
def sadowupd():
    log('Background scanning started ...') 
    action(10201)
   
                      
### Start main ...
if (__name__ == "__main__"): service()