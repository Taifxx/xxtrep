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
########## LAUNCHING FROM MEMORY SERVICE:

### Import modules ...
import context_ex as context
import context as cstart
import deb

### Define ...
ITD_FILE = cstart.ITD_FILE
error_file = cstart.error_file

adnname = context.tl(context.TAG_TTL_NM) % (context.addon.name)

### Messages ...
msgStrat = 'Launching from memory service started ...'
msgEnd   = 'Launching from memory service stopped ...'
  
msgStratVisual = 'LFM service started'
msgEndVisual   = 'LFM service stopped'

msgProcessError = 'Process ERROR'

### Base functions ...
log = lambda event : context.xbmc.log('[%s] >> %s' % (context.addon.id, event))

def starter():
    isRaise = False
    try:  
        context.plgMain (importLI=ITD_FILE)
        
    except Exception as exc:
        context.DOS.delf(context.DOS.join(context.addon.profile, context.TAG_PAR_STRARTF))
        context.GUI.msgf(adnname, msgProcessError, context.GUI.notError)
        deb.addraise(context.DOS.join(context.addon.profile, error_file))
        isRaise = True    
         
    finally:
        ## If user try double run ...
        if context.xbmcvfs.exists(context.DOS.join(context.addon.profile, ITD_FILE)):
            context.DOS.delf(context.DOS.join(context.addon.profile, ITD_FILE))
        if isRaise : raise


### Main ...
def service(externalAbort, report):
    ## Load monitor ...    
    monitor = context.xbmc.Monitor()
    
    ## Log start ...
    log(msgStrat)
    if report : context.GUI.msg(adnname, msgStratVisual)
    
    ## Start service ...
    while not monitor.abortRequested():
    
        ## Check starter ...
        if context.xbmcvfs.exists(context.DOS.join(context.addon.profile, ITD_FILE)) : starter()
        
        ## Check exit ...
        if monitor.waitForAbort(1) or externalAbort() : break        

    ## End service (log end) ...    
    del monitor
    log(msgEnd)
    context.GUI.msg(adnname, msgEndVisual) 
