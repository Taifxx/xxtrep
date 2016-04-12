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
#
########## COMMON:

### Import modules ...
from resources.lib.ext import *
from resources.lib.progress import *

def confirm (tag, tvsName=Empty, srcName=Empty):
    if   tag == TAG_MNU_RESCAN     : text = tl(TAG_CFR_RESCAN) % (srcName)
    elif tag == TAG_MNU_REMSRC     : text = tl(TAG_CFR_REMSRC) % (srcName)
    
    elif tag == TAG_MNU_RESTORE    : text = tl(TAG_CFR_RESTORE)
    elif tag == TAG_MNU_RESTOREALL : text = tl(TAG_CFR_RESTOREALL)
    elif tag == TAG_MNU_DELETE     : text = tl(TAG_CFR_DELETE)
    elif tag == TAG_MNU_TVSREN     : text = tl(TAG_CFR_TVSREN)
    elif tag == TAG_MNU_JOIN       : text = tl(TAG_CFR_JOIN)
    elif tag == TAG_MNU_DEFNM      : text = tl(TAG_CFR_DEFNM)  % (tvsName); tvsName = Empty
    
    if tvsName : kwargs = {'title': tvsName}
    else       : kwargs = dict()  
    
    return GUI.dlgYn (text, **kwargs)
         

def errord (error, error_ok=Empty, tvsName=Empty):

    if tvsName : txtTTL = tl(TAG_TTL_NM) % (tvsName) 
    else       : txtTTL = addon.name
   
    if error == TAG_ERR_OK: GUI.msg (txtTTL, tl(error_ok)); return False
        
    elif error == TAG_ERR_NOTFILE     : GUI.msgf  (txtTTL, tl(TAG_ERR_NOTFILE),  nottype=GUI.notWarning)
    elif error == TAG_ERR_NOTOJOIN    : GUI.msgf  (txtTTL, tl(TAG_ERR_NOTOJOIN), nottype=GUI.notWarning)
    elif error == TAG_ERR_DEDLINK     : GUI.msgf  (txtTTL, tl(TAG_ERR_DEDLINK),  nottype=GUI.notWarning)
                
    elif error == TAG_ERR_INCINPUT    : GUI.dlgOk (tl(TAG_ERR_INCINPUT),  tl(TAG_ERR_ABORT),   title=tvsName)
    elif error == TAG_ERR_LISTEMPTY   : GUI.dlgOk (tl(TAG_ERR_LISTEMPTY), tl(TAG_ERR_ABORT),   title=tvsName)
    elif error == TAG_ERR_NONAME      : GUI.dlgOk (tl(TAG_ERR_NONAME),    tl(TAG_ERR_NONAME2), title=tvsName)
    
    return True 


titName        = lambda tag, tvsName=Empty : '%s  ( %s )' % (tla(tag), normName(tvsName)) if tvsName else tla(tag)
normTargetName = lambda path               :  normName(DOS.getdir(path))  


def getAllTVS():

    fname = TAG_PAR_TVSPACK_FILE

    tvsNames   = []
    tvsPaths   = []
    folderList = DOS.listdir (LIB.tvs(Empty))[0]
    
    for fldr in folderList:
        path = LIB.tvs(fldr)
        if DOS.exists (DOS.join(path, fname)):
            tvsNames.append(setCap(fldr.replace(Dot, Space)))
            tvsPaths.append(path)
                        
    return (tvsNames, tvsPaths)


def joinTVSs(joinPaths, mainTVSPath, newName, linkTable):

    fname = TAG_PAR_TVSPACK_FILE 

    if newName : 
        newFormName = CMP.create_name_once(newName, TAG_TYP_FOLDER)
        if not newFormName : return TAG_ERR_INCINPUT, Empty, Empty 
        mainPath = LIB.tvs(newName)
        DOS.mkdirs(mainPath)
        isFound = False
    else:
        mainPath = mainTVSPath
        isFound = True
        
    try    : joinPaths.remove(mainPath)
    except : pass

    mainTVS  = CTVS.TVS(fname, mainPath, isFound)
    for path in joinPaths:
        targetTVS = CTVS.TVS(fname, path, True)
        mainTVS.join_tvs(targetTVS)
        linkTable.chpath(targetTVS.lib_path, mainTVS.lib_path, False)
        DOS.delf(DOS.join(path, fname))
        DOS.copyfls(path, mainPath, move=True)
        del targetTVS
    mainTVS.dexport()
    linkTable.save()
    
    name = mainTVS.lib_name
    path = mainTVS.lib_path
    del mainTVS     
    
    return TAG_ERR_OK, path, name


