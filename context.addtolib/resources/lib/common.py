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
from ext import *
import ctvsobj as CTVS
import call 


def confirm (tag, tvsName=Empty, srcName=Empty):
    if   tag == TAG_MNU_RESCAN     : text = tl(TAG_CFR_RESCAN)   % (srcName)
    elif tag == TAG_MNU_REMSRC     : text = tl(TAG_CFR_REMSRC)   % (srcName)
    elif tag == TAG_ACT_RESTBACK   : text = tl(TAG_CFR_RESTBACK) % (srcName)
    
    elif tag == TAG_ACT_REMBACK    : text = tl(TAG_CFR_REMBACK)
    elif tag == TAG_ACT_RENAMER    : text = tl(TAG_CFR_RENAMER)
    elif tag == TAG_MNU_RESCANFULL : text = tl(TAG_CFR_RESCANFULL)
    elif tag == TAG_MNU_RESCANALLS : text = tl(TAG_CFR_RESCANALLS)
    elif tag == TAG_MNU_RESTORE    : text = tl(TAG_CFR_RESTORE)
    elif tag == TAG_MNU_RESTOREALL : text = tl(TAG_CFR_RESTOREALL)
    elif tag == TAG_MNU_DELETE     : text = tl(TAG_CFR_DELETE)
    elif tag == TAG_MNU_TVSREN     : text = tl(TAG_CFR_TVSREN)
    elif tag == TAG_MNU_JOIN       : text = tl(TAG_CFR_JOIN)
    elif tag == TAG_MNU_DEFNM      : text = tl(TAG_CFR_DEFNM)  % (tvsName); tvsName = Empty
    
    elif tag == TAG_CFR_UNLOCK     : text = tl(TAG_CFR_UNLOCK); tvsName = Empty
    
    if tvsName : kwargs = {'title': tvsName}
    else       : kwargs = dict()  
    
    return GUI.dlgYn (text, **kwargs)
         

def errord (error, error_ok=Empty, tvsName=Empty, exten=Empty):

    if tvsName : txtTTL = tl(TAG_TTL_NM) % (tvsName) 
    else       : txtTTL = tl(TAG_TTL_NM) % (addon.name)
   
    if error == TAG_ERR_OK: GUI.msg (txtTTL, tl(error_ok)); return False
        
    elif error == TAG_ERR_NOTFILE     : GUI.msgf  (txtTTL, tl(TAG_ERR_NOTFILE),      nottype=GUI.notWarning)
    elif error == TAG_ERR_NOTOJOIN    : GUI.msgf  (txtTTL, tl(TAG_ERR_NOTOJOIN),     nottype=GUI.notWarning)
    elif error == TAG_ERR_DEDLINK     : GUI.msgf  (txtTTL, tl(TAG_ERR_DEDLINK),      nottype=GUI.notWarning)
    elif error == TAG_ERR_LIBACT      : GUI.msgf  (txtTTL, tl(TAG_ERR_LIBACT),       nottype=GUI.notError)
    elif error == TAG_ERR_LOCK        : GUI.msgf  (txtTTL, tl(TAG_ERR_LOCK),         nottype=GUI.notWarning)
    elif error == TAG_ERR_NOBCKPATHM  : GUI.msgf  (txtTTL, tl(TAG_ERR_NOBCKPATHM),   nottype=GUI.notError) 
    elif error == TAG_ERR_NODBXCONNECT: GUI.msgf  (txtTTL, tl(TAG_ERR_NODBXCONNECT), nottype=GUI.notError)
    elif error == TAG_ERR_BROKENLINK  : GUI.msgf  (txtTTL, tl(TAG_ERR_BROKENLINK),   nottype=GUI.notError)        
                
    elif error == TAG_ERR_INCINPUT    : GUI.dlgOk (tl(TAG_ERR_INCINPUT),  tl(TAG_ERR_ABORT),   title=tvsName)
    elif error == TAG_ERR_LISTEMPTY   : GUI.dlgOk (tl(TAG_ERR_LISTEMPTY), tl(TAG_ERR_ABORT),   title=tvsName)
    elif error == TAG_ERR_NONAME      : GUI.dlgOk (tl(TAG_ERR_NONAME),    tl(TAG_ERR_NONAME2), title=tvsName)
    
    elif error == TAG_ERR_LIB         : GUI.dlgOk (tl(TAG_ERR_LIB))
    elif error == TAG_ERR_OL          : GUI.dlgOk (tl(TAG_ERR_OL))
    elif error == TAG_ERR_BADZIP      : GUI.dlgOk (tl(TAG_ERR_BADZIP))
    elif error == TAG_ERR_NOBCKPATH   : GUI.dlgOk (tl(TAG_ERR_NOBCKPATH))
    elif error == TAG_ERR_DBXISLOCK   : GUI.dlgOk (tl(TAG_ERR_DBXISLOCK) % (NewLine))
    
    return True 


