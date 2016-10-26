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
########## INFO:

### Import modules ...
from base import *


### Convert string True result ...
_sbool = lambda sval : True if sval == 'true' else False


### Addon class ...
class CAddon:

    ### Translate tag to languare string ...
    tlraw = lambda self, tag : e(self.localize(tag))   

    ### Addon info ...
    @property
    def addon          (self) : return xbmcaddon.Addon(id=TAG_PAR_SCRIPT_ID)
    @property
    def profile        (self) : return de(xbmc.translatePath(self.addon.getAddonInfo('profile')))
    @property
    def localize       (self) : return self.addon.getLocalizedString
    @property
    def name           (self) : return self.addon.getAddonInfo('name')
    @property
    def id             (self) : return self.addon.getAddonInfo('id')
    @property
    def author         (self) : return self.addon.getAddonInfo('author')
    @property
    def version        (self) : return self.addon.getAddonInfo('version')
    @property
    def path           (self) : return de(self.addon.getAddonInfo('path'))
    @property
    def icon           (self) : return self.addon.getAddonInfo('icon')
    
    
    ### Settings ...
    @property
    def COLORIZE       (self) : return _sbool(self.addon.getSetting('colorize'))
    @property
    def UPDAFTER       (self) : return _sbool(self.addon.getSetting('updafter'))
    @property
    def ADDUPD         (self) : return _sbool(self.addon.getSetting('addupd'))
    @property
    def BGUPD          (self) : return _sbool(self.addon.getSetting('bgupd'))
    @property
    def LNKTIMEOUT     (self) : return int(self.addon.getSetting('lnktimeout'))
    @property
    def MNUITMNUM      (self) : return int(self.addon.getSetting('mnuitmnum'))
    @property
    def SETPAGE        (self) : return int(self.addon.getSetting('setpage'))
    @property
    def CALLURL        (self) : return _sbool(self.addon.getSetting('callurl'))
    @property
    def PLAYBCONT      (self) : return _sbool(self.addon.getSetting('playbcont'))         
    @property
    def POSUPD         (self) : return int(self.addon.getSetting('posupd'))   
    @property
    def POSSLEEP       (self) : return int(self.addon.getSetting('possleep')) 
    @property
    def WCHF           (self) : return _sbool(self.addon.getSetting('wchf'))   
    @property
    def WPERC          (self) : return int(self.addon.getSetting('wperc'))    
    @property
    def AUTORES        (self) : return _sbool(self.addon.getSetting('autores'))  
    @property
    def RESDLG         (self) : return _sbool(self.addon.getSetting('resdlg')) 
    @property
    def DETVIDEXT      (self) : return _sbool(self.addon.getSetting('detvidext'))
    @property
    def WAITBSEEK      (self) : return int(self.addon.getSetting('waitbseek')) 
    @property
    def EODGENM        (self) : return self.addon.getSetting('eodgenm')  
    @property
    def movFolder      (self) : return self.addon.getSetting('fldrmov')
    @property
    def tvsFolder      (self) : return self.addon.getSetting('fldrtvs')
    @property
    def SILENTUPD      (self) : return _sbool(self.addon.getSetting('silentupd')) 
    @property
    def AUTOUPDSRC     (self) : return _sbool(self.addon.getSetting('autoupdsrc'))
    @property
    def AUTOUPDALL     (self) : return _sbool(self.addon.getSetting('autoupdall'))
    @property
    def NOREPAUTO      (self) : return _sbool(self.addon.getSetting('norepauto'))
    @property
    def NOREPRAWAUTO   (self) : return _sbool(self.addon.getSetting('noreprawauto'))
    @property
    def HIDEAUPD       (self) : return _sbool(self.addon.getSetting('hideaupd'))
    @property
    def ALLOWSHADOW    (self) : return _sbool(self.addon.getSetting('allowshadow'))
    @property
    def AUTIME         (self) : return int(self.addon.getSetting('autime'))
    @property
    def STARTUPSHAD    (self) : return _sbool(self.addon.getSetting('startupshad'))
    @property
    def COLOR          (self) : return self.addon.getSetting('mnucolor')
    @property
    def libpath        (self) : _libpath = self.addon.getSetting('libpath'); return _libpath if _libpath != TAG_PAR_SETDEF else self.profile
    @property
    def BKUPPATH       (self) : _bkuppath = self.addon.getSetting('bkuppath'); return _bkuppath if _bkuppath != TAG_PAR_SETDEF else self.profile
    @property
    def BKUPREMOLD     (self) : return _sbool(self.addon.getSetting('bkupremold')) 
    @property
    def BKUPNUM        (self) : return int(self.addon.getSetting('bkupnum'))    
    @property
    def BKUPSTARTUP    (self) : return _sbool(self.addon.getSetting('bkupstartup'))
    @property
    def BKUPAUTO       (self) : return _sbool(self.addon.getSetting('bkupauto'))   
    @property
    def BKUPTIME       (self) : return int(self.addon.getSetting('bkuptime'))  
    @property
    def HIDEBCKPRGS    (self) : return _sbool(self.addon.getSetting('hidebckprgs'))
    @property
    def USESKINS       (self) : return _sbool(self.addon.getSetting('useskins'))
    @property
    def DIMBCKG        (self) : return _sbool(self.addon.getSetting('dimbckg'))
    @property
    def SKIN           (self) : return self.addon.getSetting('skin')
    #@property
    #def NEWPLAYS       (self) : return _sbool(self.addon.getSetting('newplays'))
    @property
    def PCORE          (self) : return self.addon.getSetting('pcore')
    @property
    def PCOREVAL       (self) : return int(self.addon.getSetting('pcoreval'))
    @property
    def DEDLPTIME      (self) : return int(self.addon.getSetting('dedlptime'))
    @property
    def PBMETHOD       (self) : return self.addon.getSetting('pbmethod')
    @property
    def USENOWPLAY     (self) : return _sbool(self.addon.getSetting('usenowplay'))
    @property
    def NOWPLAYTIME    (self) : return int(self.addon.getSetting('nowplaytime'))
    @property
    def FASTBCKP       (self) : return _sbool(self.addon.getSetting('fastbckp'))
    @property
    def SAVEONREST     (self) : return _sbool(self.addon.getSetting('saveonrest'))
    @property
    def ACSSTKN        (self) : return _sbool(self.addon.getSetting('acsstkn'))
    @property
    def USESYNC        (self) : return _sbool(self.addon.getSetting('usesync'))
    @property
    def STRTUPSYNC     (self) : return _sbool(self.addon.getSetting('strtupsync'))
    @property
    def AUTOSYNC       (self) : return _sbool(self.addon.getSetting('autosync'))
    @property
    def AUTOSYNCTIME   (self) : return int(self.addon.getSetting('autosynctime'))
    @property
    def SYLIMITTIME    (self) : return int(self.addon.getSetting('sylimittime'))
    @property
    def SYLIMITCOUNT   (self) : return int(self.addon.getSetting('sylimitcount'))
    @property
    def USEWS          (self) : return _sbool(self.addon.getSetting('usews'))
    @property        
    def STRTUPWS       (self) : return _sbool(self.addon.getSetting('strtupws'))
    @property        
    def AUTOWS         (self) : return _sbool(self.addon.getSetting('autows'))
    @property        
    def AUTOWSTIME     (self) : return int(self.addon.getSetting('autowstime'))
    @property        
    def JSIVAL         (self) : return int(self.addon.getSetting('jsival'))/100.0
    @property        
    def USELFM         (self) : return _sbool(self.addon.getSetting('uselfm'))
    @property        
    def USESRV         (self) : return _sbool(self.addon.getSetting('usesrv'))
    @property        
    def SRVSTATUSV     (self) : return _sbool(self.addon.getSetting('srvstatusv'))
    @property        
    def SRVSTATUS      (self) : return self.addon.getSetting('srvstatus')
    
    
    def getlibpath(self): _libpath  = self.addon.getSetting('libpath');  return _libpath  if _libpath  != TAG_PAR_SETDEF else self.profile
    def getbckpath(self): _bkuppath = self.addon.getSetting('bkuppath'); return _bkuppath if _bkuppath != TAG_PAR_SETDEF else self.profile
    
    def getlib(self)     : return self.addon.getSetting('fldrmov'), self.addon.getSetting('fldrtvs')
    def getshad(self)    : return _sbool(self.addon.getSetting('allowshadow'))
    def getsilent(self)  : return _sbool(self.addon.getSetting('silentupd')) 
    def getautime(self)  : return int(self.addon.getSetting('autime'))
    def getcolor(self)   : return self.addon.getSetting('mnucolor')
    def getabck(self)    : return _sbool(self.addon.getSetting('bkupauto'))
    def getbcktime(self) : return int(self.addon.getSetting('bkuptime'))
    def getsynctime(self): return int(self.addon.getSetting('autosynctime'))
    def getautosync(self): return _sbool(self.addon.getSetting('autosync'))
    def getsyncatkn(self): return _sbool(self.addon.getSetting('acsstkn'))
    def getwstime(self)  : return int(self.addon.getSetting('autowstime'))
    def getautows(self)  : return _sbool(self.addon.getSetting('autows'))  
    
    