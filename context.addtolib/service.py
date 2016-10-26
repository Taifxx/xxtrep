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
########## MAIN SERVICE:

### Import modules ...
import context_ex as context
import lfm_service, deb  

### Define ...
msgStart = 'Main service started'
msgEnd   = 'Main service stopped'
msgEExit = 'Emergency exit was detected. Background process %s will skipped'
msgProcessError = 'Background process ERROR'

adnname = context.tl(context.TAG_TTL_NM) % (context.addon.name) 

### Log message ...
log = lambda event : context.xbmc.log('[%s] >> %s' % (context.addon.id, event))

### Action class ...
class CAction:
    
    def __init__(self, actID, startup, skip, eventTime, logMsg, *args):
        self.timer     = context.time.time()
        self.actID     = actID
        self.logMsg    = logMsg
        self.startup   = startup
        self.skip      = skip
        self.eventTime = eventTime
        self.args      = args
    
    
    def __call__(self):

        if context.time.time() - self.timer >= self.eventTime()*60 or self.startup:
            
            if self.skip() : return
            
            if self.startup and context.emgrControl().isEmgrExit(self.actID, self.eventTime()*60): 
                log(msgEExit % (self.actID))
                self.startup = False
                return 
             
            for arg in self.args:
                if arg == 999: 
                    if self.startup : break
                    else            : continue
                if not arg() : return
            
            self.timer   = context.time.time()
            self.startup = False
                
            log(self.logMsg)
            try:
                context.plgMain(self.actID)
            #except Exception as exc:
            except:
                remover()
                context.GUI.msgf(adnname, msgProcessError, context.GUI.notError)
                deb.addraise(context.DOS.join(context.addon.profile, lfm_service.error_file))
                raise  
            
            context.emgrControl().setLAACTT(self.actID)
        
        else : pass 
        
     

### Skip functions ... 
def skip():
    if context.DOS.exists(context.DOS.join(context.addon.profile, context.TAG_PAR_STRARTF)) : return True
    return False


def remover():
    rFile = context.DOS.join(context.addon.profile, context.TAG_PAR_STRARTF);  context.DOS.delf(rFile)
    rFile = context.DOS.join(context.addon.profile, lfm_service.ITD_FILE); context.DOS.delf(rFile)
    rFile = context.DOS.join(context.addon.profile, 'stopsrv'); context.DOS.delf(rFile)
    


### Main ...
def service(report=False):

    ## Check Allow services option ...
    if not context.addon.USESRV : return    
    
    ## SEC : Skip cleaning ...
    if not context.xbmcvfs.exists(context.DOS.join(context.addon.profile, 'nocln')) : remover()
    else : context.DOS.delf(context.DOS.join(context.addon.profile, 'nocln'))
    
    ## SEC : Exit (don't allow services) ...
    if context.xbmcvfs.exists(context.DOS.join(context.addon.profile, 'nos')) : return
    
    ## Load monitir ...
    monitor = context.xbmc.Monitor()
    
    ## SEC : Backup and exit ...
    _terminate = False
    _bckupOnStartup = context.addon.BKUPSTARTUP
    if context.xbmcvfs.exists(context.DOS.join(context.addon.profile, 'bckupex')):
        context.DOS.delf(context.DOS.join(context.addon.profile, 'bckupex'))
        _bckupOnStartup = True
        _terminate      = True 
    
    ## Create background processes (Args after 999 - ignored on sturtup) ...
    backup    = CAction(10209, _bckupOnStartup, skip, context.addon.getbcktime, 'Backup creating started ...', 999, context.addon.getabck) 
    shadowupd = CAction(10201, context.addon.STARTUPSHAD, skip, context.addon.getautime, 'Background scanning started ...', context.addon.getsilent, 999, context.addon.getshad)
    sync      = CAction(10213, context.addon.STRTUPSYNC, skip, context.addon.getsynctime, 'Synchronization started ...', context.addon.getsyncatkn, 999, context.addon.getautosync)
    watchsync = CAction(10214, context.addon.STRTUPWS, skip, context.addon.getwstime, 'Watched statuses synchronization started ...', context.addon.getsyncatkn, 999, context.addon.getautows)
    
    ## Define LFM, sprocess ...
    LFM = None
    sprocess = None
    pool = 1
    
    ## Set LFM terminator ...
    lfmstop = False
    def isLFMStop() : return lfmstop 
    
    ## Log start ...
    log(msgStart)
    if report : context.GUI.msg(adnname, msgStart)
    
    ## Start service ...
    while not monitor.abortRequested():
    
        ## Check Allow services option ...
        if not context.addon.USESRV : break 
    
        ## SEC : Service termination ...
        if context.xbmcvfs.exists(context.DOS.join(context.addon.profile, 'stopsrv')):
            context.DOS.delf(context.DOS.join(context.addon.profile, 'stopsrv')) 
            break
        
        ## Set service 'Running' status ...
        if not context.addon.SRVSTATUSV or context.addon.SRVSTATUS != context.tlraw(context.TAG_SET_RUN):
            context.addon.addon.setSetting('srvstatusv', 'true')
            context.addon.addon.setSetting('srvstatus', context.tlraw(context.TAG_SET_RUN))
        
        ## Start (Stop) Launching from memory (LFM) Service ...
        if context.addon.USELFM:
            lfmstop = False 
            if LFM is not None and not LFM.isAlive() : del LFM; LFM = None # Start LFM if it stopped
            if LFM is None : LFM = context.GUI.Thrd(lfm_service.service, isLFMStop, report) # Create and start LFM
        else : lfmstop = True; report = True # Stop LFM
        
        ## Run background processes by timer ...
        # backup()
        # if _terminate : break
        # sync()
        # watchsync()
        # shadowupd()
        
        if sprocess is None or not sprocess.isAlive(): 
            del sprocess
            if   pool == 1 : 
                sprocess = context.GUI.Thrd(backup)
                if _terminate : break
            elif pool == 2 : sprocess = context.GUI.Thrd(sync)
            elif pool == 3 : sprocess = context.GUI.Thrd(watchsync)
            elif pool == 4 : sprocess = context.GUI.Thrd(shadowupd)
            if pool == 4 : pool = 1 
            else: pool += 1
        
        ## Check exit ...
        if monitor.waitForAbort(10) : break

    ## Wait LFM stopping ...
    lfmstop = True
    while LFM is not None and LFM.isAlive() : context.wait(1)
    ## Wait sub process stopping ...
    while sprocess is not None and sprocess.isAlive() : context.wait(1)
    
    ## End service (log end) ...    
    del shadowupd, backup, sync, watchsync, LFM, sprocess, monitor 
    ## Set service 'Stopped' status ...
    context.addon.addon.setSetting('srvstatusv', 'false')
    context.addon.addon.setSetting('srvstatus', context.tlraw(context.TAG_SET_STOP))
    
    log(msgEnd)
    context.GUI.msg(adnname, msgEnd) 


### Start service command ...
if (__name__ == "__main__"): service()