titName        = lambda tag, tvsName=Empty : '%s  ( %s )' % (tla(tag), normName(tvsName)) if tvsName else tla(tag)
normTargetName = lambda path               :  normName(DOS.getdir(path)) 


def backup(auto=False):
    
    extpath = Empty if DOS.isvfs(LIB.lib) == 0 else LIB.lib
        
    if DOS.isvfs(addon.BKUPPATH) == -1 : DOS.mkdirs(addon.BKUPPATH)
    isvfs = DOS.isvfs(addon.BKUPPATH)
        
    if isvfs == -1 : return TAG_ERR_NOBCKPATHM if auto else TAG_ERR_NOBCKPATH
       
    extbckpath = Empty if isvfs == 0 else addon.BKUPPATH
    
    _backup(extpath, extbckpath, auto)
    
    return TAG_ERR_OK
    

def _backup(extpath, extbckpath, auto=False):
    
    steps = 140
    if extpath    : steps += 20
    if extbckpath : steps += 15
    
    bckp_template = TAG_PAR_SYSFLSTMPL if addon.FASTBCKP else Empty 
    
    progress = CProgress(steps, bg=addon.BGUPD if not auto else True)
    if not addon.HIDEBCKPRGS or not auto : progress.show(tla(TAG_TTL_BACKUP))
    
    remtmp(progress, 20)
    
    if not extpath : libpath = LIB.lib
    else:
        tmp = DOS.join(addon.profile, TAG_PAR_TMP)
        DOS.mkdirs(tmp)
        libpath = tmp
        progress.step(tla(TAG_TTL_RESTATC), 10)
        DOS.copyfls(extpath, tmp, template=bckp_template)
    
    if not extbckpath : bckpath = addon.BKUPPATH
    else:
        tmpa = DOS.join(addon.profile, TAG_PAR_TMPA)
        DOS.mkdirs(tmpa)
        bckpath = tmpa  
    
    zipname  = TAG_PAR_ZIPTMPL % (getdate(), getunftime())
    fullname = DOS.join(bckpath, zipname)
    
    zipfile  = ZIP.CZIP(fullname)
    #flcount  = zipfile.zipdir(libpath, progress, tla(TAG_TTL_PACK) if extpath or extbckpath else Empty)
    flcount  = zipfile.zipdir(libpath, progress, tla(TAG_TTL_PACK), template=bckp_template)
    
    zipfile.close
    del zipfile
    
    newname     = zipname.replace(TAG_PAR_ZIPCN, str(flcount))
    newfullname = fullname.replace(zipname, newname) 
    DOS.rename(fullname, newfullname)
    
    if extbckpath:
        progress.step(tla(TAG_TTL_RESTAT), 10) 
        DOS.copyfls(tmpa, extbckpath)
        progress.step(tla(TAG_TTL_RESTRTMP), 5)
        DOS.remove(tmpa)
    
    if extpath:
        progress.step(tla(TAG_TTL_RESTRTMP), 10) 
        DOS.remove(tmp)
    
    progress.step(tla(TAG_TTL_REMOLDBCK), 10)
    if addon.BKUPREMOLD : remove_old_backups()
    
    progress.step(Empty, 10)  

        
def restore_lib(bckname):
    extpath    = Empty if DOS.isvfs(LIB.lib)        == 0 else LIB.lib
    extbckpath = Empty if DOS.isvfs(addon.BKUPPATH) == 0 else addon.BKUPPATH
    return _restore_lib(bckname, extpath, extbckpath)