def rebuildLinkTable():

    fname = TAG_PAR_TVSPACK_FILE

    linkTable = CTVS.CLinkTable(TAG_PAR_STL_FILE, LIB.lib, load=False)
    
    tvsPaths = getAllTVS()[1]
    
    for path in tvsPaths: 
        TVS = CTVS.TVS(fname, path, Import=True)
        x,srcLinks,y,frcLinks = TVS.get_names_and_links(); del TVS
        for link in srcLinks+frcLinks : linkTable.add(path, link, save=False)
        
    linkTable.save(); del linkTable
    
    return TAG_ERR_OK


def renameTVS(newName, TVS, prefix):
    newFormName = CMP.create_name_once(newName, TAG_TYP_FOLDER)
    if not newFormName : return TAG_ERR_INCINPUT
    TVS.os_rename(newFormName)
    TVS.os_create(prefix, overwrite=True)
    
    return TAG_ERR_OK
   
    
def deleteTVS(TVS):
    TVS.os_delete()
    
    return TAG_ERR_OK


def restoreTVS(TVS, prefix):
    TVS.os_create(prefix, overwrite=True)
        
    return TAG_ERR_OK
    
    
def restoreAllTVS(prefix):

    fname = TAG_PAR_TVSPACK_FILE 
    
    tvss  = DOS.listdir(LIB.tvsf)[0]
    
    progress = CProgress(len(tvss), bg=addon.BGUPD)
    progress.show(tla(TAG_TTL_RESTOREALL))
    
    for deftvs in tvss:
        tvs = CTVS.TVS(fname, DOS.join(LIB.tvsf, deftvs), True)
        tvs.os_create(prefix, overwrite=True)
        progress.step(normName(tvs.lib_name), 1)
        del tvs             
        
    del progress
    
    return TAG_ERR_OK


def rescanSRC(items, TVS, prefix):
    TVS.os_clear()
    TVS.exclude_source_data(items.vidCPath)
    err = addTVS(items, TVS, prefix)
    return err

    
def renameSRC(oldName, newName, isfrc, TVS):
    if isfrc   : TVS.renfsource(oldName, newName) 
    else       : TVS.rensource(oldName, newName) 
    TVS.dexport()
    
    return TAG_ERR_OK
    

def removeSRC(link, isfrc, TVS, prefix):
    if isfrc   : TVS.exclude_folsource(link); TVS.dexport()  
    else       : TVS.os_exclude_src(link, prefix)
    
    return TAG_ERR_OK


def addFolSRC(items, TVS):
    TVS.exclude_folsource(items.vidCPath)
    TVS.append_fsource(items.vidCName, items.vidCPath, items.vidFolCount)
    TVS.dexport()

    return TAG_ERR_OK


def updFolSRC(items, TVS):
    TVS.reset_inum(items.vidCPath, items.vidFolCount)
    TVS.dexport()

    return TAG_ERR_OK
    
    
def setupdSRC(fnames, snames, TVS):
    TVS.set_upd(fnames, snames)
    TVS.dexport()
    
    return TAG_ERR_OK


def addMOV(items, newName, prefix, rawadd=False):

    if not rawadd and items.vidIsFolder : return TAG_ERR_NOTFILE  
    
    mov_name = CMP.create_name_once(newName if newName else items.vidCurr, TAG_TYP_PREFILE, TAG_TYP_FILE)
    svLink = prefix % (mov_name + STRM) + items.vidLink if prefix else items.vidLink
    DOS.mkdirs(LIB.mov); DOS.file(mov_name + STRM, LIB.mov, svLink, FWrite, False)
    
    return TAG_ERR_OK
    
      
