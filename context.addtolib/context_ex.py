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
########## CONTEXT MENUE ACTIONS:

##### Import local modules ...
from resources.lib import *
import pickle


##### Compability addon vars ...
__addon__        = addon.addon 
__addonprofile__ = addon.profile
__addonname__    = addon.name
__localize__     = addon.localize
__addonid__      = addon.id
__author__       = addon.author
__version__      = addon.version
__addonpath__    = addon.path
__icon__         = addon.icon
__language__     = addon.localize



##### Call ...
def Main():

    args = parseArgs()
    if   args[0] == TAG_CND_NOACTION : plgMain()
    elif args[0] != TAG_CND_PLAY     : plgMain(*args)
    

##### Main ...
class plgMain(GUI.CAltDTmpl):        
    
    def _cleanObject(self, obj):
        try    : del obj 
        except : pass
    
    
    def lockalChangesNow(self):
        changes = self.dbx.getLocalChanges()
        if changes : self.dbx.createSyncFile()
        return changes 
    
    
    def changer(self, action, tag):
        if tag not in [TAG_MNU_CANCEL] : return
        if action and action not in [TAG_ACT_SHADOWUPD] : return 
        if self.syncAlred == True : self.syncAlred = False; return
        
        if self.useChanger == True: 
            self.useChanger = False       
            if self.lockalChangesNow() and addon.USESYNC and self.dbx.isAuthorize() : self.act_sync(hide=True)  
    
    
    # def libupdater(self, action, tag):
    #     if tag not in [TAG_MNU_CANCEL] : return
    #     #if action and action not in [TAG_ACT_SHADOWUPD] : return 
    #     if self.libUpdAlred == True : self.libUpdAlred = False; return
    #     
    #     if self.useLibUpdater == True: 
    #         self.useLibUpdater = False       
            
                
    
    # def updlock(self, action=Empty, lock=False, check=False, lcfile=Empty):
    #     if not lcfile : lcfile = TAG_PAR_LOCKF
    # 
    #     filepath = DOS.join(addon.profile, lcfile)
    #     isex     = lambda : DOS.exists(filepath) 
    # 
    #     if not check:
    #         if lock : DOS.file(lcfile, addon.profile, str(0))    
    #         else    : DOS.delf(filepath)
    #         
    #     elif isex():
    #         if not action:
    #             calln = inte(DOS.file(lcfile, addon.profile, fType=FRead))
    #             
    #             if calln < 2:
    #                 DOS.file(lcfile, addon.profile, str(calln+1), fRew=True) 
    #                 errord(TAG_ERR_LOCK, Empty); return False
    #             else: 
    #                 if not confirm (TAG_CFR_UNLOCK) : return False
    #                 DOS.delf(filepath)
    #                  
    #         else : return False
    #     
    #     return True
    # 
    # def started(self, iss, action=Empty):
    #     if action : file = TAG_PAR_STRARTAF
    #     else      : file = TAG_PAR_STRARTF
    #     
    #     if iss:
    #         check = self.updlock(action=action, check=True, lcfile=file)
    #         if check: 
    #             self.updlock(action=action, lock=True, lcfile=file)
    #             return True
    #         else : return False
    #         
    #     else : return self.updlock(lock=False, lcfile=file) 
         
        #if iss : DOS.file(file, addon.profile, Empty)
        #else   : DOS.delf(DOS.join(addon.profile, file))
    
    def started(self, action=Empty, lock=True):
        file = TAG_PAR_STRARTF
        
        filepath = DOS.join(addon.profile, file)
        
        if lock:
            if DOS.exists(filepath):
                if not action:
                    calln = inte(DOS.file2(filepath, fType=FRead)) 
                    if calln < 2:
                        DOS.file2(filepath, str(calln+1), fRew=True) 
                        errord(TAG_ERR_LOCK, Empty)
                        return False
                    else: 
                        if not confirm (TAG_CFR_UNLOCK) : return False
                        wait(2)
                else : return False
            else : DOS.file2(filepath, str(0))
        else : DOS.delf(filepath)
        
        return True
        
    
    def check_exilib(self, action):
        DOS.mkdirs(LIB.lib)
        if not DOS.exists(LIB.lib): 
            if not action:
                errord(TAG_ERR_LIB, Empty)
                self.mnu_set()
                return False
                
            elif action != TAG_ACT_LPRESET:
                errord(TAG_ERR_LIBACT, Empty)
                return False
                
        return True


    def setTVS(self, path, isFound):
        self._cleanObject(self.TVS)
        self.path    = path 
        self.isFound = isFound
        if self.isMovie and isFound : self.isMovie = False; self.forcetvstitle = True
        self.TVS = CTVS.TVS(TAG_PAR_TVSPACK_FILE, path, isFound)
        self.setSRC()
    
    
    def setLI(self, dirPath=Empty, srcName=Empty):
        self._cleanObject(self.items)
        self.items = LI.vidItems(dirPath, srcName)
    
    
    def importLI(self, filename):
        filepath = DOS.join(addon.profile, filename)
        file = open(filepath, 'rb')
        _object = pickle.load(file)
        file.close()
        DOS.delf(filepath)
        self.items = _object
    
    
    def loadLI(self, items):
        self._cleanObject(self.items)
        self.items = items
    
        
    def setLinkTable(self):
        self._cleanObject(self.linkTable)
        self.linkTable = CTVS.CLinkTable(TAG_PAR_STL_FILE, LIB.lib)
    
    
    def setSRC(self):
        self._cleanObject(self.src)
        self.src = CSRC(*self.TVS.get_names_and_links())
    
    
    def setFile(self, rep=False):
        self.isFound, self.container, self.path, isOL, self.isMovie = checkfile(self.items, self.linkTable)
        if rep and isOL : errord(TAG_ERR_OL, Empty) 
    
    
    # def libClean(self, always=False, path=Empty):
    #     if addon.UPDAFTER or always: 
    #         if GUI.dlgYn (tl(TAG_CFR_CLEANVL)) : GUI.libClean(path)
    
    def libClean(self, always=False, path=Empty):
        if GUI.dlgYn (tl(TAG_CFR_CLEANVL)) : GUI.libClean(path)
    
    
    # def libUpdate(self, report=False, always=False, path=Empty):
    #     if addon.UPDAFTER or always: 
    #         GUI.libUpdate(path)
    #         if self.container in [TAG_CON_VID, TAG_CON_LOCAL]: GUI.refresh()
    #         if report : errord(TAG_ERR_OK, TAG_ERR_OK_VIDLIBU)
    
    def libUpdate(self, report=False, always=False, path=Empty):
        GUI.libUpdate(path)
        if self.container in [TAG_CON_VID, TAG_CON_LOCAL]: GUI.refresh()
    
    
    def back(self):
        GUI.back()
     
        
    def doAction(self, action=Empty):
        ## Redefine values ... 
        self.setSRC() 
        self.isNewSource    = self.src.isnewsrc(self.items.vidCPath)
        self.isNewFolSource = self.src.isnewfrc(self.items.vidCPath)
    
        ## Delete existing menues ...
        try    : del self.MainMenue, self.tvsmMenue, self.srcmMenue, self.updtMenue 
        except : pass
        
        ## Title correction ...
        itemTitle = self.items.vidCurr
        if (self.container in [TAG_CON_VID] and not itemTitle.endswith('.strm') and not self.forcetvstitle) or self.isMovie:
            #if itemTitle.endswith('.strm') : itemTitle = normName(itemTitle.replace('.strm', Empty))
            correctTitle = itemTitle
        else : correctTitle = normName(self.TVS.lib_name)
        
        ## Define Visible conditions ...
        curVisCond         = {self.container,
                              TAG_CND_NOTFOUND  if not self.isFound           else TAG_CND_FOUND,
                              TAG_CND_NEWSRC    if self.isNewSource           else TAG_CND_OLDSRC,
                              TAG_CND_NEWFRC    if self.isNewFolSource        else TAG_CND_OLDFRC,
                              TAG_TYP_FOLDER    if self.items.vidIsFolder     else TAG_TYP_FILE,
                              TAG_CND_LISTEMPTY if self.items.vidIsEmpty      else Empty,
                              TAG_CND_NOUPD     if not addon.ADDUPD           else Empty,
                              TAG_CND_UPDPRC    if isGlUpProcess()            else TAG_CND_NOUPDPRC,
                              TAG_CND_NOGL      if isNoGlUp()                 else Empty,
                              TAG_CND_NOTISMOV  if not self.isMovie           else TAG_CND_ISMOV,
                              TAG_CND_DBXNOAUTH if not self.dbx.isAuthorize() else Empty}
        
                              
        ## Define Main Menue ...
        self.MainMenue = tagMenue({'pos':0, 'tag':TAG_MNU_DELMOV,   'hideCond':{TAG_CND_NOTISMOV}},
                                  {'pos':1, 'tag':TAG_MNU_DELTVS,   'hideCond':{TAG_CND_NOTFOUND, TAG_CON_EXT}},
                                  {'pos':2, 'tag':TAG_MNU_MOV,      'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_TYP_FOLDER}},
                                  {'pos':3, 'tag':TAG_MNU_TVS,      'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_LISTEMPTY, TAG_CND_OLDSRC}},
                                  {'pos':4, 'tag':TAG_MNU_TVSSTALN, 'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_LISTEMPTY, TAG_CND_NEWSRC}},
                                  {'pos':5, 'tag':TAG_MNU_RAWADD,   'hideCond':{TAG_CON_LOCAL, TAG_CON_VID}},
                                  {'pos':6, 'tag':TAG_MNU_TVSU,     'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_LISTEMPTY, TAG_CND_NEWSRC}},
                                  {'pos':7, 'tag':TAG_MNU_ADDFOL,   'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_OLDFRC}},
                                  {'pos':8, 'tag':TAG_MNU_UPDFOL,   'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_NEWFRC}},
                                  {'pos':9, 'tag':TAG_MNU_CONTUPD,  'hideCond':{TAG_CND_NOUPDPRC}},
                                  {'pos':10,'tag':TAG_MNU_OPEN,     'hideCond':{TAG_CND_NOTFOUND}},
                                  {'pos':11,'tag':TAG_MNU_CHKNEW,   'hideCond':{TAG_CND_NOTFOUND}},
                                  {'pos':12,'tag':TAG_MNU_CHKNEWGL, 'hideCond':{}},
                                  {'pos':13,'tag':TAG_MNU_CONTUPD,  'hideCond':{TAG_CND_UPDPRC, TAG_CND_NOGL}},
                                  {'pos':14,'tag':TAG_MNU_VIDLIBU,  'hideCond':{TAG_CND_NOUPD}},
                                  {'pos':15,'tag':TAG_MNU_VIDLIBCLN,'hideCond':{TAG_CND_NOUPD}},
                                  {'pos':16,'tag':TAG_MNU_SRCMAN,   'hideCond':{(TAG_CON_LOCAL, TAG_CND_NOTFOUND), (TAG_CON_VID, TAG_CND_NOTFOUND)}},
                                  {'pos':17,'tag':TAG_MNU_UPDMAN,   'hideCond':{}},
                                  {'pos':18,'tag':TAG_MNU_TVSMAN,   'hideCond':{TAG_CND_ISMOV}},
                                  {'pos':19,'tag':TAG_MNU_PBTYPES,  'hideCond':{TAG_CON_EXT}},
                                  {'pos':20,'tag':TAG_MNU_DBSYNC,   'hideCond':{TAG_CND_DBXNOAUTH}},         
                                  {'pos':1, 'tag':TAG_MNU_HELP,     'hideCond':{}, 'refPage':addon.SETPAGE-1},
                                  {'pos':2, 'tag':TAG_MNU_SET,      'hideCond':{}, 'refPage':addon.SETPAGE-1},
                                  pageLimit = addon.MNUITMNUM,
                                  cancelTag = TAG_MNU_CANCEL, 
                                  backTag   = TAG_MNU_BACK, 
                                  nextTag   = TAG_MNU_MORE,
                                  visCond   = curVisCond,
                                  #title     = normName(self.TVS.lib_name) if not self.isMovie else self.items.vidCurr,
                                  title     = correctTitle,
                                  addict    = tla(TAG_TTL_MAINMNU)) 
         
        ## Define Sub Menues ... 
        self.tvsmMenue = tagMenue({'pos':0, 'tag':TAG_MNU_SHOWALL,    'hideCond':{}},  
                                  {'pos':1, 'tag':TAG_MNU_JOIN,       'hideCond':{}},
                                  {'pos':2, 'tag':TAG_MNU_DELETE,     'hideCond':{}},
                                  {'pos':3, 'tag':TAG_MNU_TVSREN,     'hideCond':{}},
                                  {'pos':4, 'tag':TAG_MNU_RESTORE,    'hideCond':{}},
                                  {'pos':5, 'tag':TAG_MNU_RESTOREALL, 'hideCond':{}},
                                  {'pos':6, 'tag':TAG_MNU_REBSTL,     'hideCond':{}},
                                  {'pos':7, 'tag':TAG_MNU_RESCANFULL, 'hideCond':{}},
                                  pageLimit = addon.MNUITMNUM,
                                  cancelTag = TAG_MNU_BACKMAIN, 
                                  backTag   = TAG_MNU_BACK, 
                                  nextTag   = TAG_MNU_MORE,
                                  visCond   = curVisCond,
                                  title     = titName(TAG_MNU_TVSMAN, self.TVS.lib_name),
                                  addict    = tla(TAG_TTL_MAINMNU)+TAG_PAR_LNSEP+tla(TAG_MNU_TVSMAN))
        
        self.srcmMenue = tagMenue({'pos':0, 'tag':TAG_MNU_RESCAN,    'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_NOTFOUND, TAG_CND_NEWSRC}},
                                  {'pos':1, 'tag':TAG_MNU_BRWSREN,   'hideCond':{TAG_CND_NOTFOUND}},
                                  #{'pos':1, 'tag':TAG_MNU_ADVADD,    'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_LISTEMPTY}},   
                                  {'pos':2, 'tag':TAG_MNU_REMSRC,    'hideCond':{TAG_CND_NOTFOUND}},
                                  {'pos':3, 'tag':TAG_MNU_SRCREN,    'hideCond':{TAG_CND_NOTFOUND}},
                                  {'pos':4, 'tag':TAG_MNU_RESCANALLS,'hideCond':{TAG_CND_NOTFOUND}},
                                  pageLimit = addon.MNUITMNUM,
                                  cancelTag = TAG_MNU_BACKMAIN, 
                                  backTag   = TAG_MNU_BACK, 
                                  nextTag   = TAG_MNU_MORE,
                                  visCond   = curVisCond,
                                  title     = titName(TAG_MNU_SRCMAN, self.TVS.lib_name),
                                  addict    = tla(TAG_TTL_MAINMNU)+TAG_PAR_LNSEP+tla(TAG_MNU_SRCMAN))
        
        self.updtMenue = tagMenue({'pos':0, 'tag':TAG_MNU_TVSU,     'hideCond':{}},
                                  {'pos':1, 'tag':TAG_MNU_SHDIR,    'hideCond':{}},  
                                  pageLimit = addon.MNUITMNUM,
                                  cancelTag = TAG_MNU_BACKMAIN, 
                                  backTag   = TAG_MNU_BACK, 
                                  nextTag   = TAG_MNU_MORE,
                                  visCond   = curVisCond,
                                  title     = titName(TAG_TTL_NEWEPS, self.TVS.lib_name),
                                  addict    = tla(TAG_TTL_MAINMNU)+TAG_PAR_LNSEP+tla(TAG_MNU_UPDMAN))
    
        ## Show Main menue ...
        if self.result not in [TAG_MNU_TVS,     TAG_MNU_TVSU,    TAG_MNU_TVSMAN,  TAG_MNU_SRCMAN, TAG_MNU_DELETE, 
                               TAG_MNU_RESTORE, TAG_MNU_TVSREN,  TAG_MNU_REMSRC,  TAG_MNU_SRCREN, TAG_MNU_CHKNEW,
                               TAG_MNU_BRWSREN, TAG_MNU_PBTYPES, TAG_MNU_VIDLIBU, TAG_MNU_VIDLIBCLN, TAG_MNU_DBSYNC] and not action:
                                             
                                             self.pageNum,  self.result = self.MainMenue.show(self.pageNum)
                                             
        elif action : self.result = action 
                          
        ## Show Sub menues ...   
        if   self.result == TAG_MNU_SRCMAN : self.srcmPage, self.result = self.srcmMenue.show(self.srcmPage)  
        elif self.result == TAG_MNU_TVSMAN : self.tvsmPage, self.result = self.tvsmMenue.show(self.tvsmPage)
        
        #if not self.updlock(action, check=True) : self.result = TAG_MNU_CANCEL
        
        ## Parse results ...
        if   self.result == TAG_MNU_CANCEL        : pass
        elif self.result == TAG_MNU_ADDFOL        : self.result = self.mnu_addfol()
        elif self.result == TAG_MNU_UPDFOL        : self.result = self.mnu_updfol()
        elif self.result == TAG_MNU_BRWSREN       : self.result = self.mnu_brwsren()
        elif self.result == TAG_MNU_JOIN          : self.result = self.mnu_join()
        elif self.result == TAG_MNU_TVSREN        : self.result = self.mnu_tvsren()
        elif self.result == TAG_MNU_SRCREN        : self.result = self.mnu_scrren()
        elif self.result == TAG_MNU_REMSRC        : self.result = self.mnu_remsrc()
        elif self.result == TAG_MNU_UPDMAN        : self.result = self.mnu_updman()
        elif self.result == TAG_MNU_SHOWALL       : self.result = self.mnu_showall()
        elif self.result == TAG_MNU_CHKNEW        : self.result = self.mnu_chknew()
        elif self.result == TAG_MNU_CHKNEWGL      : self.result = self.mnu_chknewgl()
        elif self.result == TAG_MNU_CONTUPD       : self.result = self.mnu_chknewgl(True)
        elif self.result == TAG_MNU_DELETE        : self.result = self.mnu_delete()
        elif self.result == TAG_MNU_RESTORE       : self.result = self.mnu_restore()
        elif self.result == TAG_MNU_RESTOREALL    : self.result = self.mnu_restoreall()
        elif self.result == TAG_MNU_RESCAN        : self.result = self.mnu_rescan()
        elif self.result == TAG_MNU_REBSTL        : self.result = self.mnu_rebstl()
        elif self.result == TAG_MNU_RAWADD        : self.result = self.mnu_rawadd()
        elif self.result == TAG_MNU_MOV           : self.result = self.mnu_mov()
        elif self.result == TAG_MNU_TVS           : self.result = self.mnu_tvs()
        elif self.result == TAG_MNU_TVSU          : self.result = self.mnu_tvsu()
        elif self.result == TAG_MNU_TVSSTALN      : self.result = self.mnu_tvsstaln()
        elif self.result == TAG_MNU_ADVADD        : self.result = self.mnu_advadd()
        elif self.result == TAG_MNU_OPEN          : self.result = self.mnu_open()
        elif self.result == TAG_MNU_HELP          : self.result = self.mnu_help()
        elif self.result == TAG_MNU_SET           : self.result = self.mnu_set()
        elif self.result == TAG_MNU_VIDLIBU       : self.result = self.mnu_vidlibu()
        elif self.result == TAG_MNU_VIDLIBCLN     : self.result = self.mnu_vidlibcln()
        elif self.result == TAG_MNU_RESCANALLS    : self.result = self.mnu_rescanalls()
        elif self.result == TAG_MNU_RESCANFULL    : self.result = self.mnu_rescanfull()
        elif self.result == TAG_MNU_PBTYPES       : self.result = self.mnu_pbtypes()
        elif self.result == TAG_MNU_DBSYNC        : self.result = self.mnu_dbsync()
        elif self.result == TAG_MNU_DELMOV        : self.result = self.mnu_delmov()
        elif self.result == TAG_MNU_DELTVS        : self.result = self.mnu_deltvs()
        elif self.result == TAG_ACT_LPRESET       : self.result = self.act_lpreset()
        elif self.result == TAG_ACT_SHADOWUPD     : self.result = self.act_shadowupd()
        elif self.result == TAG_ACT_DONOTHING     : self.result = self.act_donothing()
        elif self.result == TAG_ACT_CHCOLOR       : self.result = self.act_chcolor()
        elif self.result == TAG_ACT_RENAMER       : self.result = self.act_renamer()
        elif self.result == TAG_ACT_BACKUP        : self.result = self.act_backup()
        elif self.result == TAG_ACT_REMBACK       : self.result = self.act_remback()
        elif self.result == TAG_ACT_RESTBACK      : self.result = self.act_restback()
        elif self.result == TAG_ACT_RESETTBU      : self.result = self.act_resettbu()
        elif self.result == TAG_ACT_AUTOBACKUP    : self.result = self.act_autobackup()
        elif self.result == TAG_ACT_RESKIN        : self.result = self.act_reskin()
        elif self.result == TAG_ACT_DBXCONNECT    : self.result = self.act_DBXConnect()
        elif self.result == TAG_ACT_DBXDISCONNECT : self.result = self.act_DBXDisconnect()
        elif self.result == TAG_ACT_SYNC          : self.result = self.act_sync()
        elif self.result == TAG_ACT_WATCHSYNC     : self.result = self.act_watchsync()
        elif self.result == TAG_ACT_STOPSRV       : self.result = self.act_stopsrv()
        elif self.result == TAG_ACT_STARTSRV      : self.result = self.act_startsrv()
        
        ## Check changes ...
        self.changer(action, tag=self.result)
    
    
    def __init__(self, action=Empty, importLI=Empty, loadLI=Empty):   
    
        ## Check and lock ...
        if not self.started(action) : return    
        if not self.check_exilib(action) : return
        #if not self.updlock(action, check=True) : return
        check_lib_folders(False)
        
        CTVS.BGPROCESS = addon.BGUPD
        LI.DETVIDEXT   = addon.DETVIDEXT
    
        ## Define empty objects ...
        self.linkTable = None
        self.items     = None
        self.TVS       = None
        self.src       = None
        
        self.fListUPD  = []
        self.sListUPD  = []
        self.reErrors  = []
        
        self.forcetvstitle = False
            
        ## Set defaults ...
        if importLI : self.importLI(importLI)
        elif loadLI : self.loadLI(loadLI) 
        else        : self.setLI()
        
        self.setLinkTable()
        self.setFile(True if not action else False)
        self.setTVS(self.path, self.isFound)
        
        self.dbx = sync.dbxSync()
        self.useChanger = False
        self.syncAlred  = False
        
        self.result   = Empty
        self.pageNum  = 0
        self.tvsmPage = 0
        self.srcmPage = 0
        self.updtPage = 0
        
        ## Start main menue process ...
        while self.result != TAG_MNU_CANCEL : self.doAction(action)
        
        ## Unlock ...
        #self.updlock(lock=False)
        self.started(action, lock=False)
        
        ## Delete all objects ...
        del self.srcmMenue, self.tvsmMenue, self.updtMenue, self.MainMenue, self.src, self.items, self.TVS, self.linkTable 
    
    
    
    def mnu_addfol(self): 
    
        rd = TAG_MNU_SRCMAN
                                                                     
        tvsNames, tvsPaths = getAllTVS()
        newPath = subMenue(tvsNames, tvsPaths, cancelVal=Empty, default=DOS.unsl(self.TVS.lib_path), 
                           title=titName(TAG_MNU_ADDFOL, self.TVS.lib_name))
                           
        if not newPath : return rd 
        
        self.setTVS(newPath, True) 
        if not errord(addFolSRC(self.items, self.TVS), TAG_ERR_OK_ADDFOL, normName(self.TVS.lib_name)):
            self.linkTable.add(self.TVS.lib_path, self.items.vidCPath)
            self.useChanger = True
                
        return rd
        
        
    def mnu_updfol(self):  
    
        rd = TAG_MNU_CANCEL
                                                                 
        if not errord(updFolSRC(self.items, self.TVS), TAG_ERR_OK_UPDFOL, normName(self.TVS.lib_name)):
            self.useChanger = True
        
        return rd
        
        
    def mnu_brwsren(self):
    
        rd = TAG_MNU_BRWSREN
        
        srccl = self.src.clone(nofrc=True)
        
        mdefault = srccl.getlinkidx(self.items.vidCPath)
        srccl(subMenue(srccl.remnames, srccl.idxs, cancelVal=-1, default=mdefault, defidx=0, 
                          title=titName(TAG_MNU_BRWSREN, self.TVS.lib_name)))
                          
        if not srccl.isidx : return TAG_MNU_SRCMAN
        
        while True: 
        
            epsnames, epslinks = self.TVS.get_eps_names_and_links_forsrc(srccl.link)
            valnames = [itm for itm in epsnames]
            
            #reslink = subMenue(epsnames, epslinks, cancelVal=Empty, title=tl(TAG_TTL_BRWSREN) % (tla(TAG_MNU_BRWSREN), normName(self.TVS.lib_name), srccl.name))
            oldname = subMenue(epsnames, valnames, cancelVal=Empty, title=tl(TAG_TTL_BRWSREN) % (tla(TAG_MNU_BRWSREN), normName(self.TVS.lib_name), srccl.name))
            
            #if not reslink : return rd
            if not oldname : return rd
            
            scr_id = self.TVS.get_src_id(srccl.link)
            
            typ = subMenue([TAG_DLG_RENM, TAG_DLG_PBTREM], cancelVal=Empty, title=oldname)
            
            if not typ : return rd
            elif typ == TAG_DLG_PBTREM:
                errord(removeEPS(self.TVS, scr_id, oldname), TAG_ERR_OK_EPSREM, normName(self.TVS.lib_name))
                
            elif typ == TAG_DLG_RENM:
            
                #oldname = self.TVS.get_eps_name_by_link(reslink) 
                newName = GUI.dlgIn(tl(TAG_TTL_BRWSRENEP), oldname)
                
                if oldname != newName:
                    prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty          
                    #errord(renEPS(self.TVS, reslink, newName, oldname, prefix), TAG_ERR_OK_BRWSREN, normName(self.TVS.lib_name))
                    errord(renEPS(self.TVS, scr_id, newName, oldname, prefix), TAG_ERR_OK_BRWSREN, normName(self.TVS.lib_name))
            
            if VideoLib().removeEpisode(self.TVS.lib_path, DOS.join(self.TVS.lib_path, oldname+'.strm')):
                self.libUpdate(path=self.TVS.lib_path)
                self.useChanger = True
        
        return rd
    
    
    def mnu_rebstl(self):
        
        rd = TAG_MNU_TVSMAN
        
        if not errord(rebuildLinkTable(), TAG_ERR_OK_REBSTL):
            self.useChanger = True
        
        return rd
        
        
    def mnu_join(self):    
    
        rd = TAG_MNU_TVSMAN
                                                              
        tvsNames, tvsPaths = getAllTVS()
        tvsNames2 = [itm for itm in tvsNames]
        tvsPaths2 = [itm for itm in tvsPaths]
        joinPaths = subMenue(tvsNames, tvsPaths, cancelVal=Empty, cancelName=TAG_MNU_OK, multiSel=True, selMarkm=tl(TAG_MNU_SMM), 
                             default=DOS.unsl(self.TVS.lib_path), title=titName(TAG_MNU_JOIN))
        
        if len(joinPaths) < 2 : errord(TAG_ERR_NOTOJOIN, Empty); return rd
        
        if not confirm (TAG_MNU_JOIN) : return rd
        
        tvsNames2.insert(0, tl(TAG_MNU_NEW))
        tvsPaths2.insert(0, TAG_MNU_NEW)            
        mainPaths = subMenue(tvsNames2, tvsPaths2, cancelVal=Empty, default=DOS.unsl(self.TVS.lib_path), defidx=1, title=titName(TAG_TTL_CHSNAME))
                             
        if    not mainPaths            : return rd 
        elif  mainPaths == TAG_MNU_NEW : newName = GUI.dlgIn(tl(TAG_TTL_ENTNAME))
        else                           : newName = Empty
          
        errn, path, name = joinTVSs(joinPaths, mainPaths, newName, self.linkTable)
        
        if not errord(errn, TAG_ERR_OK_JOIN, normName(name)):  
            self.setTVS(path, True)
            self.libClean()
            self.libUpdate(path=LIB.tvsf)
            self.useChanger = True
                
        return  rd
        
        
    def mnu_tvsren(self): 
    
       rd = TAG_MNU_TVSMAN
                   
       tvsNames, tvsPaths = getAllTVS()
       newPath = subMenue(tvsNames, tvsPaths, cancelVal=Empty, default=DOS.unsl(self.TVS.lib_path), title=titName(TAG_MNU_TVSREN))
       
       if not newPath : return rd
       
       self.setTVS(newPath, True) 
       oldName = self.TVS.lib_name 
       newName = GUI.dlgIn(tl(TAG_MNU_TVSREN), oldName)
       
       prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty
       if not errord(renameTVS(newName, self.TVS, prefix), TAG_ERR_OK_TVSREN, normName(oldName)):
           self.linkTable.chpath(newPath, self.TVS.lib_path)
           #self.libClean()
           if not VideoLib().removeTVS(newPath) : self.libClean()
           self.libUpdate(path=LIB.tvsf)
           self.useChanger = True 
           return TAG_MNU_TVSREN 
       
       return rd
       
        
    def mnu_scrren(self):
     
        rd = TAG_MNU_SRCMAN
                                                                     
        mdefault=self.src.getlinkidx(self.items.vidCPath)
        mdefidx=self.src.frclen if mdefault >= self.src.frclen else 0
        self.src(subMenue(self.src.remnames, self.src.idxs, cancelVal=-1, default=mdefault, defidx=mdefidx, 
                          title=titName(TAG_MNU_SRCREN, self.TVS.lib_name)))
                          
        if not self.src.isidx : return rd
          
        oldName = self.src.name 
        newName = GUI.dlgIn(tl(TAG_MNU_SRCREN), oldName)
         
        if not newName : return  rd
        
        if not errord(renameSRC(oldName, newName, self.src.isf, self.TVS), TAG_ERR_OK_SRCREN, normName(self.TVS.lib_name)):
            self.useChanger = True
            return  TAG_MNU_SRCREN
        
        return  rd
         
         
    def mnu_remsrc(self):                
    
        rd = TAG_MNU_SRCMAN
                                                  
        mdefault=self.src.getlinkidx(self.items.vidCPath)
        mdefidx=self.src.frclen if mdefault >= self.src.frclen else 0                                                 
        self.src(subMenue(self.src.remnames, self.src.idxs, cancelVal=-1, default=mdefault, defidx=mdefidx,
                          title=titName(TAG_MNU_REMSRC, self.TVS.lib_name)))
                           
        if not self.src.isidx : return rd
         
        if not confirm(TAG_MNU_REMSRC, normName(self.TVS.lib_name), self.src.name) : return rd
        
        prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty
        if not errord(removeSRC(self.src.link, self.src.isf, self.TVS, prefix), TAG_ERR_OK_REMSRC, normName(self.TVS.lib_name)):
           self.linkTable.remove(self.src.link) 
           #self.libClean()
           #if not VideoLib().removeTVS(self.TVS.lib_path) : self.libClean()
           if not VideoLib().eviscerateTVS(self.TVS.lib_path) : self.libClean() 
           self.libUpdate(path=LIB.tvsf)
           self.useChanger = True
        
        return rd
         
        
    def mnu_updman(self):                  
    
        rd = TAG_MNU_BACKMAIN
        
        exclude_addon = True
        
        if self.isFound:
            vrnts = [TAG_DLG_CURRTVS, TAG_TTL_EXITVS, TAG_DLG_EXCLADDON]
        else:
            vrnts = [TAG_TTL_EXITVS, TAG_DLG_EXCLADDON]    
            
        result = subMenue(vrnts, cancelVal=-1, cancelName=TAG_MNU_CANCEL, title=titName(TAG_MNU_UPDMAN, self.TVS.lib_name))
        if   result == -1 : return rd
        elif result == TAG_TTL_EXITVS:
            if self.mnu_showall() == TAG_MNU_TVSMAN : return rd 
            result = TAG_DLG_CURRTVS
        
        if   result == TAG_DLG_CURRTVS:
            exclude_addon = False            
            srcDef, frcDef = self.TVS.get_upd()
            mdefault=self.src.getlinkidx(self.items.vidCPath)
            mdefidx=self.src.frclen if mdefault >= self.src.frclen else 0
            self.src(subMenue(self.src.remnames, self.src.idxs, cancelVal=-1, cancelName=TAG_MNU_OK, multiSel=True, default=mdefault, selMarkm=tl(TAG_MNU_SM),
                         multiSelDefList=self.src.getidxs(frcDef+srcDef), defidx=mdefidx, title=titName(TAG_MNU_UPDMAN, self.TVS.lib_name)))
                            
            if not errord(setupdSRC(self.src.fnames, self.src.snames, self.TVS), TAG_ERR_OK_SETUPD, normName(self.TVS.lib_name)):
                self.useChanger = True
        
        if exclude_addon:
            plugs = getTVSsPlugs()
            plugsNemes = [prefixToName(plg) for plg in plugs]
        
            plugin = subMenue(plugsNemes, plugs, cancelVal=-1, title=tla(TAG_DLG_EXCLADDON))
            
            if plugin == -1 or not GUI.dlgYn(tl(TAG_CFR_EXCLPLUG) % (prefixToName(plugin)), title=tla(TAG_DLG_EXCLADDON)) : return rd
            
            if not errord(excludeUPDPlug(plugin), TAG_ERR_OK_EXCLUPLUG):
                self.setTVS(self.TVS.lib_path, self.isFound)
                self.useChanger = True
        
        return rd  
        
        
    def mnu_showall(self):
    
        rd = TAG_MNU_TVSMAN
                                                                  
        tvsNames, tvsPaths = getAllTVS()
        
        if not tvsNames : return rd
         
        newPath = subMenue(tvsNames, tvsPaths, cancelVal=Empty, default=DOS.unsl(self.TVS.lib_path), title=titName(TAG_TTL_EXITVS))
        
        if not newPath  : return rd
         
        self.setTVS(newPath, True)
        self.pageNum = 0
        self.forcetvstitle = True
        
        return Empty 
        
        
    def mnu_chknew(self, globalupd=False, silent=False, shadsl=False):
        #self.updlock(lock=True)  
        if addon.AUTOUPDSRC and addon.SILENTUPD and not globalupd:
            while True:
                result = self._mnu_chknew()
                if result != TAG_MNU_CHKNEW : return result
        
        else : return self._mnu_chknew(exsilent=silent, exshadu=True if globalupd and addon.AUTOUPDALL else shadsl, shadow=shadsl)  
        
        
    def _mnu_chknew(self, exsilent=False, exshadu=False, shadow=False):                                         
    
        rd = TAG_MNU_CANCEL
        
        self.chkfull = False
        updnow(False)
        
        try    : self.usrc
        except : self.usrc = CSRC(*self.TVS.check_new_eps(titName(TAG_TTL_CHKUPD, self.TVS.lib_name)))
              
        if not self.usrc.idxs : errord(TAG_ERR_OK, TAG_ERR_OK_CHKNEW, normName(self.TVS.lib_name)); del self.usrc; return rd
        
        remnames = [itm for itm in self.usrc.remnames]
        idxs     = [itm for itm in self.usrc.idxs]
        
        nosilent = True if not exsilent and not self.usrc.srccount() else False
        allowmnu = True if not addon.AUTOUPDSRC and not exshadu else False  
        if allowmnu or nosilent or not addon.SILENTUPD: 
        
            mdefault=self.usrc.getlinkidx(self.items.vidCPath) 
            mdefidx=self.usrc.frclen if mdefault >= self.src.frclen else 0
            self.usrc(subMenue(remnames, idxs, cancelVal=-1, default=mdefault, 
                               defidx=mdefidx, title=titName(TAG_TTL_NEWEPS, self.TVS.lib_name)))
                            
            #if not self.usrc.isidx : del self.usrc; return TAG_MNU_BACKMAIN
            if not self.usrc.isidx : del self.usrc; return rd
        
        else: 
            if not self.usrc.nextsidx():
                del self.usrc 
                return rd 
        
        if not addon.SILENTUPD:
        
            oldCont = self.items.vidCPath
            GUI.goTarget(self.usrc.link)
        
            if oldCont != self.usrc.link and not isWait(oldCont, LI.getCpath, addon.LNKTIMEOUT) : errord(TAG_ERR_DEDLINK); return TAG_MNU_CHKNEW 
        
            self.setLI()
         
            if self.usrc.isf : updnow(True); return rd 
            else             :
                self.TVS.os_getraw()
                if self.usrc.link not in self.TVS.get_raw_link_list() : self.mnu_tvsu  (False)
                else                                                  : self.mnu_rawadd(True)
        
            self.back()
            
        else: 
            
            self.setLI(self.usrc.link, self.usrc.name)
            if self.usrc.isf:
                oldCont = self.items.vidCPath 
                GUI.goTarget(self.usrc.link)
                if oldCont != self.usrc.link and not isWait(oldCont, LI.getCpath, addon.LNKTIMEOUT) : errord(TAG_ERR_DEDLINK); return TAG_MNU_CHKNEW
                updnow(True)
                return rd
                
            self.TVS.os_getraw()
            if self.usrc.link not in self.TVS.get_raw_link_list() : self.mnu_tvsu  (False)
            elif not (addon.NOREPRAWAUTO and shadow)              : self.mnu_rawadd(True)
        
        self.setLI()
             
        self.usrc.exclude(self.usrc.link)
    
        if self.usrc.idxs : return TAG_MNU_CHKNEW       
        
        del self.usrc
        
        self.libUpdate(path=self.TVS.lib_path)
        self.useChanger = True
        self.chkfull = True
        
        return rd 
    
    
    def act_shadowupd(self):
        #if DOS.exists(DOS.join(addon.profile, TAG_PAR_STRARTF)) : return TAG_MNU_CANCEL 
        #self.updlock(lock=True)
        self.mnu_chknewgl(shadow=addon.NOREPAUTO, shadu=True)
        if addon.NOREPAUTO and self.fListUPD : errord(TAG_ERR_OK, TAG_ERR_OK_NEWFRC)
        
        return TAG_MNU_CANCEL  
    
        
    def mnu_chknewgl(self, updreload=False, shadow=False, shadu=False):
        #self.updlock(lock=True)
        updnow(False)
        if updreload : self.sListUPD, self.fListUPD = loadTVSupd()
        resgl = self._mnu_chknewgl(updreload, shadow, shadu)
        if self.sListUPD or self.fListUPD : saveTVSupd(self.sListUPD, self.fListUPD)
        else                              : clearTVSupd() 
        
        if not updreload and not shadu : emgrControl().setLAACTT(TAG_ACT_SHADOWUPD)
        
        return resgl 
        
    
    def _mnu_chknewgl(self, updreload=False, shadow=False, shadu=False):
    
        rd = TAG_MNU_CANCEL
        
        auFinish = False if (addon.AUTOUPDALL or shadu) and addon.SILENTUPD else True
    
        if not updreload : self.sListUPD, self.fListUPD = globalUpdateCheck(shadbg=shadu)
        
        while True:
        
            if not self.sListUPD and not self.fListUPD : errord(TAG_ERR_OK, TAG_ERR_OK_CHKNEW); return rd
        
            tvsNames  = [tl(TAG_MNU_SRE) + normName(itm['name']) for itm in self.fListUPD] + [normName(itm['name']) for itm in self.sListUPD] 
            tvsVals   = range(len(tvsNames))
        
            if (not addon.AUTOUPDALL and not shadu) or not addon.SILENTUPD or auFinish:
                result = subMenue(tvsNames, tvsVals, cancelVal=-1, title=titName(TAG_MNU_CHKNEWGL))
            else: 
                if self.sListUPD : result = len(self.fListUPD) 
                elif shadow : return rd
                else        : auFinish = True; continue   
            
            #if result == -1 : return TAG_MNU_BACKMAIN
            if result == -1 : return rd
            
            if result < len(self.fListUPD) : idx = result;            self.setTVS(self.fListUPD[idx]['path'], True); name = self.fListUPD[idx]['name'] 
            else                   : idx = result-len(self.fListUPD); self.setTVS(self.sListUPD[idx]['path'], True); name = self.sListUPD[idx]['name']
            
            flst = [[], []]
            for itm in self.fListUPD:
                if itm['name'] == name : flst = [itm['ups'][0], itm['ups'][1]]; break
            
            slst = [[], []]
            for itm in self.sListUPD:
                if itm['name'] == name : slst = [itm['ups'][0], itm['ups'][1]]; break
            
            lst = slst + flst 
            self.usrc = CSRC(*lst)
            del flst, slst, lst 
            
            while True:
            
                glsilent = True if (addon.AUTOUPDALL or shadu) and addon.SILENTUPD and not auFinish else False
                upres = self.mnu_chknew(globalupd=True, silent=glsilent, shadsl=shadu) 
                
                idxf = -1; idxs = -1 
                for i, itm in enumerate(self.fListUPD):   
                    if itm['name'] == name : idxf = i; break
                for i, itm in enumerate(self.sListUPD):   
                    if itm['name'] == name : idxs = i; break
                     
                try    : self.fListUPD[idxf]['ups'] = self.usrc.getfrc()
                except : pass
                try    : self.sListUPD[idxs]['ups'] = self.usrc.getsrc()   
                except : pass
                 
                if idxf > -1 and (not self.fListUPD[idxf]['ups'][0] or self.chkfull) : self.fListUPD.pop(idxf)
                if idxs > -1 and (not self.sListUPD[idxs]['ups'][0] or self.chkfull) : self.sListUPD.pop(idxs)
                
                if upres == TAG_MNU_BACKMAIN : break
                if upres == TAG_MNU_CANCEL   : 
                    if isUpdnow() : return rd
                    else          : break 
                    
            del tvsNames, tvsVals
            if not self.sListUPD and not self.fListUPD : break
            
        return rd
                   
                   
    def mnu_delete(self):                                    
        
        rd = TAG_MNU_TVSMAN
                                                              
        tvsNames, tvsPaths = getAllTVS()
        newPath = subMenue(tvsNames, tvsPaths, cancelVal=Empty, default=DOS.unsl(self.TVS.lib_path), title=titName(TAG_MNU_DELETE))
        
        if not newPath : return rd
         
        if not confirm(TAG_MNU_DELETE, normTargetName(newPath)) : return rd
        
        self.setTVS(newPath, True)
        if not errord(deleteTVS(self.TVS), TAG_ERR_OK_DELETE, normName(self.TVS.lib_name)):
            noClean = VideoLib().removeTVS(self.TVS.lib_path) 
            self.linkTable.exclude(self.TVS.lib_path)
            
            self.setFile()
            self.setTVS(self.path, self.isFound)
            
            self.pageNum = 0
            if not noClean : self.libClean()
            #self.libUpdate()
            self.useChanger = True  
        
        return rd 
                   
                   
    def mnu_restoreall(self):
        
        rd = TAG_MNU_TVSMAN
        
        if not confirm(TAG_MNU_RESTOREALL) : return rd
        
        prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty
        if not errord(restoreAllTVS(prefix), TAG_ERR_OK_RESTOREALL):
            self.libClean()
            self.libUpdate()
            self.useChanger = True
        
        return rd
    
               
    def mnu_restore(self):   
    
        rd = TAG_MNU_TVSMAN
                 
        tvsNames, tvsPaths = getAllTVS()
        newPath = subMenue(tvsNames, tvsPaths, cancelVal=Empty, default=DOS.unsl(self.TVS.lib_path), title=titName(TAG_MNU_RESTORE))
        
        if not newPath : return rd
         
        if not confirm(TAG_MNU_RESTORE, normTargetName(newPath)) : return rd
        
        self.setTVS(newPath, True)
        prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty 
        if not errord(restoreTVS(self.TVS, prefix), TAG_ERR_OK_RESTOR, normName(self.TVS.lib_name)):
            #if not VideoLib().removeTVS(self.TVS.lib_path) : self.libClean()
            if not VideoLib().eviscerateTVS(self.TVS.lib_path) : self.libClean() 
            self.libUpdate(path=self.TVS.lib_path)
            self.useChanger = True
            return TAG_MNU_RESTORE  
        
        return rd 
                
                
    def mnu_rescanfull(self):
    
        rd = TAG_MNU_SRCMAN
        
        if not confirm(TAG_MNU_RESCANFULL) : return rd
        
        tvsNames, tvsPaths = getAllTVS()
        
        if not tvsNames : return rd
        
        self.reErrors = []
        
        progress = CProgress(len(tvsNames), bg=addon.BGUPD)
        progress.show(tla(TAG_MNU_RESCANFULL))
        
        currentPath = self.TVS.lib_path
        for path in tvsPaths:
            self.setTVS(path, True)
            progress.step(normName(self.TVS.lib_name), 1)
            self.mnu_rescanalls(full=True)    
         
        self.setTVS(currentPath, True)
        self.setLI()
        self.libClean()
        self.libUpdate(path=LIB.tvsf)
        self.useChanger = True
        
        for error in self.reErrors:
            errord(error[0], Empty, error[1], exten=error[2])
            
        self.reErrors = []
        
        errord(TAG_ERR_OK, TAG_ERR_OK_RESCANFULL)
        
        return rd
    
    
    def mnu_rescanalls(self, full=False):
        
        rd = TAG_MNU_SRCMAN
        
        srccl = self.src.clone(nofrc=True)
        
        if not full : 
            self.reErrors = []
            
            if srccl.srccount() == 1:
                _resItm  = Empty
                _defList = [0]
            else:
                _resItm  = tl(TAG_MNU_REMARKALL)
                _defList = None 
        
            mdefault=srccl.getlinkidx(self.items.vidCPath)
            snames = [itm for itm in srccl.remnames]
            srccl(subMenue(snames, srccl.idxs, cancelVal=-1, cancelName=TAG_MNU_OK, multiSel=True, default=mdefault, selMarkm=tl(TAG_MNU_SMM),
                title=titName(TAG_MNU_RESCANALLS, self.TVS.lib_name), resetItm=_resItm, multiSelDefList=_defList))
            srccl.filtering()
            
            if srccl.srccount() < 1 : return rd
            if not confirm(TAG_MNU_RESCANALLS, normName(self.TVS.lib_name)) : return rd
        
        self.TVS.os_getraw()
        
        while srccl.nextsidx():
            
            self.setLI(srccl.link, srccl.name)
            src_name = srccl.name
            srccl.exclude(srccl.link)
            if srccl.link in self.TVS.get_raw_link_list():
                seasons = self.TVS.get_multiseason_list(srccl.link)
                if len(seasons) > 1: 
                    seasonsv = [itm for itm in seasons]
                    seasonsn = [tl(TAG_TTL_NM) % (itm) for itm in seasons]
                    season = subMenue(seasonsn, seasonsv, cancelVal=-1, cancelName=TAG_MNU_DEFNM, title=tla(TAG_MNU_SRE))
                else : season = Empty
                err = self.mnu_rawadd(rescan=True, season=season)
            else:
                prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty
                err = rescanSRC(self.items, self.TVS, prefix)
            
            if err != TAG_ERR_OK : self.reErrors.append([err, normName(self.TVS.lib_name), src_name])
        
        if not full:
            self.setLI()
            if not VideoLib().eviscerateTVS(self.TVS.lib_path) : self.libClean()
            self.libUpdate(path=LIB.tvsf)
            self.useChanger = True
        
            for error in self.reErrors:
                errord(error[0], Empty, error[1], exten=error[2])
                
            self.reErrors = []
            
            errord(TAG_ERR_OK, TAG_ERR_OK_RESCANALLS, normName(self.TVS.lib_name))
        
        return rd
    
    
    def mnu_rescan(self):
    
        rd = TAG_MNU_SRCMAN
                                                                  
        if not confirm(TAG_MNU_RESCAN, normName(self.TVS.lib_name), self.src.getlinkname(self.items.vidCPath)) : return rd
        
        self.TVS.os_getraw()
        if self.items.vidCPath in self.TVS.get_raw_link_list(): 
            seasons = self.TVS.get_multiseason_list(self.items.vidCPath)
            if len(seasons) > 1: 
                seasonsv = [itm for itm in seasons]
                seasonsn = [tl(TAG_TTL_NM) % (itm) for itm in seasons]
                season = subMenue(seasonsn, seasonsv, cancelVal=Empty, cancelName=TAG_MNU_DEFNM, title=tla(TAG_MNU_SRE))
            else : season = Empty
            err = self.mnu_rawadd(rescan=True, season=season)
        else: 
            prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty
            err = rescanSRC(self.items, self.TVS, prefix)
            
        if not errord(err, TAG_ERR_OK_RESCAN, normName(self.TVS.lib_name)):
            #if not VideoLib().removeTVS(self.TVS.lib_path) : self.libClean()
            if not VideoLib().eviscerateTVS(self.TVS.lib_path) : self.libClean()
            self.libUpdate(path=LIB.tvsf)
            self.useChanger = True
            return TAG_MNU_CANCEL
            
        return rd
                
                
    def mnu_rawadd(self, update=False, rescan=False, season=Empty):
        
        rd = TAG_MNU_CANCEL
        
        ares = Empty
        
        if not update and not rescan : resType = subMenue([TAG_MNU_MOV, TAG_MNU_TVS])
        else : resType = TAG_MNU_TVS
        
        if resType == TAG_MNU_MOV:
        
            self.mnu_mov(rawadd=True)
            
        elif resType == TAG_MNU_TVS:
            
            eplist = [itm[0] for itm in self.items.vidListItemsRaw]
            idxs   = range(len(eplist))
            
            if update or rescan:
                newraw  = []
                newrawr = []
                tvsraw  = self.TVS.get_raw_eps() 
                for idx, itm in enumerate(eplist):
                    if itm not in tvsraw : newraw.append(idx)
                    else : newrawr.append(idx)
                
                idxsDef = newraw if not rescan else newrawr 
                rTTL    = TAG_PAR_TTLQ % (tla(TAG_TTL_RAWADDEPS), normName(self.TVS.lib_name))
                
            else : idxsDef = idxs; rTTL = tla(TAG_TTL_RAWADDEPS)
               
            selitems = subMenue(eplist, idxs, cancelVal=-1, cancelName=TAG_MNU_OK, multiSel=True, title=rTTL,
                                selMarkm=tl(TAG_MNU_SMM), multiSelDefList=idxsDef, resetItm=tl(TAG_MNU_REMARKALL))
            
            if not selitems : return TAG_MNU_BACKMAIN
            
            self.items.setmanually(selitems)
            
            if rescan:
                #GUI.dlgOk('Rescan')
                # mode = self.TVS.get_scr_numb_season_mode(self.items.vidCPath)[2]
                # if mode : items.convertToFolderMode() 
                # self.TVS.os_exclude_src(self.items.vidCPath)
                # update = True
                cornum = self.getCornum()
                prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty                
                ares = rescanSRC(self.items, self.TVS, prefix, season, cornum)
            else:  
                if update : ares = self.mnu_tvsu(False)
                else      : ares = self.mnu_tvs(raw=True)
            
            if ares == TAG_MNU_CANCEL:
                rawlist = [itm[0] for itm in self.items.vidListItemsRaw]
                self.TVS.os_addraw(self.items.vidCPath, rawlist)
                self.libUpdate(path=self.TVS.lib_path)
                self.useChanger = True
            else : return ares
        
        return rd
    
        
    def mnu_mov(self, rawadd=False):
        
        rd = TAG_MNU_BACKMAIN
        
        resType = subMenue([TAG_MNU_DEFNMMOV, TAG_MNU_NEWNMMOV], title=self.items.vidCurr)
        
        newName = Empty
        if   resType == TAG_MNU_BACKMAIN : return rd
        elif resType == TAG_MNU_NEWNMMOV : newName = GUI.dlgIn(tl(TAG_TTL_ENTNAMEM)) 
        
        prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_MOV, TAG_PAR_REPFN) if addon.CALLURL else Empty
        if not errord(addMOV(self.items, newName, prefix, rawadd), TAG_ERR_OK_MOVADD):
            self.libUpdate(path=LIB.mov)
            self.useChanger = True
            return TAG_MNU_CANCEL
            
        return rd
               
        
    def mnu_tvs(self, raw=False):
    
        rd = TAG_MNU_BACKMAIN
                                                                  
        #if not self.isFound : resType = subMenue([TAG_MNU_ADDNEW, TAG_MNU_ADDEXIST, TAG_MNU_ADVADD], title=normName(self.TVS.lib_defname) if self.TVS.lib_defname else titName(TAG_TTL_ADDTVS))
        #else                : resType = TAG_MNU_ADDNEW
        
        if not self.isFound : _tags = [TAG_MNU_ADDNEW, TAG_MNU_ADDEXIST, TAG_MNU_ADVADD]
        else                : _tags = [TAG_DLG_CURRTVS, TAG_MNU_ADVADD]
        resType = subMenue(_tags, title=normName(self.TVS.lib_defname) if self.TVS.lib_defname else titName(TAG_TTL_ADDTVS))
        
        if   resType == TAG_MNU_BACKMAIN : return rd
        elif resType == TAG_DLG_CURRTVS  : resType = TAG_MNU_ADDNEW
        elif resType == TAG_MNU_ADVADD   : return self.mnu_advadd(raw) 
        elif resType == TAG_MNU_ADDEXIST :
        
                tvsNames, tvsPaths = getAllTVS()
                newPath = subMenue(tvsNames, tvsPaths, cancelVal=Empty, default=DOS.unsl(self.TVS.lib_path), title=titName(TAG_TTL_CHSNAME))
                
                if not newPath : return rd
                
                self.setTVS(newPath, True)
                
                if DOS.exists(DOS.join(newPath, TAG_PAR_TVSRAWFILE)):
                    self.TVS.os_getraw() 
                    return self.mnu_advadd(raw)         
                
        prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty        
        errn = addTVS(self.items, self.TVS, prefix)             
        if not errord(errn, TAG_ERR_OK_TVSADD, normName(self.TVS.lib_name)):
            self.linkTable.add(self.TVS.lib_path, self.items.vidCPath)
            self.libUpdate(path=LIB.tvsf)
            #self.libUpdate(path=self.TVS.lib_path)
            self.useChanger = True
            return TAG_MNU_CANCEL
        
        elif errn == TAG_ERR_NONAME : return self.mnu_advadd(raw)
        
        return rd 
    
    
    def mnu_tvsstaln(self):
        
        rd = TAG_MNU_CANCEL
        
        self.mnu_advadd()
        
        return rd
    
    
    def getCornum(self, cornum=[]):
        eplist  = [itm[0] for itm in self.items.vidListItems]
        if not cornum : cornum = range(1, len(eplist)+1)    
        
        numList = []
        while True: 
          
            numList = []
            cidx    = 0
            for itm in eplist:
                while True:
                    cidx += 1
                    if cidx in cornum    : break
                    if cidx > max(cornum): cornum.append(cidx); break  
                    
                    numList.append(str(cidx)+Space+Space+tl(TAG_DLG_NUMSKIP))
                    
                numList.append(str(cidx)+Colon+Space+Space+itm)
            
            idxs    = range(1, len(numList)+1)
            idxsDef = [itm for itm in range(len(numList)) if itm+1 in cornum]
            
            selitem = subMenue(numList, idxs, cancelVal=-1, cancelName=TAG_MNU_OK, title=tla(TAG_MNU_NUMBCORR))
            if selitem == -1 : break
            if selitem: 
                if selitem in cornum: 
                    cornum.remove(selitem)
                    cornum.append(len(numList))
                else: 
                    numList.pop(selitem-1)
                    cornum.append(selitem) 
            
        return cornum
    
    
    def mnu_advadd(self, raw=False):
        
        rd = TAG_MNU_BACKMAIN
        
        newtvs  = tl(TAG_MNU_NEW) 
        
        defEpsList = [itm[0] for itm in self.items.vidListItems]  
        
        def _getParam():
        
            defname = self.TVS.lib_name if self.TVS.lib_name else createName(self.items.vidFolderNameDef)
            
            aSeason, aNumb, mode = self.TVS.get_scr_numb_season_mode(self.items.vidCPath)
            
            aSeq    = self.TVS.seq 
            aSeqT   = TAG_MNU_SEANUM if not aSeq    else TAG_MNU_SEQNUM
            aNumbT  = TAG_MNU_SERDEF if not aSeason else TAG_MNU_SERTPL
            aTVS    = normName(self.TVS.lib_name) if self.TVS.lib_name else newtvs
            aName   = defname
            
            return defname, aSeq, aSeqT, aNumb, aNumbT, aSeason, aTVS, aName, mode
        
        defname, aSeq, aSeqT, aNumb, aNumbT, aSeason, aTVS, aName, mode = _getParam()    
        
        result  = 0
        newPath = TAG_MNU_NEW if aTVS == newtvs else Empty
        aSortOd = TAG_MNU_ADVLSORTDOWN
        diflist = []
        cornum  = []
        skip    = 0
        oldSeason = aSeason
        
        aMode = tl(TAG_MNU_YES) if mode else tl(TAG_MNU_NO)
        
        while int(result) != -1:
        
            if not aSeason : aSeason = TAG_PAR_TVSDEFSEASON   
            aName2 = tl(TAG_MNU_DEFNM) if aName == defname else aName 
            
            mList  = []; mVals = []
            mList += [tl(TAG_MNU_ATVS) + aTVS]                   ; mVals += [0]
            
            if aTVS == newtvs :
                mList += [tl(TAG_MNU_ATVSNUMT) + tl(aSeqT)]      ; mVals += [1] 
                mList += [tl(TAG_MNU_ATVSNM)   + aName2]         ; mVals += [2]
            
            if aSeqT == TAG_MNU_SEANUM:   
                mList += [tl(TAG_MNU_ATVSSERT) + tl(aNumbT)]     ; mVals += [3]
            
            if aSeqT == TAG_MNU_SEANUM and aNumbT == TAG_MNU_SERTPL:
                mList += [tl(TAG_MNU_SEASON)   + aSeason]        ; mVals += [4]
            
            if aNumbT == TAG_MNU_SERTPL or aSeqT == TAG_MNU_SEQNUM:    
                mList += [tl(TAG_MNU_ADVLSORT) + tl(aSortOd)]    ; mVals += [5]
            
            mList += [tl(TAG_MNU_FOLDMODE) + aMode]              ; mVals += [6]    
            
            if aNumbT == TAG_MNU_SERTPL or aSeqT == TAG_MNU_SEQNUM:
                mList += [tl(TAG_MNU_NUMBCORR)]                  ; mVals += [7]
            
            mList += [tl(TAG_MNU_EPSLISTCORR)]                   ; mVals += [8]
            
            mList += [tl(TAG_MNU_STARTADD)]                      ; mVals += [9]
        
            if not skip : result = subMenue(mList, mVals, cancelVal=-1, title=tl(TAG_TTL_ADVADD))
            else        : result = skip; skip = 0
        
            if   result == 0:
                tvsNames, tvsPaths = getAllTVS()
                tvsNames.insert(0, tl(TAG_MNU_NEW))
                tvsPaths.insert(0, TAG_MNU_NEW)
                newPath = subMenue(tvsNames, tvsPaths, cancelVal=Empty, default=DOS.unsl(self.TVS.lib_path), title=titName(TAG_TTL_CHSNAME), defidx=0)
                if newPath:
                    if newPath == TAG_MNU_NEW : self.setTVS(Empty, False)
                    else                      : self.setTVS(newPath, True)            
                    defname, aSeq, aSeqT, aNumb, aNumbT, aSeason, aTVS, aName, mode = _getParam()
                    oldSeason = aSeason
                
                
            elif result == 1: 
                aSeqT   = TAG_MNU_SEANUM if aSeqT  == TAG_MNU_SEQNUM else TAG_MNU_SEQNUM
                if cornum and (aNumbT == TAG_MNU_SERTPL or aSeqT == TAG_MNU_SEQNUM) : skip = 7
                
            elif result == 2: 
                while True  : 
                    aName = createName(GUI.dlgIn(tl(TAG_DLG_INNM), aName)) 
                    if aName : break
            
            elif result == 3: 
                aNumbT  = TAG_MNU_SERDEF if aNumbT == TAG_MNU_SERTPL else TAG_MNU_SERTPL
                if cornum and (aNumbT == TAG_MNU_SERTPL or aSeqT == TAG_MNU_SEQNUM) : skip = 7
            
            elif result == 4: 
                while True  : 
                    aSeason = GUI.dlgInnum(tl(TAG_DLG_INSE), aSeason) 
                    if aSeason : break
            
            elif result == 5: 
                aSortOd = TAG_MNU_ADVLSORTUP if aSortOd == TAG_MNU_ADVLSORTDOWN else TAG_MNU_ADVLSORTDOWN
                self.items.reverse()
            
            elif result == 6:
                if not mode: 
                    aMode = tl(TAG_MNU_YES)
                    mode  = True
                else: 
                    aMode = tl(TAG_MNU_NO)
                    mode  = False 
                
            elif result == 7:
                cornum = self.getCornum(cornum)
                # eplist  = [itm[0] for itm in self.items.vidListItems]
                # if not cornum : cornum = range(1, len(eplist)+1)    
                # 
                # numList = []
                # while True: 
                #   
                #     numList = []
                #     cidx    = 0
                #     for itm in eplist:
                #         while True:
                #             cidx += 1
                #             if cidx in cornum    : break
                #             if cidx > max(cornum): cornum.append(cidx); break  
                #             
                #             numList.append(str(cidx)+Space+Space+tl(TAG_DLG_NUMSKIP))
                #             
                #         numList.append(str(cidx)+Colon+Space+Space+itm)
                #     
                #     idxs    = range(1, len(numList)+1)
                #     idxsDef = [itm for itm in range(len(numList)) if itm+1 in cornum]
                #     
                #     selitem = subMenue(numList, idxs, cancelVal=-1, cancelName=TAG_MNU_OK, title=tla(TAG_MNU_NUMBCORR))
                #     if selitem == -1 : break
                #     if selitem: 
                #         if selitem in cornum: 
                #             cornum.remove(selitem)
                #             cornum.append(len(numList))
                #         else: 
                #             numList.pop(selitem-1)
                #             cornum.append(selitem) 
                                                
            elif result == 8:    
                eplist    = [itm[0] for itm in self.items.vidListItemsRaw]
                seleplist = [itm[0] for itm in self.items.vidListItems]
                idxs      = range(len(eplist))
                idxsDef   = [idx for idx, itm in enumerate(eplist) if itm in seleplist]
                
                selitems = subMenue(eplist, idxs, cancelVal=-1, cancelName=TAG_MNU_OK, multiSel=True, title=normName(self.TVS.lib_name),
                                    selMarkm=tl(TAG_MNU_SMM), multiSelDefList=idxsDef, resetItm=tl(TAG_MNU_REMARKALL))
                
                if selitems: 
                    self.items.setmanually(selitems)
                    if not raw:
                        selEps = [eplist[itm] for itm in selitems]
                        diflistA = [itm for itm in selEps if itm not in defEpsList]
                        diflistB = [itm for itm in defEpsList if itm not in selEps]
                        diflist  = diflistA + diflistB    
                    
                    # diflistA = [itm for itm in selitems if itm not in idxsDef]  
                    # diflistB = [itm for itm in idxsDef  if itm not in selitems]
                    # diflist  = diflistA + diflistB  
                
                if cornum and (aNumbT == TAG_MNU_SERTPL or aSeqT == TAG_MNU_SEQNUM) : skip = 7
                
            elif result == 9: 
                if aName2 == tl(TAG_MNU_DEFNM) and newPath == TAG_MNU_NEW and not confirm(TAG_MNU_DEFNM, aName) : continue
                
                if mode: 
                    self.items.convertToFolderMode()
                    url_prefix = getURLPrefix(self.items.vidCPath)
                    if url_prefix:
                        pTable = playersTable()
                        pTable.setPType(url_prefix, 3)
                        del pTable 
                
                if aSeqT  == TAG_MNU_SEQNUM :
                    if aSeq < 1 : aSeq = 1 
                    self.TVS.seq = aSeq
                if aNumbT == TAG_MNU_SERDEF : aSeason = Empty 
                
                if newPath == TAG_MNU_NEW   : 
                    self.TVS.lib_name = aName
                    self.TVS.lib_path = LIB.tvs(aName)
                
                if oldSeason != aSeason     :
                    aNumb = 0
                    
                prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty
                errn = addTVS(self.items, self.TVS, prefix, aSeason, aNumb, cornum, folmode=mode)
                
                if not errord(errn, TAG_ERR_OK_TVSADD, normName(self.TVS.lib_name)):
                    self.linkTable.add(self.TVS.lib_path, self.items.vidCPath)
                    
                    if diflist and not raw:
                        rawlist = [itm[0] for itm in self.items.vidListItemsRaw]
                        self.TVS.os_addraw(self.items.vidCPath, rawlist)
                    
                    if aTVS != newtvs:
                        self.libUpdate(path=self.TVS.lib_path)
                    else:
                        self.libUpdate(path=LIB.tvsf)
                    self.useChanger = True
                    
                    return TAG_MNU_CANCEL
                    
        return rd
                
        
    def mnu_tvsu(self, isupd=True):
    
        rd = TAG_MNU_BACKMAIN
        
        prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty
        
        season, numb, mode = self.TVS.get_scr_numb_season_mode(self.items.vidCPath)         
        if mode : self.items.convertToFolderMode()
                                              
        if not errord(addTVS(self.items, self.TVS, prefix, season, numb, folmode=mode), TAG_ERR_OK_TVSUPD, normName(self.TVS.lib_name)):
               self.linkTable.add(self.TVS.lib_path, self.items.vidCPath)
               if isupd : self.libUpdate(path=LIB.tvsf); self.useChanger = True
               return TAG_MNU_CANCEL
        
        return rd    
                
        
    def mnu_open(self):                                                              
        
        rd = TAG_MNU_BACKMAIN
        
        subLink  = subMenue(self.src.remnames, self.src.links, cancelVal=Empty, title=titName(TAG_MNU_OPEN, self.TVS.lib_name))
         
        if not subLink : return rd
         
        oldCont = self.items.vidCPath 
        GUI.goTarget(subLink)
        if oldCont != subLink and not isWait(oldCont, LI.getCpath, addon.LNKTIMEOUT) : errord(TAG_ERR_DEDLINK); return rd
        
        return TAG_MNU_CANCEL  
    
    
    def mnu_pbtypes(self):
        
        rd = TAG_MNU_BACKMAIN
        
        pTable = playersTable()
        plugs, types = pTable.getall()
        idxs = range(len(plugs))
        
        plugsNemes = [prefixToName(plg) for plg in plugs]
        
        plugin = subMenue(plugsNemes, idxs, cancelVal=-1, title=tla(TAG_MNU_PBTYPES))
        
        if plugin != -1:
            rd = TAG_MNU_PBTYPES
            PBTYPES_LIST_L = PBTYPES_LIST + [tl(TAG_DLG_PBTREM)]
            lastel = len(PBTYPES_LIST_L)
            idxs = range(1, lastel+1)

            ptype = subMenue(PBTYPES_LIST_L, idxs, cancelVal=-1, default=int(types[plugin]), title=titName(TAG_DLG_PBT2, prefixToName(plugs[plugin])))
            
            if ptype != -1: 
                if ptype == lastel : pTable.removePType(plugs[plugin])
                else : pTable.setPType(plugs[plugin], ptype)
                      
        del pTable
        return rd   
    
    
    def mnu_delmov(self):
    
        rd = TAG_MNU_CANCEL
        
        title = self.items.vidCurr
        
        if GUI.dlgYn(tl(TAG_DLG_MOVIEDEL), title=title): 
            VideoLib().removeMovie(self.path)
            DOS.delf(self.path)
            GUI.msg(tl(TAG_ERR_OK_MTVSDEL) % title)
            self.useChanger = True
        
        return rd
    
    
    def mnu_deltvs(self):
        rd = TAG_MNU_CANCEL
        
        title = self.items.vidCurr
        path  = self.TVS.lib_path
        
        if GUI.dlgYn(tl(TAG_DLG_TVSDEL), title=title): 
            VideoLib().removeTVS(self.TVS.lib_path)
            deleteTVS(self.TVS)
            self.linkTable.exclude(path)
            GUI.msg(tl(TAG_ERR_OK_MTVSDEL) % title)
            self.useChanger = True
                
        return rd
    
    
    def mnu_dbsync(self):
    
        rd = TAG_MNU_CANCEL
    
        upload   = False
        download = False
        forsend  = False  
        
        resultM = subMenue([TAG_TTL_SVIDDB, TAG_TTL_SWS, TAG_TTL_SYNCUNLOCK, TAG_TTL_LOCKSY], title=tla(TAG_MNU_DBSYNC))
        
        mnuList = [TAG_TTL_SYNCAUTO, TAG_TTL_SYNCSENDCH, TAG_TTL_SYNCUP, TAG_TTL_SYNCDOWN]
        
        if   resultM == TAG_TTL_SVIDDB     : pass
        elif resultM == TAG_TTL_SWS        : pass
        elif resultM == TAG_TTL_LOCKSY     : 
            if GUI.dlgYn(tl(TAG_DLG_LOCKSYQ)):
                lsync = self.dbx.justLock()
                if   lsync == -1 : errord(TAG_ERR_NODBXCONNECT)
                elif lsync == -2 : errord(TAG_ERR_DBXISLOCK)
                else : errord(TAG_ERR_OK, TAG_ERR_OK_SYNCLOCK)  
                return TAG_MNU_BACKMAIN
                
        elif resultM == TAG_TTL_SYNCUNLOCK : 
            corrReset = -1
            corrID = self.dbx.getCorrupted()
            if corrID == -1 : errord(TAG_ERR_NODBXCONNECT); return TAG_MNU_BACKMAIN
            if corrID:
                adnID = self.dbx.getAddonUID()
                if adnID == corrID:
                    GUI.dlgOk(tl(TAG_DLG_CORR1))
                    corrReset = GUI.dlgYn(tl(TAG_DLG_CORR_FORCE))
                    if corrReset:
                        result  = TAG_TTL_SYNCUP
                        resultM = TAG_TTL_SVIDDB
                        forsend = True
                    
                    else : corrReset = GUI.dlgYn(tl(TAG_DLG_CORR_UNL)) 
                        
                else:
                    GUI.dlgOk(tl(TAG_DLG_CORR2))
                    corrReset = GUI.dlgYn(tl(TAG_DLG_CORR3))
                
            if corrReset and self.dbx.unLock(resetCorr=True) : errord(TAG_ERR_OK, TAG_ERR_OK_SYNCUNLOCK) 
            if not forsend : return TAG_MNU_BACKMAIN
            else : self.dbx.progress_show_always = True
            
        else : return TAG_MNU_BACKMAIN
        
        if not forsend : result = subMenue(mnuList, title=titName(TAG_MNU_DBSYNC, tla(resultM)))
        
        if   result == TAG_TTL_SYNCAUTO   : upload = False; download = False
        elif result == TAG_TTL_SYNCSENDCH : 
            upload = False; download = False
            if resultM == TAG_TTL_SVIDDB  : self.dbx.createSyncFile()
            else                          : self.dbx.createWatchedInfo(standalone_progress=True)
              
        elif result == TAG_TTL_SYNCUP     : upload = True;  download = False
        elif result == TAG_TTL_SYNCDOWN   : upload = False; download = True
        else : return TAG_MNU_DBSYNC 
        
        if resultM == TAG_TTL_SVIDDB : self.act_sync(upload=upload, download=download, allreports=True); emgrControl().setLAACTT(TAG_ACT_SYNC)
        else                         : self.act_watchsync(upload=upload, download=download, allreports=True); emgrControl().setLAACTT(TAG_ACT_WATCHSYNC) 
        
        return rd    
             
        
    def mnu_help(self): 
        help.showHelp()
        return TAG_MNU_BACKMAIN           
        
        
    def mnu_set(self):
        GUI.openSet()
        #check_lib_folders()
        return TAG_MNU_CANCEL 
                   
    
    def mnu_vidlibu(self):                                                                            
        self.libUpdate(True, True)
        return TAG_MNU_CANCEL 
        
        
    def mnu_vidlibcln(self):                                                              
        self.libClean (True)
        #self.libUpdate(False, True)
        return TAG_MNU_CANCEL
        
        
    def act_DBXConnect(self):
        if self.dbx.authorize(GUI.dlgDropbox):
            addon.addon.setSetting('acsstkn', 'true')
        return TAG_MNU_CANCEL
        
        
    def act_DBXDisconnect(self):
        self.dbx.disable()
        addon.addon.setSetting('acsstkn', 'false')
        GUI.dlgDropbox(3)
        return TAG_MNU_CANCEL
    
    
    def act_watchsync(self, upload=False, download=False, allreports=False, hide=False):
    
        if not hide : self.dbx.progress_show_always = True
    
        syncMode = self.dbx.watchSync(upload=upload, download=download)
    
        errorn = TAG_ERR_OK
        rd     = TAG_MNU_CANCEL
        repmsg = Empty
    
        if   syncMode == 0 and allreports: 
            repmsg = TAG_ERR_OK_DBXWSMAC
            
        elif syncMode == 11 or (syncMode == 1 and allreports):
            repmsg = TAG_ERR_OK_DBXWSMUP
            
        elif syncMode in [2, 22]:
            repmsg = TAG_ERR_OK_DBXWSMDL
            #rd     = TAG_MNU_VIDLIBU
                    
        elif syncMode == -1:
            errorn = TAG_ERR_NODBXCONNECT
        elif syncMode == -2 and allreports:
            errorn = TAG_ERR_DBXISLOCK
            
        if repmsg or errorn != TAG_ERR_OK : errord(errorn, repmsg)
        self.syncAlred = True
        return rd
    
        
    def act_sync(self, upload=False, download=False, allreports=False, hide=False):
         
        if not hide : self.dbx.progress_show_always = True
         
        if self.useChanger : self.lockalChangesNow()
     
        #GUI.msg('SYNC')
        
        syncMode = self.dbx.sync(upload=upload, download=download)
        
        errorn = TAG_ERR_OK
        rd     = TAG_MNU_CANCEL
        repmsg = Empty
        
        if   syncMode == 0 and allreports:
            repmsg = TAG_ERR_OK_DBXSMAC
            
        elif syncMode == 11 or (syncMode == 1 and allreports):
            repmsg = TAG_ERR_OK_DBXSMUP
            
        elif syncMode in [2, 22]:
            repmsg = TAG_ERR_OK_DBXSMDL    
                
        elif syncMode == -1:
            errorn = TAG_ERR_NODBXCONNECT
        elif syncMode == -2 and allreports:
            errorn = TAG_ERR_DBXISLOCK
        
        if self.dbx.last_removed:
            if syncMode == 2: 
                #GUI.msg(tl(TAG_DLG_SCLNDB))
                VideoLib().cleanList(self.dbx.last_removed, allreports)
                #GUI.msg(tl(TAG_DLG_SREMEF))
                VideoLib().osCleanTVS(allreports)
            if syncMode == 22:
                self.libClean()
        
        if syncMode in [2, 22] and (self.dbx.last_removed or self.dbx.last_added) : self.libUpdate()  
        if repmsg or errorn != TAG_ERR_OK : errord(errorn, repmsg)
        self.syncAlred = True
         
        return rd
    
    
    def act_lpreset(self):
        addon.addon.setSetting('libpath', TAG_PAR_SETDEF)
        return TAG_MNU_CANCEL
        
    
    def act_chcolor(self):
        pckdcolors = DOS.file(TAG_PAR_COLORS_FILE, DOS.join(addon.path, TAG_PAR_RESFOLDER, TAG_PAR_BSFOLDER), fType=FRead)
        colors     = [color.replace(CR, Empty) for color in pckdcolors.split(NewLine)]
        colnames   = [TAG_PAR_MNUCOLORFORMAT % (color, color) for color in colors]
        defcolor   = addon.getcolor() 

        newcolor = subMenue(colnames, colors, cancelVal=Empty, default=defcolor, title=tl(TAG_TTL_COLORIZE))
        
        if newcolor : 
            addon.addon.setSetting('mnucolor', newcolor)
            addon.addon.setSetting('actcolor', newcolor)
        
        path       = DOS.join(addon.path, *TAG_PAR_STRINGSXML_PATH)
        stringsxml = DOS.file(TAG_PAR_STRINGSXML_FILE, path, fType=FRead)
        label      = CMP.comps(stringsxml)
        label.sub(TAG_PAR_ADDONLABEL_PATT, rep_text=TAG_PAR_ADDONLABEL % addon.getcolor())
        DOS.file(TAG_PAR_STRINGSXML_FILE, path, label(), fType=FWrite, fRew=True)
        
        return TAG_MNU_CANCEL
        
    
    def act_reskin(self):
        
        skins      = DOS.listdir(DOS.join(addon.path, *TAG_PAR_SKINSFOLDER))[0]
        skinsnames = [itm for itm in skins] 
        defskin    = addon.SKIN 

        skin = subMenue(skinsnames, skins, cancelVal=Empty, default=defskin, title=tl(TAG_TTL_RESKIN))
        
        if skin : 
            addon.addon.setSetting('skin', skin)
            addon.addon.setSetting('actskin', skin)
        
        return TAG_MNU_CANCEL
    
    
    def act_renamer(self):
        rd = TAG_MNU_CANCEL
        if not confirm(TAG_ACT_RENAMER) : return rd
        srcRenamer()
        errord(TAG_ERR_OK, TAG_ERR_OK_RENAMER)
        return rd
        
        
    def act_resettbu(self):
        addon.addon.setSetting('bkuppath', TAG_PAR_SETDEF)
        return TAG_MNU_CANCEL
        
    
    def act_autobackup(self):    
        return self.act_backup(True)
        
    
    def act_backup(self, auto=False):
        rd = TAG_MNU_CANCEL
        
        #self.updlock(lock=True)
        
        errord(backup(auto), TAG_ERR_OK_BACKUP)
        
        if not auto : emgrControl().setLAACTT(TAG_ACT_AUTOBACKUP)
        
        return rd
    
    
    def act_remback(self):
        rd = TAG_MNU_CANCEL
        
        if not confirm(TAG_ACT_REMBACK) : return rd
        errord(remove_all_backups(), TAG_ERR_OK_REMBACK)
        
        return rd
    
    
    def act_restback(self):
        rd = TAG_MNU_CANCEL
        
        #self.updlock(lock=True)
        
        backups = get_all_sort_backups()
        if backups == -1:
            errord(TAG_ERR_NOBCKPATH, Empty) 
            return rd
            
        if not backups:
            errord(TAG_ERR_OK, TAG_ERR_OK_NOBACK) 
            return rd
        
        bcknames = []
        for name in backups:
            pn = parse_backupname(name)
            bcknames.append(tl(TAG_TTL_BCKNM) % (pn[2], pn[1], pn[0], pn[3], pn[4], pn[5], pn[6]))
        
        bckname = subMenue(bcknames, backups, cancelVal=Empty, default=backups[0], title=tl(TAG_TTL_RESTBACK))
         
        if not bckname or not confirm(TAG_ACT_RESTBACK, srcName=bckname) : return rd
        
        if not errord(restore_lib(bckname), TAG_ERR_OK_RESTBACK):
            self.libClean()
            self.libUpdate()
            
        return rd
    
    
    def act_stopsrv(self):
        DOS.file('stopsrv', addon.profile, Empty)
        return TAG_MNU_CANCEL
        
         
    def act_startsrv(self):
        import service 
        GUI.Thrd(service.service, True)   
        return TAG_MNU_CANCEL
        
    
    def act_donothing(self):
        return TAG_MNU_CANCEL


##### Start main ...
if __name__ == '__main__':  Main()