def _restore_lib(bckname, extpath, extbckpath):

    def maskfnc(path, fls):
        for tmpl in TAG_PAR_SYSFLSTMPL:
            if fls.find(tmpl) != -1 : return True
        return False 
    
    
    steps = 6
    if extpath    : steps += 2
    if extbckpath : steps += 1 
    
    progress = CProgress(steps, bg=False)
    progress.show(tla(TAG_TTL_RESTLIB))
    
    remtmp(progress, 2)
    
    if not extpath : rlibpath = libpath = LIB.lib
    else:
        tmp = DOS.join(addon.profile, TAG_PAR_TMP)
        DOS.mkdirs(tmp)
        libpath  = tmp
        rlibpath = extpath 
    
    if not extbckpath : bckpath = addon.BKUPPATH
    else:
        tmpa = DOS.join(addon.profile, TAG_PAR_TMPA)
        DOS.mkdirs(tmpa)
        bckpath = tmpa
        progress.step(tla(TAG_TTL_RESTAT))
        DOS.copyf(DOS.join(extbckpath, bckname), DOS.join(tmpa, bckname))  
    
    zipfile = ZIP.CZIP(DOS.join(bckpath, bckname), FRead)
    
    progress.step(tla(TAG_TTL_RESTCHK))
    if not zipfile.crc() : return TAG_ERR_BADZIP

    progress.step(tla(TAG_TTL_RESTRL))
    DOS.remove(rlibpath, delDir=False, maskfn=maskfnc if addon.SAVEONREST else None)
    progress.step(tla(TAG_TTL_RESTUL))
    zipfile.unzip(libpath)
    
    zipfile.close
    del zipfile
    
    if extpath:
        progress.step(tla(TAG_TTL_RESTATC))
        DOS.copyfls(tmp, extpath)
        progress.step(tla(TAG_TTL_RESTRTMP)) 
        DOS.remove(tmp)
    
    if extbckpath : DOS.remove(tmpa)
    progress.step(Empty) 
    
    return TAG_ERR_OK


_bid = lambda name : '%s%s%s%s%s%s' % (parse_backupname(name)[:6])


def get_all_sort_backups():
    bcklist = get_all_backups()
    if bcklist == -1 : return -1
    
    bckbids = [(_bid(file), file) for file in bcklist]
    bckbids.sort(); bckbids.reverse()  
    return [file for bid, file in bckbids]


def get_all_backups():
    if DOS.isvfs(addon.BKUPPATH) == -1 : return -1
    return [file for file in DOS.listdir(addon.BKUPPATH)[1] if file.startswith(TAG_PAR_ZIPST)]


def remove_all_backups():
    if DOS.isvfs(addon.BKUPPATH) == -1 : return TAG_ERR_NOBCKPATH
    for file in get_all_backups() : DOS.delf(DOS.join(addon.BKUPPATH, file))
    return TAG_ERR_OK


def remove_old_backups():
    bcklist = get_all_backups()
    if bcklist == -1 : return
    
    if len(bcklist) <= addon.BKUPNUM : return
    
    bckbids = [(_bid(file), file) for file in bcklist]; bckbids.sort()
    wlist   = [file for bid, file in bckbids[addon.BKUPNUM*-1:]]
    for file in bcklist:
        if file not in wlist : DOS.delf(DOS.join(addon.BKUPPATH, file)) 
     

def parse_backupname(name):
    if not name : return Empty
    parts = name.split(Dot)
    d = parts[2].split(Dash)
    t = parts[3].split(Dash)
    c = parts[4]
    return d[2], d[1], d[0], t[0], t[1], t[2], c


def srcRenamer():

    fname = TAG_PAR_TVSPACK_FILE

    tvsNames, tvsPaths = getAllTVS()
    
    if not tvsNames : return
    
    progress = CProgress(len(tvsNames), bg=addon.BGUPD)
    progress.show(tla(TAG_SET_RENAMER))
    
    for path in tvsPaths:
        tvs = CTVS.TVS(fname, path, True)
        episodes, fsources, sources  = tvs.get_direct()
        progress.step(normName(tvs.lib_name), 1)
        for src in sources:
            src_oldname = src['src_name']
            src_id      = src['src_id']
            eps_name    = Empty
            for eps in episodes:
                if eps['src_id'] == src_id : eps_name = eps['new_name']; break
                
            if eps_name: 
                src_newname = CMP.create_name_once (eps_name, TAG_TYP_SRC, srcFolder=src_oldname, season=Empty)
                if src_newname : tvs.rensource(src_oldname, src_newname)
        
        tvs.dexport()
        del tvs
    del progress