def addTVS(items, TVS, prefix, defSeason=Empty, defNumb=Empty): 

    if not items.vidListItems : return TAG_ERR_LISTEMPTY
    
    rename = True if TVS.seq or defNumb else False
    addnum = TVS.seq if TVS.seq else inte(defNumb)   
      
    if not TVS.lib_path: 
        if items.vidPath : TVS.lib_path = items.vidPath
        else             : return TAG_ERR_NONAME  
    
    file_name = CMP.comps()
    src_name  = CMP.create_name_once (items.vidFolderNameDef, TAG_TYP_SRC, srcFolder=items.vidCName) 
    src_id    = TVS.append_source    (src_name, items.vidCPath, defSeason)
      
    CMP.create_name(file_name, TAG_TYP_PREFILE)
    for eps, item in enumerate(items.vidListItems):
    
        if TVS.seq or defSeason : file_name(TVS.lib_name)
        else                    : file_name(item[0]) 
        
        if   TVS.seq : season = Empty;     seq = True;  episode = TVS.seq  
        else         : season = defSeason; seq = False; episode = inte(defNumb) + eps + 1             
           
        CMP.create_name(file_name, TAG_TYP_FILE, Season=season, Episode=episode, Seq=seq)
        TVS.append_episode(item[0], file_name(), item[1], src_id)
        
    del file_name
         
    TVS.os_create(prefix)
                        
    return TAG_ERR_OK
    

def createName(name):
    if not name : return Empty
    ndir = CMP.create_name_once (name, TAG_TYP_FOLDER)
    ntvs = CMP.create_name_once (name, TAG_TYP_FOLDER, TAG_TYP_TVS)
    return ntvs if ntvs else ndir  
    
    
def checkfile(items, linkTable, recurse=False):
    
    fname  = TAG_PAR_TVSPACK_FILE
    
    containerPath = items.vidCPath       
    if    containerPath.startswith (TAG_CON_STARTSW_EXT) : container  = TAG_CON_EXT 
    elif  containerPath.startswith (TAG_CON_STARTSW_VID) : container  = TAG_CON_VID
    elif  containerPath.startswith (TAG_CON_STARTSW_PVD) : container  = TAG_CON_PVD
    else                                                 : container  = TAG_CON_LOCAL
    
    if not items.vidIsFolder: localPath = items.vidPath
    else                    : localPath = items.vidPath if container == TAG_CON_VID else items.vidFPath 
     
    ltPath    = Empty
    linkLocal = linkTable.find(localPath)
    linkExt   = linkTable.find(containerPath)
    
    if   linkLocal : ltPath = linkLocal
    elif linkExt   : ltPath = linkExt
    
    if ltPath:
        
        if DOS.exists(DOS.join(ltPath, fname)): 
            path    = ltPath
            isFound = True
        else: 
            rebuildLinkTable(); linkTable.load()
            if not recurse : return checkfile(items, linkTable, recurse=True)

    else:
    
        cmpFolderName = CMP.comps()
        
        if items.vidIsFolder :
              cmpFolderName   (items.vidCurr)
              CMP.create_name (cmpFolderName, TAG_TYP_FOLDER)
              
              nameByTargetFolder = cmpFolderName()
        else: nameByTargetFolder = Empty
        
        noTamplate = False
        cmpFolderName   (items.vidFolderNameDef)
        CMP.create_name (cmpFolderName, TAG_TYP_FOLDER, TAG_TYP_TVS)
        
        if  cmpFolderName.isempty() :
            noTamplate = True
            cmpFolderName   (items.vidFolderNameDef)
            CMP.create_name (cmpFolderName, TAG_TYP_FOLDER)
                  
        nameByFirst = cmpFolderName()
            
        cmpFolderName   (DOS.getdir(items.vidLink))
        CMP.create_name (cmpFolderName, TAG_TYP_FOLDER)
        
        nameByLink  = cmpFolderName()
             
        externalPath1   = LIB.tvs(nameByTargetFolder)
        externalPath2   = LIB.tvs(nameByFirst)
        externalPath3   = LIB.tvs(nameByLink)
        
        isFound = True; Path = Empty
        if    DOS.exists(DOS.join(localPath    , fname)) : path = localPath 
        elif  DOS.exists(DOS.join(externalPath1, fname)) : path = externalPath1
        elif  DOS.exists(DOS.join(externalPath2, fname)) : path = externalPath2 
        elif  DOS.exists(DOS.join(externalPath3, fname)) : path = externalPath3
        else: isFound = False; path = externalPath2 if not noTamplate else Empty
        
        del cmpFolderName
    
    items.vidPath = path
         
    return (isFound, container, path)
    
    
