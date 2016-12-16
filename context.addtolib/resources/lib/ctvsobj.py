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
########## CTVS:

### Import modules ...
from ext import *


BGPROCESS = True

##### TVS Object ...
class TVS:
       
    def __init__(self, def_file_name, def_file_path=Empty, Import=False):
        ## Pack file separators ...
        self._sepLST = TAG_PAR_TVSPACK_LSEP
        self._sepSRC = TAG_PAR_TVSPACK_SSEP + NewLine
        self._sepFRC = TAG_PAR_TVSPACK_FSEP + NewLine
        self._sepEPS = TAG_PAR_TVSPACK_ESEP + NewLine
        self._sepPRT = TAG_PAR_TVSPACK_PSEP + NewLine
        
        self._sepVER = TAG_PAR_TVSPACK_VERSEP + NewLine
        self._PACK_VERS = TAG_PAR_TVSPACK_VERSION
        
        ## Define TVS ...
        self._define(def_file_name, def_file_path, Import)
        
    
    def _define(self, def_file_name, def_file_path, Import):
        ## Set default param ...
        self.clear()
        self._file_name  = def_file_name
        self.lib_path    = def_file_path
        self.lib_name    = DOS.getdir(def_file_path) if def_file_path and Import else Empty 
        self.lib_defname = DOS.getdir(def_file_path) if def_file_path else Empty
        
        ## Import data on initialize ...
        if Import : self.dimport()
        
    ### Clear TV Show ...
    def clear(self):
        self.lib_path    = Empty
        self.packed_data = Empty
        self._file_name  = Empty
        self._episodes   = []
        self._sources    = []
        self._folsources = []
        self._rawlist    = []
        self.seq         = 0
        self._sn_add     = 1
        self._inc_lock   = False
    
    ### Inside append ... 
    def _append(self, template, mark, var, appdict):
        if template not in [itm[mark] for itm in var]:
            var.append(appdict)
            return True
        return False

    ### Append ...            
    def append_episode(self, original_name, new_name, link, src_id, season=Empty):
        if self._append(original_name, 'original_name', self._episodes, {'original_name':original_name, 'new_name':new_name, 'link':link, 'src_id':src_id, 'season':season}):
            for src in self._sources:
                if src['src_id'] == src_id and not self._inc_lock : src['src_numb'] += self._sn_add; self._sn_add = 1; break
            if self.seq : self.seq += 1
            
    def update_season(self, src_link, src_season, src_numb, src_name):
        for src in self._sources : 
            if src_link == src['src_link']: 
                if inte(src_season) >= inte(src['src_season']):
                    src['src_season'] = src_season   
                    src['src_numb']   = src_numb 
                    src['src_name']   = src_name
                else:
                    self._inc_lock = True
              
    def append_fsource(self, fsrc_name, fsrc_link, fsrc_inum, fsrc_upd=True):
        self._append(fsrc_link, 'fsrc_link', self._folsources, {'fsrc_name':getUniqname(fsrc_name, [itm['fsrc_name'] for itm in self._folsources]), 'fsrc_link':fsrc_link, 'fsrc_inum':fsrc_inum, 'fsrc_upd':fsrc_upd})
    
    def append_source(self, src_name, src_link, src_season=Empty, src_upd=True, src_folmode=False, src_numb=0):
        src_id = self.get_src_id(src_link)
        if not self._append(src_link, 'src_link', self._sources, {'src_name':getUniqname(src_name, [itm['src_name'] for itm in self._sources]), 'src_link':src_link, 'src_id':src_id, 'src_upd':src_upd, 'src_season':src_season, 'src_numb':src_numb, 'src_folmode':src_folmode}):
            #self.update_season(src_link, src_season, src_numb, getUniqname(src_name, [itm['src_name'] for itm in self._sources]))
            self.update_season(src_link, src_season, src_numb, src_name)
        return src_id 
    
    def incSeq(self):
        self.seq += 1
    
    def incSN(self):
        self._sn_add += 1
    
    ### Exclude ...
    def _exclude(self, value, mark, var, skipvalue=Empty, skipmark=Empty):  
        return [itm for itm in var if value != itm[mark] or (skipvalue and itm[skipmark] != skipvalue)]
    
    def exclude_source(self, src_id):
        self._sources = self._exclude(src_id, 'src_id', self._sources)
    
    def exclude_episodes(self, src_id, season=Empty):
        self._episodes = self._exclude(src_id, 'src_id', self._episodes, season, 'season')
    
    def exclude_source_data(self, src_link, season=Empty):
        src_id = self.get_src_id(src_link)
        self.exclude_episodes(src_id, season=season)
        return src_id
    
    def exclude_folsource(self, frc_link):
        self._folsources = self._exclude(frc_link, 'fsrc_link', self._folsources)
    
    def remove_episode(self, src_id, eps_name):
        for eps in self._episodes:
             if eps['src_id'] == src_id and eps['new_name'] == eps_name : self._episodes.remove(eps)  
    
    ### Get ...  
    def get_multiseason_list(self, src_link):
        src_id = self.get_src_id(src_link)
        seasons = []
        for eps in self._episodes:
            if eps['src_id'] == src_id and eps['season'] not in seasons : seasons.append(eps['season'])
        return seasons    
      
    def get_eps_names_and_links(self):
        return {eps['new_name']: eps['link'] for eps in self._episodes}
    
    def get_eps_names_and_links_forsrc(self, src_link):
        src_id = self.get_src_id(src_link)
        return [eps['new_name'] for eps in self._episodes if eps['src_id'] == src_id], [eps['link'] for eps in self._episodes if eps['src_id'] == src_id] 
        
    def get_names_and_links(self):
        return [src['src_name'] for src in self._sources], [src['src_link'] for src in self._sources], \
               [frc['fsrc_name'] for frc in self._folsources], [frc['fsrc_link'] for frc in self._folsources]
        
    def get_src_id(self, src_link):
        for src in self._sources : 
            if src_link == src['src_link'] : return src['src_id']
        
        cidx = 1    
        seq  = [src['src_id'] for src in self._sources]
        for idx in range(len(seq)+1)[1:] : 
            if cidx not in seq : return cidx
            cidx = idx+1
        return cidx
          
    def get_src_name_by_link(self, link):
        for itm in self._sources:
            if itm['src_link'] == link : return itm['src_name']
        return Empty
        
    def get_eps_name_by_link(self, link):
        for itm in self._episodes:
            if itm['link'] == link : return itm['new_name']
        return Empty 
    
    def get_direct(self):
        return (self._episodes, self._folsources, self._sources)
    
    def get_eps_count(self):
        return len(self._episodes)
    
    def get_upd(self):
        updListS = [src['src_name'] for src in self._sources if src['src_upd']]
        updListF = [frc['fsrc_name'] for frc in self._folsources if frc['fsrc_upd']]
        return updListF, updListS
    
    def get_frc_names_and_links(self):
        return ([frc['fsrc_name'] for frc in self._folsources], [frc['fsrc_link'] for frc in self._folsources])
    
    def get_scr_numb_and_season(self, link):
        for itm in self._sources:
            if itm['src_link'] == link : return itm['src_season'], itm['src_numb']
        return Empty, 0
    
    def get_scr_numb_season_mode(self, link):
        for itm in self._sources:
            if itm['src_link'] == link : return itm['src_season'], itm['src_numb'], itm['src_folmode'] 
        return Empty, 0, False
        
    def get_raw_link_list(self):
        return [itm[0] for itm in self._rawlist]
    
    def get_raw_eps(self):
        return [itm[1] for itm in self._rawlist]
    
    ### Add target TVS to current TVS ...
    def join_tvs(self, TVS):
        srcId = dict()
        epsExt, frcExt, srcExt = TVS.get_direct()
        for src in srcExt:
            scrOldId = src['src_id']
            scrNewId = self.append_source(src['src_name'], src['src_link'], src['src_season'], src['src_upd'])
            srcId.update({scrOldId: scrNewId})
        
        for frc in frcExt:
            self.append_fsource(frc['fsrc_name'], frc['fsrc_link'], frc['fsrc_inum'], frc['fsrc_upd'])
            
        for eps in epsExt:
            self.append_episode(eps['original_name'], eps['new_name'], eps['link'], srcId[eps['src_id']])
    
    ### Rename ... 
    def rensource(self, srcOldName, srcNewName):
        for src in self._sources:
            if src['src_name'] == srcOldName : src['src_name'] = srcNewName   
    
    def renfsource(self, frcOldName, frcNewName):
        for frc in self._folsources:
            if frc['fsrc_name'] == frcOldName : frc['fsrc_name'] = frcNewName
    
    def ren_eps(self, src_id, oldname, newname):
        for itm in self._episodes:
            if itm['src_id'] == src_id and itm['new_name'] == oldname : itm['new_name'] = newname; break   
    
    ### Set updateble flags ...
    def set_upd(self, fcrNames, scrNames):
        for src in self._sources:
            src['src_upd'] = True if src['src_name'] in scrNames else False
            
        for frc in self._folsources:
            frc['fsrc_upd'] = True if frc['fsrc_name'] in fcrNames else False 
    
    def reset_inum(self, frcLink, frcInum):
        for frc in self._folsources:
            if frc['fsrc_link'] == frcLink : frc['fsrc_inum'] = frcInum; break    
    
    ### Import and export tvs.pack 
    def dimport(self):
        self.packed_data = DOS.file(self._file_name, self.lib_path, fType=FRead) 
        if self.packed_data == -1: self.packed_data = Empty
        self.packed_data = self.packed_data.replace(CR, Empty)
        self._unpack_by_version()
    
    def dexport(self):
        self._pack()
        self._inc_lock = False
        DOS.file(self._file_name, self.lib_path, self.packed_data, FWrite)
    
    ### Pack and unpack TV Show data ...    
    def _pack(self):
        lst = [self._sepLST.join([itm['src_name'], itm['src_link'], str(itm['src_id']), str(itm['src_upd']), itm['src_season'], str(itm['src_numb']), str(itm['src_folmode'])]) for itm in self._sources]
        src =  self._sepSRC.join(lst)
        
        lst = [self._sepLST.join([itm['fsrc_name'], itm['fsrc_link'], str(itm['fsrc_inum']), str(itm['fsrc_upd'])]) for itm in self._folsources]
        frc =  self._sepFRC.join(lst)
        
        lst = [self._sepLST.join([itm['original_name'], itm['new_name'], itm['link'], str(itm['src_id']), str(itm['season'])]) for itm in self._episodes]
        eps =  self._sepEPS.join(lst)
        
        self.packed_data = self._sepVER.join([self._PACK_VERS, self._sepPRT.join([src, frc, eps, str(self.seq)])]) 
    
    ### Unpack by version ...
    def _unpack_by_version (self):
        try:
            pVers, pData = (self.packed_data.split(self._sepVER))
            if pVers == '10013' : self._unpack10013(pData) 
            if pVers == '10015' : self._unpack10015(pData)
        except: 
            self._unpack()     

    ### Unpacker versions ...
    def _unpack10015(self, pData):
        if not pData: return
        self.packed_data = pData
        src, frc, eps, seq       = (self.packed_data.split(self._sepPRT)) 
        if src: self._sources    = [{'src_name':itm1, 'src_link':itm2, 'src_id':int(itm3), 'src_upd':sbool(itm4), 'src_season':itm5, 'src_numb':int(itm6), 'src_folmode':sbool(itm7)} for itm in src.split(self._sepSRC) for itm1, itm2, itm3, itm4, itm5, itm6, itm7 in [itm.split(self._sepLST)]]
        if frc: self._folsources = [{'fsrc_name':itm1, 'fsrc_link':itm2, 'fsrc_inum':int(itm3), 'fsrc_upd':sbool(itm4)} for itm in frc.split(self._sepFRC) for itm1, itm2, itm3, itm4 in [itm.split(self._sepLST)]]
        if eps: self._episodes   = [{'original_name':itm1, 'new_name':itm2, 'link':itm3, 'src_id':int(itm4), 'season':itm5} for itm in eps.split(self._sepEPS) for itm1, itm2, itm3, itm4, itm5 in [itm.split(self._sepLST)]]
        self.seq                 = int(seq)
        self.packed_data = Empty
    
    def _unpack10013(self, pData):
        if not pData: return
        self.packed_data = pData
        src, frc, eps, seq       = (self.packed_data.split(self._sepPRT)) 
        if src: self._sources    = [{'src_name':itm1, 'src_link':itm2, 'src_id':int(itm3), 'src_upd':sbool(itm4), 'src_season':itm5, 'src_numb':int(itm6), 'src_folmode':sbool(itm7)} for itm in src.split(self._sepSRC) for itm1, itm2, itm3, itm4, itm5, itm6, itm7 in [itm.split(self._sepLST)]]
        if frc: self._folsources = [{'fsrc_name':itm1, 'fsrc_link':itm2, 'fsrc_inum':int(itm3), 'fsrc_upd':sbool(itm4)} for itm in frc.split(self._sepFRC) for itm1, itm2, itm3, itm4 in [itm.split(self._sepLST)]]
        if eps: self._episodes   = [{'original_name':itm1, 'new_name':itm2, 'link':itm3, 'src_id':int(itm4), 'season':Empty} for itm in eps.split(self._sepEPS) for itm1, itm2, itm3, itm4 in [itm.split(self._sepLST)]]
        self.seq                 = int(seq)
        self.packed_data = Empty
        
    def _unpack(self):
        if not self.packed_data: return
        src, frc, eps, seq       = (self.packed_data.split(self._sepPRT)) 
        if src: self._sources    = [{'src_name':itm1, 'src_link':itm2, 'src_id':int(itm3), 'src_upd':sbool(itm4), 'src_season':itm5, 'src_numb':int(itm6), 'src_folmode':False} for itm in src.split(self._sepSRC) for itm1, itm2, itm3, itm4, itm5, itm6 in [itm.split(self._sepLST)]]
        if frc: self._folsources = [{'fsrc_name':itm1, 'fsrc_link':itm2, 'fsrc_inum':int(itm3), 'fsrc_upd':sbool(itm4)} for itm in frc.split(self._sepFRC) for itm1, itm2, itm3, itm4 in [itm.split(self._sepLST)]]
        if eps: self._episodes   = [{'original_name':itm1, 'new_name':itm2, 'link':itm3, 'src_id':int(itm4), 'season':Empty} for itm in eps.split(self._sepEPS) for itm1, itm2, itm3, itm4 in [itm.split(self._sepLST)]]
        self.seq                 = int(seq)
        self.packed_data = Empty
    
    ### Get source list with new episodes ...
    def check_new_eps(self, message=Empty, globp=None, globmsg=Empty):
        if globp is None : 
            progress = CProgress(len(self._sources)+len(self._folsources), bg=BGPROCESS)
            progress.show(message)
            stepv = 1
        else             : 
            progress = globp 
            slen = len(self._sources)+len(self._folsources)
            stepv = 100.0 / slen if slen else 100
        
        self.os_getraw()
        
        srcListNames  = []
        srcListLinks  = []
        rawlinklist   = self.get_raw_link_list()
        for src in self._sources:
            progress.step(src['src_name'] if not globmsg else globmsg, stepv)
            if not src['src_upd']: continue
            if src['src_link'] in rawlinklist: 
                ld = DOS.listdir(src['src_link'])
                srcItmNum = len(ld[0] + ld[1])
                locEpsNum = len([itm[1] for itm in self._rawlist if itm[0] == src['src_link']])
            else:
                srcItmNum = len(DOS.listdir(src['src_link'])[1])
                locEpsNum = len([eps['original_name'] for eps in self._episodes if eps['src_id'] == src['src_id']])
                
            if srcItmNum > locEpsNum and srcItmNum != 0: 
                srcListNames.append(src['src_name'])
                srcListLinks.append(src['src_link'])
        
        frcListNames  = []
        frcListLinks  = []
        for frc in self._folsources:
            progress.step(frc['fsrc_name'] if not globmsg else globmsg, stepv)
            if not frc['fsrc_upd']: continue
            frcItmNum = len(DOS.listdir(frc['fsrc_link'])[1])
            folNum    = frc['fsrc_inum']
            if frcItmNum > folNum and frcItmNum != 0: 
                frcListNames.append(frc['fsrc_name'])
                frcListLinks.append(frc['fsrc_link'])
        
        if globp is None : del progress
                
        return srcListNames, srcListLinks, frcListNames, frcListLinks  
         
    
    ### OS ...
    def os_clear(self):
        DOS.remove(self.lib_path, False)
    
    def os_delete(self):
        DOS.remove(self.lib_path)
    
    def os_rename(self, newName):
        self.lib_name = newName
        newPathName = DOS.join(DOS.gettail(self.lib_path), newName)
        DOS.rename(self.lib_path, newPathName)
        self.lib_path = newPathName
    
    def os_exclude_src(self, link, dexport=True, season=Empty, remove_src=True):
        src_id = self.get_src_id(link)
        for eps in self._episodes:
            if season and season != eps['season'] : continue  
            if eps['src_id'] == src_id : DOS.delf(DOS.join(self.lib_path, eps['new_name']+STRM))     
        self.exclude_source_data(link, season=season)
        if remove_src : self.exclude_source(src_id)
        if dexport : self.dexport()
    
    def os_exclude_src_rest(self, src_link, prefix):
        self.os_clear()
        self.exclude_source(self.exclude_source_data(src_link))
        self.os_create(prefix)
        
    def os_create(self, prefix, overwrite=False):
        DOS.mkdirs(self.lib_path)
        lEpisodes = self.get_eps_names_and_links()
        for eps in lEpisodes: self._os_create_strm(eps, self.lib_path, lEpisodes[eps], overwrite, prefix)
        self.dexport()
        
    def _os_create_strm(self, fName, fPath, Link, Overwrite, prefix):
        svLink = prefix % (DOS.join(DOS.getdir(fPath), fName + STRM)) + Link if prefix else Link      
        DOS.file(fName + STRM, fPath, svLink, fRew = Overwrite)
        
    def os_addraw(self, link, itmlist):
        rawepslist = [itm[1] for itm in self._rawlist] 
        for itm in itmlist : 
            if itm not in rawepslist : self._rawlist.append([link, itm])
        
        lined   = []
        for itm in self._rawlist : lined.append(itm[0] + self._sepLST + itm[1])
        rawdata = self._sepEPS.join(lined)
        DOS.file(TAG_PAR_TVSRAWFILE, self.lib_path, rawdata, fRew = True)
        del rawepslist, lined 
        
    def os_getraw (self):
        unpraw = DOS.file(TAG_PAR_TVSRAWFILE, self.lib_path, fType=FRead)
        if unpraw == -1 : return 
        lined  = unpraw.split(self._sepEPS)
        self._rawlist = []
        for itm in lined : self._rawlist.append(itm.split(self._sepLST)) 
        
    def os_rename_eps(self, src_id, newname, oldname, prefix):
        #DOS.delf(DOS.join(self.lib_path, oldname) + STRM)
        #self._os_create_strm(newname, self.lib_path, link, True, prefix)
        DOS.rename(DOS.join(self.lib_path, oldname) + STRM, DOS.join(self.lib_path, newname) + STRM)
        self.ren_eps(src_id, oldname, newname)
        self.dexport()
        
    def os_remove_eps(self, src_id, eps_name):
        DOS.delf(DOS.join(self.lib_path, eps_name) + STRM)
        self.remove_episode(src_id, eps_name)
        self.dexport()  
        