def getTVSsPlugs():

    fname = TAG_PAR_TVSPACK_FILE

    tvsNames, tvsPaths = getAllTVS()
    
    if not tvsNames : return []
    
    prefixes = []
    
    for path in tvsPaths:
        tvs = CTVS.TVS(fname, path, True)
        episodes, fsources, sources  = tvs.get_direct()
        
        for src in sources:
            prefix = call.getURLPrefix(src['src_link'])
            if prefix not in prefixes and src['src_upd'] == True : prefixes.append(prefix)
        
        for frc in fsources:
            prefix = call.getURLPrefix(frc['fsrc_link'])
            if prefix not in prefixes and frc['fsrc_upd'] == True : prefixes.append(prefix)
        
        del tvs 
            
    return prefixes


def excludeUPDPlug(plugin):

    fname = TAG_PAR_TVSPACK_FILE

    tvsNames, tvsPaths = getAllTVS()
    
    if not tvsNames : return []
    
    for path in tvsPaths:
        tvs = CTVS.TVS(fname, path, True)
        episodes, fsources, sources  = tvs.get_direct()
        
        fsources_upd = []
        sources_upd  = []
        
        for src in sources:
            prefix = call.getURLPrefix(src['src_link'])
            if prefix != plugin and src['src_upd'] == True : sources_upd.append(src['src_name'])
        
        for frc in fsources:
            prefix = call.getURLPrefix(frc['fsrc_link'])
            if prefix != plugin and frc['fsrc_upd'] == True : fsources_upd.append(frc['fsrc_name'])
        
        tvs.set_upd(fsources_upd, sources_upd)
        tvs.dexport()
        del tvs

    return TAG_ERR_OK
              

def remtmp(progress, stepv):
    tmp  = DOS.join(addon.profile, TAG_PAR_TMP)
    tmpa = DOS.join(addon.profile, TAG_PAR_TMPA)
    
    prt = 0.0
    if not DOS.exists(tmp) : prt += 1
    if not DOS.exists(tmpa): prt += 1
    if not prt : progress.step(tla(TAG_TTL_CLRERRDT), stepv); return
    
    progress.step(tla(TAG_TTL_CLRERRD), stepv / prt)
    DOS.remove(tmp)
    progress.step(tla(TAG_TTL_CLRERRD), stepv / prt)
    DOS.remove(tmpa)


def check_lib_folders(now=True):

    fname = TAG_PAR_FSET_FILE
    fSep  = TAG_PAR_TVSPACK_FSEP
    
    err   = False
    
    if now:
        oldtvsfol = LIB.tvsf
        oldmovfol = LIB.mov
        
    else:
        try:
            oldmovfol, oldtvsfol = DOS.file(fname, LIB.lib, fType=FRead).replace(CR, Empty).split(fSep)
        except : err = True 
            
    pack  = fSep.join([LIB.mov, LIB.tvsf]) 
    DOS.file(fname, LIB.lib, pack, fRew = True)
    
    if err : return
    
    if not DOS.compath(oldtvsfol, LIB.tvsf)  : DOS.rename(oldtvsfol, LIB.tvsf) 
    if not DOS.compath(oldmovfol, LIB.mov)   : DOS.rename(oldmovfol, LIB.mov)


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

def saveTVSupd(sList, fList):
    
    fname = TAG_PAR_TVSUPD_FILE
    
    lSep = TAG_PAR_TVSPACK_LSEP
    sSep = TAG_PAR_TVSPACK_SSEP
    fSep = TAG_PAR_TVSPACK_FSEP 
    eSep = TAG_PAR_TVSPACK_ESEP + NewLine
    pSep = TAG_PAR_TVSPACK_PSEP + NewLine
    
    sList_packed = Empty
    fList_packed = Empty
        
    if sList : sList_packed = eSep.join([fSep.join([itm['name'], itm['path'], itm['pack'], lSep.join(itm['ups'][0])+sSep+lSep.join(itm['ups'][1])]) for itm in sList])
    if fList : fList_packed = eSep.join([fSep.join([itm['name'], itm['path'], itm['pack'], lSep.join(itm['ups'][0])+sSep+lSep.join(itm['ups'][1])]) for itm in fList]) 
    pack = sList_packed+pSep+fList_packed  
    
    DOS.file(fname, LIB.lib, pack, fRew = True)