def globalUpdateCheck():
    
    fname  = TAG_PAR_TVSPACK_FILE
    
    tmplist = DOS.listdir(LIB.tvsf)[0]
    
    progress = CProgress(len(tmplist)*100, bg=addon.BGUPD)
    progress.show(tla(TAG_TTL_CHKUPDGL))
    
    sList = []; fList = []
    for itm in tmplist:
        
        path = LIB.tvs(itm)
        
        TVS = CTVS.TVS(fname, path, True)
        u_sNames, u_sLinks, u_fNames, u_fLinks = TVS.check_new_eps(globp=progress, globmsg=normName(TVS.lib_name))
        
        if u_sNames : 
            ustvs = dict()
            ustvs['name'] = itm
            ustvs['path'] = path
            ustvs['pack'] = DOS.join(path, fname)
            ustvs['ups']  = [u_sNames, u_sLinks]
            sList.append(ustvs)
            del ustvs
        
        if u_fNames :
            uftvs = dict()
            uftvs['name'] = itm
            uftvs['path'] = path
            uftvs['pack'] = DOS.join(path, fname)
            uftvs['ups']  = [u_fNames, u_fLinks]
            fList.append(uftvs)
            del uftvs
         
        del TVS
    
    del progress
    
    return sList, fList
    

class CSRC:
    def __init__(self, tsrc_names, tsrc_links, tfrc_names, tfrc_links):
         self.frclen   = len(tfrc_names)
         self.links    = tfrc_links + tsrc_links
         self.names    = tfrc_names + tsrc_names
         self.remnames = [tl(TAG_MNU_SRE) + itm for itm in tfrc_names] + tsrc_names
         self.idxs     = range(len(self.names))
         self._idx     = -1
    
    def exclude(self, link):
        if link in self.links:
            name    = self.getlinkname(link)
            idx     = self.getlinkidx (link)
            remname = tl(TAG_MNU_SRE) + name
            
            if not idx > self.frclen - 1 : 
                  self.frclen -= 1
                  self.remnames.remove(remname)
            else: self.remnames.remove(name)
            
            self.links.remove(link)   
            self.names.remove(name)   
            self.idxs = range(len(self.names))       
    
    def __call__(self, zidx): 
         if type(zidx) == int:
             self._idx  = zidx
             self.name  = self.names[zidx] if zidx != -1 else Empty
             self.link  = self.links[zidx] if zidx != -1 else Empty 
             self.isf   = False if zidx > self.frclen - 1 else True
             self.isidx = True if zidx != -1 else False
         else: 
             self.fnames = [self.names[idx] for idx in zidx if idx <= self.frclen - 1]
             self.snames = [self.names[idx] for idx in zidx if idx >  self.frclen - 1]
    
    def getidxs(self, gNames): 
         return [idx for idx in self.idxs if self.names[idx] in gNames]                         
          
    def getlinkname(self, link):
         for idx, itm in enumerate(self.names):
             if link == self.links[idx] : return itm
         return Empty
    
    def getlinkidx(self, link):
         for idx, itm in enumerate(self.links):
             if link == itm : return idx
         return -1
    
    def isnewsrc(self, link):
        return False if link in self.links and self.getlinkidx(link) > self.frclen - 1 else True
    
    def isnewfrc(self, link):
        return False if link in self.links and self.getlinkidx(link) <= self.frclen - 1 else True
    
    def getfrc(self):
        return self.names[:self.frclen], self.links[:self.frclen]    
    
    def getsrc(self):
        return self.names[self.frclen:], self.links[self.frclen:] 
        
    