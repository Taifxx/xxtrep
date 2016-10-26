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
import context_ex as context 

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
            
            if self.startup and emgrControl().isEmgrExit(self.actID, self.eventTime()*60): 
                log('Emergency exit was detected. Background process %s will skipped' % (self.actID))
                self.startup = False
                return 
             
            self.timer   = 0
            self.startup = False
             
            
            for arg in self.args:
                if not arg() : return
                
            log(self.logMsg)
            context.plgMain(self.actID)
            
            emgrControl().setLAACTT(self.actID)
        
        else : self.timer += 1 
        

class emgrControl:
    def __init__(self):
        self._sepLST = context.TAG_PAR_TVSPACK_LSEP
        self._sepPRT = context.TAG_PAR_TVSPACK_PSEP + context.NewLine
    
    def _laactt_wr(self, actions):
        jact = []
        for akey, aval in actions.items():
            jact.append(str(akey)+self._sepLST+str(aval))
        laacttData = self._sepPRT.join(jact)
        context.DOS.file(context.TAG_PAR_LAACTT, context.addon.profile, laacttData, fType=context.FWrite, fRew=True)
    
    def _laactt_rd(self):
        laacttData = context.DOS.file(context.TAG_PAR_LAACTT, context.addon.profile, fType=context.FRead) 
        if laacttData == -1: return context.Empty         
        return {int(_actid):_acttime for rec in laacttData.split(self._sepPRT) for _actid, _acttime in [rec.split(self._sepLST)]}
    
    def setLAACTT(self, actId):
        actions = self._laactt_rd()
        aRec    = {actId:context.time.time()}
        if not actions : actions = aRec
        else           : actions.update(aRec)
        self._laactt_wr(actions)
        
    def isEmgrExit(self, actId, period):
        actions = self._laactt_rd()
        if not actions : return False
        laacttTime = actions.get(actId, context.Empty)
        if not laacttTime : return False
        if context.time.time() - float(laacttTime) > period : return False
        return True
     

### Skip functions ... 
def skip():
    if context.DOS.exists(context.DOS.join(context.addon.profile, context.TAG_PAR_STRARTF)) : return True
    return False

def remover():
    rFile = context.DOS.join(context.addon.profile, context.TAG_PAR_STRARTF);  context.DOS.delf(rFile) 


### Main ...
def service():
    
    remover()
    
    monitor = context.xbmc.Monitor()
    shadowupd = CAction(10201, context.addon.STARTUPSHAD, skip, context.addon.getautime, 'Background scanning started ...', context.addon.getshad, context.addon.getsilent)
    backup    = CAction(10209, context.addon.BKUPSTARTUP, skip, context.addon.getbcktime, 'Backup creating started ...', context.addon.getabck)
    sync      = CAction(10213, context.addon.STRTUPSYNC, skip, context.addon.getsynctime, 'Synchronization started ...', context.addon.getsyncatkn, context.addon.getautosync)
    watchsync = CAction(10214, context.addon.STRTUPWS, skip, context.addon.getwstime, 'Watched statuses synchronization started ...', context.addon.getsyncatkn, context.addon.getautows)
    
    log('OLD Service started ...')
    
    ## Start on timer ...
    while not monitor.abortRequested():
        if monitor.waitForAbort(10) : break
        
        backup()
        shadowupd()
        sync()
        watchsync()

        
    ## End ...    
    del shadowupd, backup
    log('OLD Service stoped ...') 


### Start main ...
if (__name__ == "__main__"): service()