def loadTVSupd():

    fname = TAG_PAR_TVSUPD_FILE

    pack = DOS.file(fname, LIB.lib, fType=FRead)
    
    fList = []
    sList = []    
    
    if pack == -1 : return sList, fList
    
    lSep = TAG_PAR_TVSPACK_LSEP
    sSep = TAG_PAR_TVSPACK_SSEP
    fSep = TAG_PAR_TVSPACK_FSEP 
    eSep = TAG_PAR_TVSPACK_ESEP + NewLine
    pSep = TAG_PAR_TVSPACK_PSEP + NewLine
    
    sListPacked, fListPacked = pack.split(pSep)
    
    if sListPacked : sList = [{'name':itm2, 'path':itm3, 'pack':itm4, 'ups':[itm6.split(lSep), itm7.split(lSep)]} for itm in sListPacked.split(eSep) for itm2, itm3, itm4, itm5  in [itm.split(fSep)] for itm6, itm7 in [itm5.split(sSep)]]
    if fListPacked : fList = [{'name':itm2, 'path':itm3, 'pack':itm4, 'ups':[itm6.split(lSep), itm7.split(lSep)]} for itm in fListPacked.split(eSep) for itm2, itm3, itm4, itm5  in [itm.split(fSep)] for itm6, itm7 in [itm5.split(sSep)]]   
    
    return sList, fList
    
    
def clearTVSupd():
    fname  = TAG_PAR_TVSUPD_FILE
    fname2 = TAG_PAR_TVSUPDNOW_FILE
    DOS.delf(DOS.join(LIB.lib, fname))    
    DOS.delf(DOS.join(LIB.lib, fname2))
   
    
def isGlUpProcess():
    fname  = TAG_PAR_TVSUPD_FILE
    fname2 = TAG_PAR_TVSUPDNOW_FILE
    if DOS.exists(DOS.join(LIB.lib, fname)) and DOS.exists(DOS.join(LIB.lib, fname2)) : return True
    else                                                                              : return False 
    

def updnow(updflag):
    fname2 = TAG_PAR_TVSUPDNOW_FILE
    if updflag : DOS.file(fname2, LIB.lib, Empty, fRew = True)
    else       : DOS.delf(DOS.join(LIB.lib, fname2))

def isUpdnow():
    fname2 = TAG_PAR_TVSUPDNOW_FILE
    if DOS.exists(DOS.join(LIB.lib, fname2)) : return True
    else                                     : return False
        

def isNoGlUp():
    fname  = TAG_PAR_TVSUPD_FILE
    if DOS.exists(DOS.join(LIB.lib, fname)) : return False
    else                                    : return True
    

def remLinkTVSupd(path, link):
    sList, fList = loadTVSupd()
    lfind = False
    for itm in fList:
        if itm['path'] == path: 
            for idx, itm2 in enumerate(itm['ups'][1]): 
                if itm2 == link: 
                    itm['ups'][0].pop(idx)
                    itm['ups'][1].pop(idx)
                    lfind = True
                    break        
              
        if not itm['ups'][0] : fList.remove(itm)
        if lfind : break
    
    if sList or fList : saveTVSupd(sList, fList)
    else              : clearTVSupd()


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
        progress.step(normName(tvs.lib_name), 1)
        tvs.os_create(prefix, overwrite=True)
        del tvs             
        
    del progress
    
    return TAG_ERR_OK
    
    
def rescanSRC(items, TVS, prefix, rescSeason=Empty, cornum=[]):
    #if items.vidCPath in TVS.get_raw_link_list() : return TAG_MNU_RAWADD 
    if len(TVS.get_eps_names_and_links_forsrc(items.vidCPath)[0]) > len(items.vidListItems) and not rescSeason:
        if not GUI.dlgYn (tl(TAG_ERR_BROKENLINK), tl(TAG_ERR_BROKENLINK2) % (NewLine, TVS.get_src_name_by_link(items.vidCPath)), title=normName(TVS.lib_name)): 
            return TAG_ERR_BROKENLINK  
    
    season, numb, mode = TVS.get_scr_numb_season_mode(items.vidCPath)
    remove_src = False
    if mode : items.convertToFolderMode()
    if rescSeason == -1 : rescSeason = season = Empty; remove_src = True
    elif rescSeason : season = rescSeason    
    TVS.os_exclude_src(items.vidCPath, dexport=False, season=rescSeason, remove_src=remove_src)
    err = addTVS(items, TVS, prefix, season, 0, cornum, folmode=mode)
       
    return err


