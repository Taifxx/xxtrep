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
import resources.lib.help as help

from resources.lib.common  import *
from resources.lib.menues  import *
from resources.lib.call    import *

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
    if parseArgs() : plgMain()
    

##### Main ...
class plgMain():        
    
    def _cleanObject(self, obj):
        try    : del obj 
        except : pass


    def setTVS(self, path, isFound):
        self._cleanObject(self.TVS)
        self.path    = path 
        self.isFound = isFound
        self.TVS = CTVS.TVS(TAG_PAR_TVSPACK_FILE, path, isFound)
    
    
    def setLI(self):
        self._cleanObject(self.items)
        self.items = LI.vidItems()
     
        
    def setLinkTable(self):
        self._cleanObject(self.linkTable)
        self.linkTable = CTVS.CLinkTable(TAG_PAR_STL_FILE, LIB.lib)
    
    
    def setSRC(self):
        self._cleanObject(self.src)
        self.src = CSRC(*self.TVS.get_names_and_links())
    
    
    def setFile(self):
        self.isFound, self.container, self.path = checkfile(self.items, self.linkTable)
    
    
    def libClean(self, always=False):
        if addon.UPDAFTER or always: 
            if GUI.dlgYn (tl(TAG_CFR_CLEANVL)) : GUI.libClean()
    
    
    def libUpdate(self, report=False, always=False):
        if addon.UPDAFTER or always: 
            GUI.libUpdate()
            if self.container in [TAG_CON_VID, TAG_CON_LOCAL]: GUI.refresh()
            if report : errord(TAG_ERR_OK, TAG_ERR_OK_VIDLIBU)
    
    
    def back(self):
        GUI.back()
     
        
    def doAction(self):
        ## Redefine values ... 
        self.setSRC() 
        self.isNewSource    = self.src.isnewsrc(self.items.vidCPath)
        self.isNewFolSource = self.src.isnewfrc(self.items.vidCPath)
    
        ## Delete existing menues ...
        try    : del self.MainMenue, self.tvsmMenue, self.srcmMenue, self.updtMenue 
        except : pass
         
        ## Define Visible conditions ...
        curVisCond         = {self.container, 
                              TAG_CND_NOTFOUND  if not self.isFound        else TAG_CND_FOUND,
                              TAG_CND_NEWSRC    if self.isNewSource        else TAG_CND_OLDSRC,
                              TAG_CND_NEWFRC    if self.isNewFolSource     else TAG_CND_OLDFRC,
                              TAG_TYP_FOLDER    if self.items.vidIsFolder  else TAG_TYP_FILE,
                              TAG_CND_LISTEMPTY if self.items.vidIsEmpty   else Empty,
                              TAG_CND_NOUPD     if not addon.ADDUPD        else Empty}
        
                              
        ## Define Main Menue ...
        self.MainMenue = tagMenue({'pos':0, 'tag':TAG_MNU_MOV,      'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_TYP_FOLDER}},
                                  {'pos':1, 'tag':TAG_MNU_TVS,      'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_LISTEMPTY, TAG_CND_OLDSRC}},
                                  {'pos':1, 'tag':TAG_MNU_TVSU,     'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_LISTEMPTY, TAG_CND_NEWSRC}},
                                  {'pos':2, 'tag':TAG_MNU_UPDFOL,   'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_NEWFRC}},
                                  {'pos':3, 'tag':TAG_MNU_CHKNEW,   'hideCond':{TAG_CND_NOTFOUND}},
                                  {'pos':4, 'tag':TAG_MNU_OPEN,     'hideCond':{TAG_CND_NOTFOUND}},
                                  {'pos':5, 'tag':TAG_MNU_CHKNEWGL, 'hideCond':{}},
                                  {'pos':6, 'tag':TAG_MNU_VIDLIBU,  'hideCond':{TAG_CND_NOUPD}},
                                  {'pos':7, 'tag':TAG_MNU_VIDLIBCLN,'hideCond':{TAG_CND_NOUPD}},
                                  {'pos':8, 'tag':TAG_MNU_SRCMAN,   'hideCond':{(TAG_CON_LOCAL, TAG_CND_NOTFOUND), (TAG_CON_VID, TAG_CND_NOTFOUND)}},
                                  #{'pos':8, 'tag':TAG_MNU_SRCMAN,   'hideCond':{}},
                                  {'pos':9, 'tag':TAG_MNU_UPDMAN,   'hideCond':{TAG_CND_NOTFOUND}},
                                  {'pos':10,'tag':TAG_MNU_TVSMAN,   'hideCond':{}},         
                                  {'pos':1, 'tag':TAG_MNU_HELP,     'hideCond':{}, 'refPage':addon.SETPAGE-1},
                                  {'pos':2, 'tag':TAG_MNU_SET,      'hideCond':{}, 'refPage':addon.SETPAGE-1},
                                  pageLimit = addon.MNUITMNUM,
                                  cancelTag = TAG_MNU_CANCEL, 
                                  backTag   = TAG_MNU_BACK, 
                                  nextTag   = TAG_MNU_MORE,
                                  visCond   = curVisCond,
                                  title     = normName(self.TVS.lib_name)) 
         
        ## Define Sub Menues ... 
        self.tvsmMenue = tagMenue({'pos':0, 'tag':TAG_MNU_SHOWALL,    'hideCond':{}},
                                  #{'pos':1, 'tag':TAG_MNU_ADVADD,     'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_LISTEMPTY}},  
                                  {'pos':2, 'tag':TAG_MNU_REBSTL,     'hideCond':{}},
                                  {'pos':3, 'tag':TAG_MNU_JOIN,       'hideCond':{}},
                                  {'pos':4, 'tag':TAG_MNU_TVSREN,     'hideCond':{}},
                                  {'pos':5, 'tag':TAG_MNU_DELETE,     'hideCond':{}},
                                  {'pos':6, 'tag':TAG_MNU_RESTORE,    'hideCond':{}},
                                  {'pos':7, 'tag':TAG_MNU_RESTOREALL, 'hideCond':{}},
                                  pageLimit = addon.MNUITMNUM,
                                  cancelTag = TAG_MNU_BACKMAIN, 
                                  backTag   = TAG_MNU_BACK, 
                                  nextTag   = TAG_MNU_MORE,
                                  visCond   = curVisCond,
                                  title     = titName(TAG_MNU_TVSMAN, self.TVS.lib_name))
        
        self.srcmMenue = tagMenue({'pos':0, 'tag':TAG_MNU_ADDFOL,   'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_OLDFRC}},
                                  #{'pos':0, 'tag':TAG_MNU_UPDFOL,   'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_NEWFRC}},
                                  {'pos':1, 'tag':TAG_MNU_ADVADD,   'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_LISTEMPTY}},   
                                  {'pos':2, 'tag':TAG_MNU_REMSRC,   'hideCond':{TAG_CND_NOTFOUND}},
                                  {'pos':3, 'tag':TAG_MNU_RESCAN,   'hideCond':{TAG_CON_LOCAL, TAG_CON_VID, TAG_CND_NOTFOUND, TAG_CND_NEWSRC}},
                                  {'pos':4, 'tag':TAG_MNU_SRCREN,   'hideCond':{TAG_CND_NOTFOUND}},
                                  pageLimit = addon.MNUITMNUM,
                                  cancelTag = TAG_MNU_BACKMAIN, 
                                  backTag   = TAG_MNU_BACK, 
                                  nextTag   = TAG_MNU_MORE,
                                  visCond   = curVisCond,
                                  title     = titName(TAG_MNU_SRCMAN, self.TVS.lib_name))
        
        self.updtMenue = tagMenue({'pos':0, 'tag':TAG_MNU_TVSU,     'hideCond':{}},
                                  {'pos':0, 'tag':TAG_MNU_SHDIR,    'hideCond':{}},  
                                  pageLimit = addon.MNUITMNUM,
                                  cancelTag = TAG_MNU_BACKMAIN, 
                                  backTag   = TAG_MNU_BACK, 
                                  nextTag   = TAG_MNU_MORE,
                                  visCond   = curVisCond,
                                  title     = titName(TAG_TTL_NEWEPS, self.TVS.lib_name))
    
        ## Show Main menue ...
        if self.result not in [TAG_MNU_TVS,     TAG_MNU_TVSU,   TAG_MNU_TVSMAN, TAG_MNU_SRCMAN, TAG_MNU_DELETE, 
                               TAG_MNU_RESTORE, TAG_MNU_TVSREN, TAG_MNU_REMSRC, TAG_MNU_SRCREN, TAG_MNU_CHKNEW]:
                                             
                                             self.pageNum,  self.result = self.MainMenue.show(self.pageNum)                  
        ## Show Sub menues ...   
        if   self.result == TAG_MNU_SRCMAN : self.srcmPage, self.result = self.srcmMenue.show(self.srcmPage)  
        elif self.result == TAG_MNU_TVSMAN : self.tvsmPage, self.result = self.tvsmMenue.show(self.tvsmPage) 
        
        ## Parse results ...
        if   self.result == TAG_MNU_CANCEL      : pass
        elif self.result == TAG_MNU_ADDFOL      : self.result = self.mnu_addfol()
        elif self.result == TAG_MNU_UPDFOL      : self.result = self.mnu_updfol()
        elif self.result == TAG_MNU_JOIN        : self.result = self.mnu_join()
        elif self.result == TAG_MNU_TVSREN      : self.result = self.mnu_tvsren()
        elif self.result == TAG_MNU_SRCREN      : self.result = self.mnu_scrren()
        elif self.result == TAG_MNU_REMSRC      : self.result = self.mnu_remsrc()
        elif self.result == TAG_MNU_UPDMAN      : self.result = self.mnu_updman()
        elif self.result == TAG_MNU_SHOWALL     : self.result = self.mnu_showall()
        elif self.result == TAG_MNU_CHKNEW      : self.result = self.mnu_chknew()
        elif self.result == TAG_MNU_CHKNEWGL    : self.result = self.mnu_chknewgl()
        elif self.result == TAG_MNU_DELETE      : self.result = self.mnu_delete()
        elif self.result == TAG_MNU_RESTORE     : self.result = self.mnu_restore()
        elif self.result == TAG_MNU_RESTOREALL  : self.result = self.mnu_restoreall()
        elif self.result == TAG_MNU_RESCAN      : self.result = self.mnu_rescan()
        elif self.result == TAG_MNU_REBSTL      : self.result = self.mnu_rebstl()
        elif self.result == TAG_MNU_MOV         : self.result = self.mnu_mov()
        elif self.result == TAG_MNU_TVS         : self.result = self.mnu_tvs()
        elif self.result == TAG_MNU_TVSU        : self.result = self.mnu_tvsu()
        elif self.result == TAG_MNU_ADVADD      : self.result = self.mnu_advadd()
        elif self.result == TAG_MNU_OPEN        : self.result = self.mnu_open()
        elif self.result == TAG_MNU_HELP        : self.result = self.mnu_help()
        elif self.result == TAG_MNU_SET         : self.result = self.mnu_set()
        elif self.result == TAG_MNU_VIDLIBU     : self.result = self.mnu_vidlibu()
        elif self.result == TAG_MNU_VIDLIBCLN   : self.result = self.mnu_vidlibcln()
    
    
    def __init__(self):
        ## Create Addon Profile folder ...
        DOS.mkdirs(addon.profile)
        
        CTVS.BGPROCESS = addon.BGUPD
    
        ## Define empty objects ...
        self.linkTable = None
        self.items     = None
        self.TVS       = None
        self.src       = None
    
        ## Set defaults ...
        self.setLI()
        self.setLinkTable()
        self.setFile()
        self.setTVS(self.path, self.isFound)
        
        self.result   = Empty
        self.pageNum  = 0
        self.tvsmPage = 0
        self.srcmPage = 0
        self.updtPage = 0
        
        ## Start main menue process ...
        while self.result != TAG_MNU_CANCEL : self.doAction()
        
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
                
        return rd
        
        
    def mnu_updfol(self):  
    
        rd = TAG_MNU_CANCEL
                                                                 
        errord(updFolSRC(self.items, self.TVS), TAG_ERR_OK_UPDFOL, normName(self.TVS.lib_name))
        
        return rd
    
    
    def mnu_rebstl(self):
        
        rd = TAG_MNU_TVSMAN
        
        errord(rebuildLinkTable(), TAG_ERR_OK_REBSTL)
        
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
            self.libUpdate()
                
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
           self.libClean()
           self.libUpdate() 
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
           self.libUpdate()
        
        return rd
         
        
    def mnu_updman(self):                  
    
        rd = TAG_MNU_BACKMAIN
                                                
        srcDef, frcDef = self.TVS.get_upd()
        mdefault=self.src.getlinkidx(self.items.vidCPath)
        mdefidx=self.src.frclen if mdefault >= self.src.frclen else 0
        self.src(subMenue(self.src.remnames, self.src.idxs, cancelVal=-1, cancelName=TAG_MNU_OK, multiSel=True, default=mdefault, selMarkm=tl(TAG_MNU_SM),
                     multiSelDefList=self.src.getidxs(frcDef+srcDef), defidx=mdefidx, title=titName(TAG_MNU_UPDMAN, self.TVS.lib_name)))
                        
        errord(setupdSRC(self.src.fnames, self.src.snames, self.TVS), TAG_ERR_OK_SETUPD, normName(self.TVS.lib_name))                                      
        
        return rd  
        
        
    def mnu_showall(self):
    
        rd = TAG_MNU_TVSMAN
                                                                  
        tvsNames, tvsPaths = getAllTVS()
        
        if not tvsNames : return rd
         
        newPath = subMenue(tvsNames, tvsPaths, cancelVal=Empty, default=DOS.unsl(self.TVS.lib_path), title=titName(TAG_TTL_EXITVS))
        
        if not newPath  : return rd
         
        self.setTVS(newPath, True)
        self.pageNum = 0
        
        return Empty 
        
        
    def mnu_chknew(self):                                         
    
        rd = TAG_MNU_CANCEL
        
        self.chkfull = False
        
        try    : self.usrc
        except : self.usrc = CSRC(*self.TVS.check_new_eps(titName(TAG_TTL_CHKUPD, self.TVS.lib_name)))
              
        if not self.usrc.idxs : errord(TAG_ERR_OK, TAG_ERR_OK_CHKNEW, normName(self.TVS.lib_name)); del self.usrc; return rd
        
        remnames = [itm for itm in self.usrc.remnames]
        idxs     = [itm for itm in self.usrc.idxs]
        
        mdefault=self.usrc.getlinkidx(self.items.vidCPath) 
        mdefidx=self.usrc.frclen if mdefault >= self.src.frclen else 0
        self.usrc(subMenue(remnames, idxs, cancelVal=-1, default=mdefault, 
                           defidx=mdefidx, title=titName(TAG_TTL_NEWEPS, self.TVS.lib_name)))
                        
        if not self.usrc.isidx : del self.usrc; return TAG_MNU_BACKMAIN
        
        oldCont = self.items.vidCPath
        GUI.goTarget(self.usrc.link)
        
        if oldCont != self.usrc.link and not isWait(oldCont, LI.getCpath, addon.LNKTIMEOUT) : errord(TAG_ERR_DEDLINK); return TAG_MNU_CHKNEW 
        
        self.setLI()
         
        if self.usrc.isf : return rd #self.mnu_updfol()
        else             : self.mnu_tvsu(False)
        
        self.back()
        self.setLI() 
        self.usrc.exclude(self.usrc.link)
        self.libUpdate()
    
        if self.usrc.idxs : return TAG_MNU_CHKNEW       
        
        del self.usrc
        
        self.chkfull = True
        
        return rd 
        
    
    def mnu_chknewgl(self):
    
        rd = TAG_MNU_CANCEL
    
        sList, fList = globalUpdateCheck()
        
        while True:
        
            if not sList and not fList : errord(TAG_ERR_OK, TAG_ERR_OK_CHKNEW); return rd
        
            tvsNames  = [tl(TAG_MNU_SRE) + normName(itm['name']) for itm in fList] + [normName(itm['name']) for itm in sList] 
            tvsVals   = range(len(tvsNames))
        
            result = subMenue(tvsNames, tvsVals, cancelVal=-1, title=titName(TAG_MNU_CHKNEWGL))
            
            if result == -1 : return TAG_MNU_BACKMAIN
            
            if result < len(fList) : idx = result;            self.setTVS(fList[idx]['path'], True); name = fList[idx]['name'] 
            else                   : idx = result-len(fList); self.setTVS(sList[idx]['path'], True); name = sList[idx]['name']
            
            flst = [[], []]
            for itm in fList:
                if itm['name'] == name : flst = [itm['ups'][0], itm['ups'][1]]; break
            
            slst = [[], []]
            for itm in sList:
                if itm['name'] == name : slst = [itm['ups'][0], itm['ups'][1]]; break
            
            lst = slst + flst 
            self.usrc = CSRC(*lst)
            del flst, slst, lst 
            
            while True:
            
                upres = self.mnu_chknew() 
                
                idxf = -1; idxs = -1 
                for i, itm in enumerate(fList):   
                    if itm['name'] == name : idxf = i; break
                for i, itm in enumerate(sList):   
                    if itm['name'] == name : idxs = i; break
                     
                try    : fList[idxf]['ups'] = self.usrc.getfrc()
                except : pass
                try    : sList[idxs]['ups'] = self.usrc.getsrc()   
                except : pass
                 
                if idxf > -1 and (not fList[idxf]['ups'][0] or self.chkfull) : fList.pop(idxf)
                if idxs > -1 and (not sList[idxs]['ups'][0] or self.chkfull) : sList.pop(idxs)
                
                if upres == TAG_MNU_BACKMAIN : break
                if upres == TAG_MNU_CANCEL   : break
                    
            del tvsNames, tvsVals
            if not sList and not fList : break
            
        return rd
                   
                   
    def mnu_delete(self):                                    
        
        rd = TAG_MNU_TVSMAN
                                                              
        tvsNames, tvsPaths = getAllTVS()
        newPath = subMenue(tvsNames, tvsPaths, cancelVal=Empty, default=DOS.unsl(self.TVS.lib_path), title=titName(TAG_MNU_DELETE))
        
        if not newPath : return rd
         
        if not confirm(TAG_MNU_DELETE, normTargetName(newPath)) : return rd
        
        self.setTVS(newPath, True)
        if not errord(deleteTVS(self.TVS), TAG_ERR_OK_DELETE, normName(self.TVS.lib_name)):
            self.linkTable.exclude(self.TVS.lib_path)
            
            self.setFile()
            self.setTVS(self.path, self.isFound)
            
            self.pageNum = 0
            self.libClean()
            self.libUpdate()  
        
        return rd 
                   
                   
    def mnu_restoreall(self):
        
        rd = TAG_MNU_TVSMAN
        
        if not confirm(TAG_MNU_RESTOREALL) : return rd
        
        prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty
        errord(restoreAllTVS(prefix), TAG_ERR_OK_RESTOREALL)
        
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
            self.libUpdate()
            return TAG_MNU_RESTORE  
        
        return rd 
                
        
    def mnu_rescan(self):
    
        rd = TAG_MNU_SRCMAN
                                                                  
        if not confirm(TAG_MNU_RESCAN, normName(self.TVS.lib_name), self.src.getlinkname(self.items.vidCPath)) : return rd 
        
        prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_PAR_REPFN, TAG_TYP_MOV) if addon.CALLURL else Empty
        if not errord(rescanSRC(self.items, self.TVS, prefix), TAG_ERR_OK_RESCAN, normName(self.TVS.lib_name)):
            self.libUpdate()
            return TAG_MNU_CANCEL
            
        return rd
                
        
    def mnu_mov(self):
        
        rd = TAG_MNU_BACKMAIN
        
        resType = subMenue([TAG_MNU_DEFNMMOV, TAG_MNU_NEWNMMOV], title=self.items.vidCurr)
        
        newName = Empty
        if   resType == TAG_MNU_BACKMAIN : return rd
        elif resType == TAG_MNU_NEWNMMOV : newName = GUI.dlgIn(tl(TAG_TTL_ENTNAMEM)) 
        
        prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_MOV, TAG_PAR_REPFN) if addon.CALLURL else Empty
        if not errord(addMOV(self.items, newName, prefix), TAG_ERR_OK_MOVADD):
            self.libUpdate()
            return TAG_MNU_CANCEL
            
        return rd
               
        
    def mnu_tvs(self):
    
        rd = TAG_MNU_BACKMAIN
                                                                  
        if not self.isFound : resType = subMenue([TAG_MNU_ADDNEW, TAG_MNU_ADDEXIST, TAG_MNU_ADVADD], title=normName(self.TVS.lib_defname) if self.TVS.lib_defname else titName(TAG_TTL_ADDTVS))
        else                : resType = TAG_MNU_ADDNEW
        
        if   resType == TAG_MNU_BACKMAIN : return rd
        elif resType == TAG_MNU_ADVADD   : self.mnu_advadd() 
        elif resType == TAG_MNU_ADDEXIST :
        
                tvsNames, tvsPaths = getAllTVS()
                newPath = subMenue(tvsNames, tvsPaths, cancelVal=Empty, default=DOS.unsl(self.TVS.lib_path), title=titName(TAG_TTL_CHSNAME))
                
                if not newPath : return rd
                
                self.setTVS(newPath, True)
                
        prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty        
        errn = addTVS(self.items, self.TVS, prefix)             
        if not errord(errn, TAG_ERR_OK_TVSADD, normName(self.TVS.lib_name)):
            self.linkTable.add(self.TVS.lib_path, self.items.vidCPath)
            self.libUpdate()
            return TAG_MNU_CANCEL
        
        elif errn == TAG_ERR_NONAME : return self.mnu_advadd()
        
        return rd 
    
    
    def mnu_advadd(self):
        
        rd = TAG_MNU_BACKMAIN
        
        newtvs  = tl(TAG_MNU_NEW)   
        
        def _getParam():
        
            defname = self.TVS.lib_name if self.TVS.lib_name else createName(self.items.vidFolderNameDef)
            
            aSeason, aNumb = self.TVS.get_scr_numb_and_season(self.items.vidCPath)
            
            aSeq    = self.TVS.seq 
            aSeqT   = TAG_MNU_SEANUM if not aSeq    else TAG_MNU_SEQNUM
            aNumbT  = TAG_MNU_SERDEF if not aSeason else TAG_MNU_SERTPL
            aTVS    = normName(self.TVS.lib_name) if self.TVS.lib_name else newtvs
            aName   = defname
            
            return defname, aSeq, aSeqT, aNumb, aNumbT, aSeason, aTVS, aName
        
        defname, aSeq, aSeqT, aNumb, aNumbT, aSeason, aTVS, aName = _getParam()    
        
        result  = 0
        newPath = TAG_MNU_NEW if aTVS == newtvs else Empty
        
        while result != -1:
        
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
            
            mList += [tl(TAG_MNU_STARTADD)]                      ; mVals += [5]
        
            result = subMenue(mList, mVals, cancelVal=-1, title=tl(TAG_TTL_ADVADD))
        
        
            if   result == 0:
                tvsNames, tvsPaths = getAllTVS()
                tvsNames.insert(0, tl(TAG_MNU_NEW))
                tvsPaths.insert(0, TAG_MNU_NEW)
                newPath = subMenue(tvsNames, tvsPaths, cancelVal=Empty, default=DOS.unsl(self.TVS.lib_path), title=titName(TAG_TTL_CHSNAME), defidx=0)
                if newPath:
                    if newPath == TAG_MNU_NEW : self.setTVS(Empty, False)
                    else                      : self.setTVS(newPath, True)            
                    defname, aSeq, aSeqT, aNumb, aNumbT, aSeason, aTVS, aName = _getParam()
                
                
            elif result == 1: 
                aSeqT   = TAG_MNU_SEANUM if aSeqT  == TAG_MNU_SEQNUM else TAG_MNU_SEQNUM
                
            elif result == 2: 
                while True  : 
                    aName = createName(GUI.dlgIn(tl(TAG_DLG_INNM), aName)) 
                    if aName : break
            
            elif result == 3: 
                aNumbT  = TAG_MNU_SERDEF if aNumbT == TAG_MNU_SERTPL else TAG_MNU_SERTPL
            
            elif result == 4: 
                while True  : 
                    aSeason = GUI.dlgInnum(tl(TAG_DLG_INSE), aSeason) 
                    if aSeason : break
                
            elif result == 5: 
            
                if aName2 == tl(TAG_MNU_DEFNM) and newPath == TAG_MNU_NEW and not confirm(TAG_MNU_DEFNM, aName) : continue
                
                if aSeqT  == TAG_MNU_SEQNUM :
                    if aSeq < 1 : aSeq = 1 
                    self.TVS.seq = aSeq
                if aNumbT == TAG_MNU_SERDEF : aSeason      = Empty 
                
                if newPath == TAG_MNU_NEW   : 
                    self.TVS.lib_name = aName
                    self.TVS.lib_path = LIB.tvs(aName)
                    
                prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty
                errn = addTVS(self.items, self.TVS, prefix, aSeason, aNumb)
                
                if not errord(errn, TAG_ERR_OK_TVSADD, normName(self.TVS.lib_name)):
                    self.linkTable.add(self.TVS.lib_path, self.items.vidCPath)
                    self.libUpdate()
                    return TAG_MNU_CANCEL
                    
        return rd
                
        
    def mnu_tvsu(self, isupd=True):
    
        rd = TAG_MNU_BACKMAIN
        
        prefix = TAG_PAR_CALLURLTMPL % (addon.id, TAG_TYP_TVS, TAG_PAR_REPFN) if addon.CALLURL else Empty
        season, numb = self.TVS.get_scr_numb_and_season(self.items.vidCPath)                                   
        if not errord(addTVS(self.items, self.TVS, prefix, season, numb), TAG_ERR_OK_TVSUPD, normName(self.TVS.lib_name)):
               self.linkTable.add(self.TVS.lib_path, self.items.vidCPath)
               if isupd : self.libUpdate()
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
                
        
    def mnu_help(self): 
        help.showHelp()
        
        return TAG_MNU_BACKMAIN           
        
        
    def mnu_set(self):
        GUI.openSet()
        
        oldtvsfol = LIB.tvsf
        oldmovfol = LIB.mov
        
        resetfol()
        
        if not DOS.compath(oldtvsfol, LIB.tvsf)  : DOS.rename(oldtvsfol, LIB.tvsf) 
        if not DOS.compath(oldmovfol, LIB.mov)   : DOS.rename(oldmovfol, LIB.mov) 
        
        return TAG_MNU_CANCEL 
                   
    
    def mnu_vidlibu(self):                                                                            
        self.libUpdate(True, True) 
        
        
    def mnu_vidlibcln(self):                                                              
        self.libClean (True)
        self.libUpdate(False, True)



##### Start main ...
if __name__ == '__main__':  Main()