class CLinkTable:
    
    def __init__(self, fName, fPath, load=True):
        self._sepLST = TAG_PAR_TVSPACK_LSEP
        self._sepSRC = TAG_PAR_TVSPACK_SSEP + NewLine
        
        self._unp_table = Empty
        self._table     = []
        
        self._file_name = fName
        self._file_path = fPath
        
        if load : self._load_table()
    
    def _load_table(self):
        self._unp_table = DOS.file(self._file_name, self._file_path, fType=FRead)
        if self._unp_table == -1: self._unp_table = Empty
        self._unp_table = self._unp_table.replace(CR, Empty)
        self._unpack()
    
    def _unpack(self):
        self._table = []
        if self._unp_table: self._table = [{'stl_path':itm1, 'stl_link':itm2} for itm in self._unp_table.split(self._sepSRC) for itm1, itm2 in [itm.split(self._sepLST)]]
        self._unp_table = Empty
    
    def _pack(self):
        src = [self._sepLST.join([itm['stl_path'], itm['stl_link']]) for itm in self._table]
        self._unp_table = self._sepSRC.join(src)
    
    def _save_table(self):
        self._pack()
        DOS.file(self._file_name, self._file_path, self._unp_table, fRew = True)
        
    def find(self, link):
        if not link : return Empty
        for itm in self._table:
            if itm['stl_link'] == link: return itm['stl_path']
        return Empty
    
    def add(self, path, link, save=True):
        self._add(path, path, False)
        self._add(path, link, True)
    
    def _add(self, path, link, save):
        if link not in [itm['stl_link'] for itm in self._table]:
            self._table.append({'stl_path': path, 'stl_link': link})
            if save: self._save_table()
    
    def remove(self, link, save=True):
        for itm in self._table:
            if itm['stl_link'] == link: 
                self._table.remove(itm)
                if save: self._save_table()
                break    

    def exclude(self, path, save=True):
        self._table = [itm for itm in self._table if itm['stl_path'] != path]
        if save: self._save_table()
    
    def chpath(self, oldPath, newPath, save=True):
        self._chlink(oldPath, newPath, False)
        self._chpath(oldPath, newPath, True)
    
    def _chpath(self, oldPath, newPath, save=True):
        for itm in self._table:
            if itm['stl_path'] == oldPath: itm['stl_path'] = newPath
        if save: self._save_table()
    
    def _chlink(self, oldLink, newLink, save=True):
        for itm in self._table:
            if itm['stl_link'] == oldLink: itm['stl_link'] = newLink
        if save: self._save_table()
    
    def save(self):
        self._save_table()
    
    def load(self):
        self._load_table()
    
    