# def rescanSRC(items, TVS, prefix):
#     TVS.os_clear()
#     TVS.exclude_source_data(items.vidCPath)
#     err = addTVS(items, TVS, prefix)
#     return err

    
def renameSRC(oldName, newName, isfrc, TVS):
    if isfrc   : TVS.renfsource(oldName, newName) 
    else       : TVS.rensource(oldName, newName) 
    TVS.dexport()
    
    return TAG_ERR_OK
    

def removeSRC(link, isfrc, TVS, prefix):
    if isfrc   : TVS.exclude_folsource(link); TVS.dexport()  
    else       : TVS.os_exclude_src(link, dexport=True)
    
    return TAG_ERR_OK


def addFolSRC(items, TVS):
    TVS.exclude_folsource(items.vidCPath)
    TVS.append_fsource(items.vidCName, items.vidCPath, items.vidFolCount)
    TVS.dexport()

    return TAG_ERR_OK


def updFolSRC(items, TVS):
    TVS.reset_inum(items.vidCPath, items.vidFolCount)
    TVS.dexport()
    
    remLinkTVSupd(TVS.lib_path, items.vidCPath)

    return TAG_ERR_OK
    
    
def setupdSRC(fnames, snames, TVS):
    TVS.set_upd(fnames, snames)
    TVS.dexport()
    
    return TAG_ERR_OK
    

def renEPS(TVS, src_id, newName, oldname, prefix):
    #TVS.os_rename_eps(reslink, newName, oldname, prefix)
    TVS.os_rename_eps(src_id, newName, oldname, prefix)
    
    return TAG_ERR_OK


def removeEPS(TVS, src_id, epsName):
    TVS.os_remove_eps(src_id, epsName)
    
    return TAG_ERR_OK


def addMOV(items, newName, prefix, rawadd=False):

    if not rawadd and items.vidIsFolder : return TAG_ERR_NOTFILE  
    
    mov_name = CMP.create_name_once(newName if newName else items.vidCurr, TAG_TYP_PREFILE, TAG_TYP_FILE)
    svLink = prefix % (mov_name + STRM) + items.vidLink if prefix else items.vidLink
    DOS.mkdirs(LIB.mov); DOS.file(mov_name + STRM, LIB.mov, svLink, FWrite, False)
    
    return TAG_ERR_OK
    
      
def addTVS(items, TVS, prefix, defSeason=Empty, defNumb=Empty, cornum=Empty, folmode=False): 

    if not items.vidListItems : return TAG_ERR_LISTEMPTY
    
    rename = True if TVS.seq or defNumb else False
    addnum = TVS.seq if TVS.seq else inte(defNumb)   
      
    if not TVS.lib_path: 
        if items.vidPath : TVS.lib_path = items.vidPath
        else             : return TAG_ERR_NONAME  
    
    file_name = CMP.comps()
    src_name  = CMP.create_name_once (items.vidFolderNameDef, TAG_TYP_SRC, srcFolder=items.vidCName, season=defSeason) 
    src_id    = TVS.append_source    (src_name, items.vidCPath, defSeason, src_folmode=folmode, src_numb=inte(defNumb))
      
    CMP.create_name(file_name, TAG_TYP_PREFILE)
    maxcorn = max(cornum) if cornum else 0 
    eps     = 0 
    for item in items.vidListItems:
    
        if TVS.seq or defSeason : file_name(TVS.lib_name)
        else                    : file_name(item[0]) 
        
        season = Empty if TVS.seq else defSeason 
        seq    = True  if TVS.seq else False 
        
        while True:
            episode = TVS.seq if TVS.seq else inte(defNumb) + eps + 1  
            if not cornum        : break 
            if episode in cornum : break
            if episode > maxcorn : break
            
            if TVS.seq : TVS.incSeq()
            else       : TVS.incSN(); eps += 1                         
           
        CMP.create_name(file_name, TAG_TYP_FILE, Season=season, Episode=episode, Seq=seq)
        TVS.append_episode(item[0], file_name(), item[1], src_id, season=defSeason)
        
        eps += 1
        
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
    
    isOL   = False
    
    containerPath = items.vidCPath       
    if    containerPath.startswith (TAG_CON_STARTSW_EXT) : container  = TAG_CON_EXT 
    elif  containerPath.startswith (TAG_CON_STARTSW_VID) : container  = TAG_CON_VID
    elif  containerPath.startswith (TAG_CON_STARTSW_PVD) : container  = TAG_CON_PVD
    else                                                 : container  = TAG_CON_LOCAL
    
    isMovie = False
    if container in [TAG_CON_VID, TAG_CON_LOCAL]:
        mlPath = items.vidLink
        if mlPath and mlPath.startswith(LIB.mov):
            isFound = False
            isMovie = True
            path    = mlPath
            return (isFound, container, path, isOL, isMovie)
    
    
    if container != TAG_CON_EXT:
        if not items.vidIsFolder: localPath = items.vidPath
        else                    : localPath = items.vidPath if container == TAG_CON_VID else items.vidFPath
    else : localPath = Empty 
     
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
    
    #if not path.startswith(LIB.lib) and container in [TAG_CON_VID, TAG_CON_LOCAL] : isOL = True 
    if not path.startswith(LIB.lib) and isFound:
        isFound = False 
        if container == TAG_CON_VID : isOL = True
    
    items.vidPath = path
         
    return (isFound, container, path, isOL, isMovie)
    
    
def globalUpdateCheck(shadbg=False):
    
    fname  = TAG_PAR_TVSPACK_FILE
    
    tmplist = DOS.listdir(LIB.tvsf)[0]
    
    bgmode   = addon.BGUPD if not shadbg else True 
    progress = CProgress(len(tmplist)*100, bg=bgmode)
    
    if not addon.HIDEAUPD or not addon.SILENTUPD or not addon.ALLOWSHADOW : progress.show(tla(TAG_TTL_CHKUPDGL))
    
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
         self.fsidxs   = []
    
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
             self.fsidxs = [idx for idx in zidx]
    
    def filtering(self):
        removed_links = []
        for idx in self.idxs:
            if idx == -1 : continue
            if idx not in self.fsidxs : removed_links.append(self.links[idx])
            
        for link in removed_links:
            self.exclude(link)         
    
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
        
    def srccount(self):
        return len(self.names) - self.frclen 
    
    def nextsidx(self):
        if self.srccount() : self.__call__(self.frclen); return True 
        else               : return False 
    
    def clone(self, nofrc=False):
        tsrc_names, tsrc_links = self.getsrc()
        
        if nofrc : tfrc_names = []; tfrc_links = []
        else     : tfrc_names, tfrc_links = self.getfrc() 
        
        return CSRC(tsrc_names, tsrc_links, tfrc_names, tfrc_links)
  
        
### Emegrancy exit control ...
class emgrControl:
    def __init__(self):
        self._sepLST = TAG_PAR_TVSPACK_LSEP
        self._sepPRT = TAG_PAR_TVSPACK_PSEP + NewLine
    
    def _laactt_wr(self, actions):
        jact = []
        for akey, aval in actions.items():
            jact.append(str(akey)+self._sepLST+str(aval))
        laacttData = self._sepPRT.join(jact)
        DOS.file(TAG_PAR_LAACTT, addon.profile, laacttData, fType=FWrite, fRew=True)
    
    def _laactt_rd(self):
        laacttData = DOS.file(TAG_PAR_LAACTT, addon.profile, fType=FRead) 
        if laacttData == -1: return Empty         
        return {int(_actid):_acttime for rec in laacttData.split(self._sepPRT) for _actid, _acttime in [rec.split(self._sepLST)]}
    
    def setLAACTT(self, actId):
        actions = self._laactt_rd()
        aRec    = {actId:time.time()}
        if not actions : actions = aRec
        else           : actions.update(aRec)
        self._laactt_wr(actions)
        
    def isEmgrExit(self, actId, period):
        actions = self._laactt_rd()
        if not actions : return False
        laacttTime = actions.get(actId, Empty)
        if not laacttTime : return False
        if time.time() - float(laacttTime) > period : return False
        return True


### Video Library CMD's ...
class VideoLib():
    
    def __init__(self):
        self._jRemoveMovie = lambda mid   : self._jsex('{"jsonrpc": "2.0", "method": "VideoLibrary.RemoveMovie",  "params": { "movieid": %s }, "id": "1"}' % str(mid))
        self._jGetMovies   = lambda       : self._js  ('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies",    "params": { "properties": ["file"] }, "id": 1}', 'movies')
        
        self._jRemoveTVS   = lambda tvsid : self._jsex('{"jsonrpc": "2.0", "method": "VideoLibrary.RemoveTVShow", "params": { "tvshowid": %s }, "id": "1"}' % str(tvsid))
        self._jGetTVSs     = lambda       : self._js  ('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows",   "params": { "properties": ["file"] }, "id": 1}', 'tvshows')
        
        self._jRemoveEpisode = lambda epsid : self._jsex('{"jsonrpc": "2.0", "method": "VideoLibrary.RemoveEpisode", "params": { "episodeid": %s }, "id": "1"}' % str(epsid))
        self._jGetEpisodes   = lambda tvsid : self._js  ('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes",  "params": { "properties": ["file"], "tvshowid": %s }, "id": 1}' % str(tvsid), 'episodes')       
        

    def _js(self, cmd, key):
        try:
            return eval(self._jsex(cmd))['result'][key]
        except: return []
    
    def _jsex(self, cmd):
        return xbmc.executeJSONRPC(cmd)
    
    def _removeMovie(self, movfile, movList):
        mid = -1
        for mov in movList:
            if DOS.compath(mov['file'], movfile) : mid = mov['movieid']; break   
        if mid != -1: 
            self._jRemoveMovie(mid)
            return True
        return False  
    
    def removeMovie(self, movfile): 
        movList = self._jGetMovies()
        result  = self._removeMovie(movfile, movList)
        if result : GUI.refresh() 
        return result
            
    def removeTVS(self, tvsfile): 
        tvsid = -1
        #tvsfile = TVS.lib_path
        tvsList = self._jGetTVSs()
        for tvs in tvsList:
            if DOS.compath(tvs['file'], tvsfile) : tvsid = tvs['tvshowid']; break
        if tvsid != -1: 
            self._jRemoveTVS(tvsid)  
            GUI.refresh()
            return True
        return False
    
    def removeEpisode(self, tvsfile, epsfile): 
        tvsList = self._jGetTVSs()
        result = self._removeEpisode(tvsfile, epsfile, tvsList)
        if result : GUI.refresh() 
        return result
    
    def eviscerateTVS(self, tvsfile):
        tvsid = -1
        tvsList = self._jGetTVSs()
        for tvs in tvsList:
            if DOS.compath(tvs['file'], tvsfile) : tvsid = tvs['tvshowid']; break
        if tvsid == -1 : return False
        epsList = self._jGetEpisodes(tvsid)
        for eps in epsList:
            epsid = eps['episodeid']
            self._jRemoveEpisode(epsid)      
        GUI.refresh()
        return True
    
    def _removeEpisode(self, tvsfile, epsfile, tvsList):
        tvsid = -1
        epsid = -1
        for tvs in tvsList:
            if DOS.compath(tvs['file'], tvsfile) : tvsid = tvs['tvshowid']; break
        if tvsid != -1:
            epsList = self._jGetEpisodes(tvsid)
            for eps in epsList:
                if DOS.compath(eps['file'], epsfile) : epsid = eps['episodeid']; break
            if epsid != -1:
                self._jRemoveEpisode(epsid)  
                return True
        return False
    
    def cleanList(self, fList, bg=False):
        progress = CProgress(len(fList), bg=addon.BGUPD if bg else True)
        progress.show(tl(TAG_DLG_SCLNDB))
      
        isMov = lambda file : DOS.compathStart(file, LIB.mov)
        isTVS = lambda file : DOS.compathStart(file, LIB.tvsf) and file.endswith(STRM)     
         
        movList = self._jGetMovies()
        tvsList = self._jGetTVSs() 
        lb = LIB.lib
        for file in fList:
            progress.step(file.replace(lb, Empty))
            if isMov(file) : self._removeMovie(file, movList); continue 
            if isTVS(file) : self._removeEpisode(DOS.gettail(file), file, tvsList)
        del progress 
        
        
    def osCleanTVS(self, bg=False):
        dirs, f = DOS.listdir(LIB.tvsf)
        progress = CProgress(len(dirs), bg=addon.BGUPD if bg else True)
        progress.show(tl(TAG_DLG_SREMEF))
        for tvsname in dirs:
            progress.step(tvsname)
            tvsfile  = DOS.join(LIB.tvsf, tvsname)
            d, files = DOS.listdir(tvsfile) 
            if not files: 
                self.removeTVS(tvsfile)
                DOS.remove(tvsfile)
        del progress
        GUI.refresh()
        
        