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
########## Dropbox Sync:

### Import modules ...
#import resources.lib.dropboxapi as dropboxapi
from dropboxapi import *
from random  import randrange


### Sync types constants...
stypeNoSync       = 0
stypeUpload       = 1
stypeDownload     = 2
stypeUploadFull   = 11
stypeDownloadFull = 22

### DBX sync...
class dbxSync():
    
    def __init__(self):
        limit_time               = addon.SYLIMITTIME
        limit_count              = addon.SYLIMITCOUNT
        
        self.dbx                 = dropboxConnect(limit_time, limit_count, self.raise_report)
        
        self.last_removed        = Empty
        self.last_added          = Empty
        
        self.vdbLockFile         = TAG_PAR_DROPBOX_LF
        self.vdbLockCode         = TAG_PAR_DROPBOX_LCODE
        
        self.vdbSyncFile         = TAG_PAR_DROPBOX_SYNC_FILE
        self.vdbSyncTmpFile      = TAG_PAR_DROPBOX_SYNC_T_FILE
        
        self.vdbLilDir           = TAG_PAR_LIB_FOLDER
        self.vdbSyncDBXDir       = self.vdbLilDir
        self.vdbSyncDBXTmpDir    = TAG_PAR_DROPBOX_SYNC_T_DIR
        
        #self.vdbSyncLoacalPrDir  = addon.profile
        self.vdbSyncLoacalPrDir  = LIB.libpath
        #self.vdbSyncLoacalDir    = LIB.lib
        self.vdbSyncLoacalDir    = DOS.join(self.vdbSyncLoacalPrDir, self.vdbLilDir)
        self.vdbSyncLocalTmpDir  = DOS.join(self.vdbSyncLoacalPrDir, TAG_PAR_DROPBOX_SYNC_T_DIR)
        
        self.vdbSyncDBXFile      = self.dbx.join(self.vdbSyncDBXDir, self.vdbSyncFile)
        self.vdbSyncLocalFile    = DOS.join(self.vdbSyncLoacalDir, self.vdbSyncFile)
        
        #self.vdbSyncDBXTmpFile   = join(self.vdbSyncDBXTmpDir, self.vdbSyncFile)
        self.vdbSyncLocalTmpFile = DOS.join(self.vdbSyncLoacalPrDir, self.vdbSyncTmpFile)
        
        self.vdbTemplate         = TAG_PAR_DROPBOX_TMPL
        
        self.libImgFile          = TAG_PAR_DROPBOX_LI_FILE
        self.libImgTmpFile       = TAG_PAR_DROPBOX_LI_T_FILE
        self.libImgSyncFile      = TAG_PAR_DROPBOX_LI_S_FILE
        
        self.separatorItm        = TAG_PAR_DROPBOX_LISEPTM
        self.separatorRec        = TAG_PAR_DROPBOX_LISEPREC
        
        self.vbdLibImgFileLocal    = DOS.join(self.vdbSyncLoacalDir, self.libImgFile)
        self.vbdLibImgTmpFileLocal = DOS.join(self.vdbSyncLoacalDir, self.libImgTmpFile)
        self.vbdLibImgFileDBX      = self.dbx.join(self.vdbSyncDBXDir, self.libImgFile) 
        self.vbdLibImgSyncFile     = DOS.join(self.vdbSyncLoacalDir, self.libImgSyncFile)
                        
        self.vdbCorruptionFile     = TAG_PAR_DROPBOX_CORR_FILE
        self.adnUID_file           = TAG_PAR_DROPBOX_UID_FILE
        self.vdbCorrFileLocal      = DOS.join(self.vdbSyncLoacalPrDir, self.vdbCorruptionFile)
        #self.vdbCorrFileDBX        = self.dbx.join(self.vdbSyncDBXDir, self.vdbCorruptionFile)
        self.vdbCorrFileDBX        = self.vdbCorruptionFile
        self.addonUID              = self.getAddonUID()
        
        ## WatchSync ...
        
        self.cmd_mov      = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "properties": ["file", "thumbnail", "title", "year", "rating", "genre", "plot", "country", "director", "originaltitle", "writer", "studio", "mpaa", "votes", "cast", "art"] },  "id": 1}'
        self.cmd_tvs_tvs  = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": { "properties": ["file", "genre", "year", "studio", "mpaa"] },  "id": 1}'
        self.cmd_tvs_eps  = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": { "properties": ["season", "plot", "file", "rating", "votes", "episode", "showtitle", "writer", "originaltitle", "director", "firstaired", "art", "cast"], "tvshowid":%s },  "id": 1}'
        
        self.cmd_mov_w    = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": { "properties": ["playcount", "resume"], "movieid":%s }, "id": 1}'
        self.cmd_tvs_w    = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": { "properties": ["playcount", "resume"], "episodeid": %s }, "id": 1}'
        
        self.cmd_set_mov  = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid":%s, "resume": {"position":%s, "total":%s} }, "id": 1}'
        self.cmd_set_tvs  = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid":%s, "resume": {"position":%s, "total":%s} }, "id": 1}'
        
        self.cmd_set_movw = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid":%s, "playcount": %s }, "id": 1}'
        self.cmd_set_tvsw = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid":%s, "playcount": %s }, "id": 1}'
        
        #self.moviesList   = []
        #self.tvshowsList  = []
        
        self.inffName     = TAG_PAR_WS_FILE
        self.inffNameTmp  = TAG_PAR_WS_TMP_FILE
        
        self.infFPath     = DOS.join(self.vdbSyncLoacalDir, self.inffName) 
        self.infFPathTmp  = DOS.join(self.vdbSyncLoacalPrDir, self.inffNameTmp)
        self.infDBX       = self.dbx.join(self.vdbSyncDBXDir, self.inffName)
        
        self.separatorWS1 = TAG_PAR_TVSPACK_LSEP
        self.separatorWS2 = TAG_PAR_TVSPACK_SSEP
        self.separatorWS3 = TAG_PAR_TVSPACK_PSEP
        
        ### Progress ...
        self.progress     = None
        self.prog_st_time = 0
        self.prog_st_go   = 0
        self.prog_step    = 0
        self.prog_visible = False
        self.progress_show_always = False
        self.prog_st_scale = 1000
        self.prog_hide_sec = 10
        self._last_msg     = Empty 
        
        
        self.prog_msgs = tl(TAG_DLG_DBXPRGSMSGS).split(TAG_PAR_DROPBOX_MSGSEP)
        self.dbx.prog_msgs = [self.prog_msgs[13], self.prog_msgs[14], self.prog_msgs[15], self.prog_msgs[16], self.prog_msgs[17], self.prog_msgs[18]]  
        
    
    
    def _setProgress(self):
        self.progress = CProgress(self.prog_st_scale, bg=addon.BGUPD if self.progress_show_always else True)
        self.prog_st_time = time.time()
        self.prog_visible = False
        self.dbx.progstepfnc = self._progressStep 
    
    
    def _delProgress(self):
        if self.progress is not None : del self.progress
        self.progress     = None
        self.prog_st_time = 0
        self.prog_st_go   = 0
        self.prog_step    = 0
        self.prog_visible = False
        self._last_msg    = Empty
        self.progress_show_always = False
        self.dbx.progstepfnc = None  
    
    
    def _calcProgressSteps(self, stepscount, reserve=50):
        rest = self.prog_st_scale - self.prog_st_go - reserve
        #self.prog_step = float(rest) / float(stepscount+1) if stepscount else rest
        self.prog_step = float(rest) / float(stepscount+1)
        self._progressStep()   
    
    
    def _progressStep(self, msg=Empty, blank=False):
        if self.progress is None : return
        if msg : self._last_msg = msg
        #if step : self.prog_step = step
        if not self.prog_visible:
            nowtime = time.time()
            if nowtime - self.prog_st_time > self.prog_hide_sec or self.progress_show_always: 
                self.prog_visible = True
                #if not addon.HIDEBCKPRGS : progress.show(tla(TAG_TTL_BACKUP))
                self.progress.show(self.prog_msgs[0])
                if not self.progress_show_always : self.progress.step(self._last_msg, self.prog_st_go)
            #else : return 
        step = self.prog_step if not blank else 0  
        self.progress.step(msg, step)
        self.prog_st_go += step
    
    
    def _nosyncProgressSteps(self):
        self._calcProgressSteps(0)
        self._calcProgressSteps(2,0)
          
    
    def _connect(self): 
        self._progressStep(self.prog_msgs[1])
        return self.dbx.Connect() 
    
    
    def _disconnect(self, stayLocked=False):
        self._progressStep(self.prog_msgs[2])
        if not stayLocked : self._syncLock(False)
        self.dbx.Disconnect()
        self._delProgress()
    
    
    def authorize(self, inboxWnd):
        return self.dbx.authorize_dropbox(inboxWnd)
        
    
    def disable(self):
        self.dbx.disableAToken()
    
    
    def unLock(self, resetCorr=False):
        if not self._connect() : return False
        if resetCorr : self._setCorruptionMode(False)
        self._disconnect()
        return True
    
    
    def justLock(self):
        result = 0 
        if not self._connect()  : result = -1    
        if not self._syncLock() : result = -2
        self._disconnect(stayLocked=True)
        return result 
    
    
    def sync(self, upload=False, download=False): 
        
        self._setProgress()
        
        if not self._connect()  : return -1    
        if not self._syncLock() : self._disconnect(stayLocked=True); return -2 
        
        if upload: 
            self.vdbUploadFull()
            self._disconnect()
            return stypeUploadFull
            
        if download: 
            self.vdbDownloadFull()
            self._disconnect()
            return stypeDownloadFull
            
        syncMode = self._getSyncMode()
        if   syncMode == stypeUpload       : self._vdbUpload()
        elif syncMode == stypeDownload     : self._vdbDownload()
        elif syncMode == stypeUploadFull   : self.vdbUploadFull()
        elif syncMode == stypeDownloadFull : self.vdbDownloadFull()
        else : self._nosyncProgressSteps()
        self._disconnect()
        return syncMode  
    
    
    def _getSyncMode(self):
        self._progressStep(self.prog_msgs[3])
        ## Delete local sync tmp file ...
        DOS.delf(self.vdbSyncLocalTmpFile)
        ## Get DBX sync file as local tmp sync file ...
        self.dbx.get_file(self.vdbSyncDBXFile, self.vdbSyncLocalTmpFile)
        ## Read info from local tmp sync file ...
        syncInfoDBX = DOS.file(self.vdbSyncTmpFile, self.vdbSyncLoacalPrDir, fType=FRead)
        ## Set syncMode to Upload if not exists ... 
        if syncInfoDBX  == -1  : return stypeUploadFull 
        ## Delete local sync tmp file ...
        DOS.delf(self.vdbSyncLocalTmpFile)
        ## Read info from local sync file ...
        syncInfoLocal = DOS.file(self.vdbSyncFile, self.vdbSyncLoacalDir, fType=FRead)
        ## Set syncMode to Download if not exists ...
        if syncInfoLocal == -1 : return stypeDownloadFull
        ## Comp Sync files ...
        cmpResult = self._compSyncFiles(syncInfoDBX, syncInfoLocal)
        ## Set syncMode to NoSync if files are same ...
        if cmpResult == 0 : return stypeNoSync
        ## Set syncMode to Download if DBX date later (else Upload) ...
        return stypeDownload if cmpResult == 1 else stypeUpload
        
    
    def vdbUploadFull(self):
        self._progressStep(self.prog_msgs[4])
        ## Calc progress steps ...
        self._calcProgressSteps(len(self.libScan())+2)
        ## Delete DBX tmp directory (if exists) ...
        self.dbx.delete(self.vdbSyncDBXTmpDir) 
        ## Send local directory to DBX as tmp directory  ...
        self.dbx.send_dir(self.vdbSyncLoacalDir, self.vdbSyncDBXTmpDir, template=self.vdbTemplate)
        ## If all is Ok ...
        ## Delete DBX directory ...
        self.dbx.delete(self.vdbSyncDBXDir)
        ## Rename DBX tmp directory (normalize)...
        self.dbx.rename(self.vdbSyncDBXTmpDir, self.vdbSyncDBXDir)
        ## Create libImg local file ....
        self.saveLibImg()
        ## Create libimg.sync ... 
        self.createLibImgSync(new=False)
        ## Calc progress final steps (8) ...
        self._calcProgressSteps(8, 0)
        ## Send libImg file to DBX ...
        self._sendLibImgFile()
        ## Create sync file ...
        self.createSyncFile()
        ## Send sync file to DBX ...
        self._sendSyncFile()
    
    
    def vdbDownloadFull(self):
        self._progressStep(self.prog_msgs[5])
        self.last_removed = Empty
        self.last_added   = Empty
        ## Calc progress steps ...
        self._calcProgressSteps(len(self.dbx.walkFiles(self.vdbSyncDBXDir, self.vdbTemplate)))
        ## Delete local tmp directory (if exists) ...
        DOS.rmdir(self.vdbSyncLocalTmpDir)
        ## Get DBX directory (download to local tmp directory) ...
        self.dbx.get_dir(self.vdbSyncDBXDir, self.vdbSyncLocalTmpDir, template=self.vdbTemplate)
        ## If all is Ok ...
        ## Delete local directory ...
        DOS.remove(self.vdbSyncLoacalDir, maskfn=self._chk_tmpl)
        ## Move local tmp directory (normalize)...
        DOS.copyfls(self.vdbSyncLocalTmpDir, self.vdbSyncLoacalDir, move=True)
        ## Calc progress final steps (6) ...
        self._calcProgressSteps(6, 0)
        ## Get libImg file from DBX ...
        self._getLibImgFile()
        ## Get sync file ...
        self._getSyncFile()
        ## Create libimg.sync ... 
        self.createLibImgSync()
    
    
    def _vdbGetImgChanges(self):
        self._progressStep(self.prog_msgs[6])
        ## Delete local libImg tmp file ...
        DOS.delf(self.vbdLibImgTmpFileLocal)
        ## Get DBX libImg file as tmp ...
        self.dbx.get_file(self.vbdLibImgFileDBX, self.vbdLibImgTmpFileLocal)
        ## Get DBX libImg from downloaded file...
        libImgDBX = self.loadLibImg(self.vbdLibImgTmpFileLocal)
        ## Delete tmp DBX libImg file ...
        DOS.delf(self.vbdLibImgTmpFileLocal)
        ## Create libImg local file ....
        self.getLocalChanges()
        ## Get local libImg ...
        libImgLocal = self.loadLibImg()
        ## Return result ...
        return self.cmpImgs(libImgLocal, libImgDBX)
        
    
    def _convertToDBX(self, flist): 
        return [self.dbx.convertToDBX(fl, self.vdbSyncLoacalDir) for fl in flist]
    
    
    def _vdbDownload(self):
        ## Delete local tmp directory (if exists) ...
        DOS.rmdir(self.vdbSyncLocalTmpDir)
        ## Get libImg's changes ...
        removed, added = self._vdbGetImgChanges()
        self.last_removed = removed
        self.last_added   = added 
        ## Convert to DBX paths ...
        addedDBX = [self.dbx.join(self.vdbSyncDBXDir, remf) for remf in self._convertToDBX(added)] if added else [] 
        ## Calc progress steps ...
        self._calcProgressSteps(len(added))
        ## Download added files to tmp dir...
        self.dbx.get_filesList(addedDBX, self.vdbSyncDBXDir, self.vdbSyncLocalTmpDir)
        DOS.mkdirs(self.vdbSyncLocalTmpDir)
        ## Remove local LIB files ... 
        DOS.delFilesList(removed) 
        ## Move local tmp files (normalize)...
        DOS.copyfls(self.vdbSyncLocalTmpDir, self.vdbSyncLoacalDir, move=True)
        ## Calc progress final steps (6) ...
        self._calcProgressSteps(6, 0)
        ## Get libImg file from DBX ...
        self._getLibImgFile()
        ## Get sync file ...
        self._getSyncFile()
        ## Create libimg.sync ...
        self.createLibImgSync()

    
    # def _vdbUpload(self):
    #     ## Delete DBX tmp directory (if exists) ...
    #     self.dbx.delete(self.vdbSyncDBXTmpDir) 
    #     ## Get libImg's changes ...
    #     added, removed = self._vdbGetImgChanges()
    #     ## Calc progress steps ...
    #     self._calcProgressSteps(len(added)*3+self.getDirsCount(added)+len(removed)+1)
    #     ## Upload added files ...
    #     self.dbx.send_filesList(added, self.vdbSyncLoacalDir, self.vdbSyncDBXTmpDir)
    #     ## Convert to DBX paths ...
    #     removedDBX = [self.dbx.join(self.vdbSyncDBXDir, remf) for remf in self._convertToDBX(removed)] if removed else [] 
    #     ## Remove DBX LIB files ...
    #     self.dbx.delete_filesList(removedDBX) 
    #     ## Move DBX tmp files (normalize) ...
    #     self.dbx.copy_dir(self.vdbSyncDBXTmpDir, self.vdbSyncDBXDir, move=True)
    #     ## Calc progress final steps (8) ...
    #     self._calcProgressSteps(8, 0)
    #     ## Send libImg file to DBX ...
    #     self._sendLibImgFile()
    #     ## Create sync file ...
    #     self.createSyncFile()
    #     ## Send sync file to DBX ...
    #     self._sendSyncFile()
    
    
    def _vdbUpload(self):
        ## Delete DBX tmp directory (if exists) ...
        self.dbx.delete(self.vdbSyncDBXTmpDir) 
        ## Get libImg's changes ...
        added, removed = self._vdbGetImgChanges()
        ## Set DBX database corruption mode ...
        self._setCorruptionMode()
        ## Calc progress steps ...
        self._calcProgressSteps(len(added)+len(removed))
        ## Convert to DBX paths ...
        removedDBX = [self.dbx.join(self.vdbSyncDBXDir, remf) for remf in self._convertToDBX(removed)] if removed else [] 
        ## Remove DBX LIB files ...
        self.dbx.delete_filesList(removedDBX) 
        ## Upload added files ...
        self.dbx.send_filesList(added, self.vdbSyncLoacalDir, self.vdbSyncDBXDir)
        ## Calc progress final steps (9) ...
        self._calcProgressSteps(9, 0)
        ## Reset DBX database corruption mode ...
        self._setCorruptionMode(False)
        ## Send libImg file to DBX ...
        self._sendLibImgFile()
        ## Create sync file ...
        self.createSyncFile()
        ## Send sync file to DBX ...
        self._sendSyncFile()
    
    
    def _setCorruptionMode(self, setc=True):
        #self._progressStep(self.prog_msgs[19])
        if not setc: 
            self.dbx.delete(self.vdbCorrFileDBX)
        else:
            DOS.file2(self.vdbCorrFileLocal, self.addonUID, fRew=True)
            self.dbx.send_file(self.vdbCorrFileLocal, self.vdbCorrFileDBX)
            DOS.delf(self.vdbCorrFileLocal)
    
    
    def getCorrupted(self):
        if not self._connect() : return -1
        self.dbx.get_file(self.vdbCorrFileDBX, self.vdbCorrFileLocal)
        corr = DOS.file2(self.vdbCorrFileLocal, fType=FRead)
        DOS.delf(self.vdbCorrFileLocal)
        if corr == -1 : corr = Empty
        self._disconnect()
        return corr
         
        
    def createSyncFile(self):
        ## Create sync information ...
        syncInfo = str(time.time())
        ## Create Sync file (local, rewrite) ...
        DOS.file(self.vdbSyncFile, self.vdbSyncLoacalDir, syncInfo, fType=FWrite, fRew = True)
    
    
    def isAuthorize(self):
        return self.dbx.isAToken()
    
    def isLock(self):
        return self.dbx.exists(self.vdbLockFile)
    
    def _syncLock(self, lock=True):  
        path = DOS.join(self.vdbSyncLoacalPrDir, self.vdbLockFile)
        if lock == True:
            if self.isLock() : return False
            DOS.file2(path, self.vdbLockCode, fType=FWrite, fRew = True)
            self.dbx.send_file(path, self.vdbLockFile)
            DOS.delf(path)
        else : self.dbx.delete(self.vdbLockFile)
        return True 
            
    
    def _sendSyncFile(self):
        self._progressStep(self.prog_msgs[7])
        ## Remove Sync file from DBX directoty ...
        self.dbx.delete(self.vdbSyncDBXFile)
        ## Send Sync file to DBX directoty ...
        self.dbx.send_file(self.vdbSyncLocalFile, self.vdbSyncDBXFile)
    
    
    def _getSyncFile(self):
        self._progressStep(self.prog_msgs[8])
        DOS.delf(self.vdbSyncLocalFile)
        self.dbx.get_file(self.vdbSyncDBXFile, self.vdbSyncLocalFile)
    
    
    def _sendLibImgFile(self):
        self._progressStep(self.prog_msgs[9])
        ## Remove libImgFile file from DBX directoty ...
        self.dbx.delete(self.vbdLibImgFileDBX)
        ## Send libImgFile to DBX ... 
        self.dbx.send_file(self.vbdLibImgFileLocal, self.vbdLibImgFileDBX)
    
    def _getLibImgFile(self):
        self._progressStep(self.prog_msgs[10])
        DOS.delf(self.vbdLibImgFileLocal)
        self.dbx.get_file(self.vbdLibImgFileDBX, self.vbdLibImgFileLocal)
    
    
    def _compSyncFiles(self, sFile1, sFile2):
        if   float(sFile1) > float(sFile2) : return 1
        elif float(sFile1) < float(sFile2) : return 2
        else                               : return 0


    ### Check tmpl function ...
    def _chk_tmpl(self, path, fls):
        for tmpl in self.vdbTemplate:
            if fls.find(tmpl) != -1 : return True
        return False 
         
    
    ### libImg functions ...
    
    def libScan(self):
        return [fls.replace(self.vdbSyncLoacalDir, Empty) for fls in DOS.scanWalk(self.vdbSyncLoacalDir) if self._chk_tmpl(Empty, fls)]
    
    def _addTime(self, libList):
        return [self.separatorItm.join([fls, getdtcode(DOS.stat(DOS.join(LIB.lib, fls)).st_mtime())]) for fls in libList]
    
    def saveLibImg(self, path=Empty, img=Empty):
        if not path : path = self.vbdLibImgFileLocal
        if not img  : img  = self._addTime(self.libScan())
        libImgPack = self.separatorRec.join(img)
        DOS.file2(path, libImgPack, fRew=True)
    
    def loadLibImg(self, path=Empty):
        if not path : path = self.vbdLibImgFileLocal
        loaded = DOS.file2(path, fType=FRead)
        return loaded.split(self.separatorRec) if loaded != -1 else Empty
        
    def getLibFiles(self, libImg):
        return [DOS.join(self.vdbSyncLoacalDir, fls) for rec in libImg for fls, tm in [rec.split(self.separatorItm)]] if libImg else [] 
    
    def cmpImgs(self, libImgA, libImgB, raw=False):
        def _cmpLists(listA, listB):
            result = []
            for itm in listA:
                if itm not in listB : result.append(itm)
            return result
    
        removed = _cmpLists(libImgA, libImgB)        
        added   = _cmpLists(libImgB, libImgA)
        
        return (removed, added) if raw else (self.getLibFiles(removed),  self.getLibFiles(added))
    
    
    def createLibImgSync(self, new=True):
        if new:
            self.saveLibImg(path=self.vbdLibImgSyncFile)
        else:
            DOS.copyf(self.vbdLibImgFileLocal, self.vbdLibImgSyncFile)
    
    
    def getLocalChanges(self):
    
        def _removeOld(img, record):
            fl, code = record.split(self.separatorItm)
            for rec in img:
                fl_tmp, code_tmp = rec.split(self.separatorItm)
                if fl_tmp == fl : img.remove(rec)
            return img  
    
        oldLibImg = self.loadLibImg()
        newLibImg = self._addTime(self.libScan())
        synLibImg = self.loadLibImg(self.vbdLibImgSyncFile) 
        
        if not oldLibImg : self.saveLibImg(img=newLibImg)
        if not synLibImg : self.createLibImgSync(new=False)  
        if not oldLibImg or not synLibImg : return True 
        
        removed, added = self.cmpImgs(synLibImg, newLibImg, raw=True)
        
        for rem in removed:
             oldLibImg = _removeOld(oldLibImg, rem) 
             synLibImg.remove(rem)
        
        for add in added:
             oldLibImg.append(add)
             synLibImg.append(add)
        
        self.saveLibImg(img=oldLibImg)
        self.saveLibImg(path=self.vbdLibImgSyncFile, img=synLibImg)
        
        return True if removed or added else False  
    
    
    def getDirsCount(self, flist):
        dirlist = []
        for itm in flist:
            tdir = DOS.gettail(itm)
            if tdir not in dirlist : dirlist.append(tdir)
        return len(dirlist)     
    
    
    ### Rise report fnc ...
    def raise_report(self):
        GUI.dlgOk(tlraw(TAG_ERR_DBXRAISE) % (NewLine))
    
    
    ### Watch sync functions ...
    
    def watchSync(self, upload=False, download=False):
    
        self._setProgress()
    
        if not self._connect()  : return -1    
        if not self._syncLock() : self._disconnect(stayLocked=True); return -2 
        
        if upload: 
            self._watchUploadForce()
            self._disconnect()
            return stypeUploadFull
            
        if download: 
            self._watchDownloadForce()
            self._disconnect()
            return stypeDownloadFull
    
        self._progressStep(self.prog_msgs[3])
        ### Delete local tmp WS file (if exists) ...
        DOS.delf(self.infFPathTmp)
        ### Get tmp WS from DBX ...
        self.dbx.get_file(self.infDBX, self.infFPathTmp)
        ### Get info from tmp WS file ...
        _syncInfoDBX, _movPackDBX, _tvsPackDBX = self._getUnpacked(self.infFPathTmp)
        ### Force upload if no tmp (DBX) WS file ...
        if not _syncInfoDBX: 
            self._watchUploadForce()
            self._disconnect()
            return stypeUploadFull
        ### Get info from local WS file ...
        _syncInfo, _movPack, _tvsPack = self._getUnpacked(self.infFPath)
        ### Force Download if no local WS file ...
        if not _syncInfo: 
            self._watchDownloadForce()
            self._disconnect()
            return stypeDownloadFull
        ### Compare sync time (exit if same)
        if _syncInfo == _syncInfoDBX:
            self._nosyncProgressSteps()
            self._disconnect() 
            return stypeNoSync
        ## determ U/D type ...
        if _syncInfo < _syncInfoDBX :
            self._progressStep(self.prog_msgs[11])
            ## Download type ...
            infSyncType = stypeDownload 
            ## Delete local WS file ... 
            DOS.delf(self.infFPath)
            ## Rename tmp WS to local WS file ...
            DOS.rename(self.infFPathTmp, self.infFPath)  
            ## Set wathed info (changes only) ...
            self._setInfoChanges(_movPackDBX, _tvsPackDBX, _movPack, _tvsPack)
            ## Calc progress final steps (2) ...
            self._calcProgressSteps(2, 0)  
        else:
            ## Calc progress steps (4) ...
            self._calcProgressSteps(2)
            self._progressStep(self.prog_msgs[12], blank=True)
            ## Upload type ...
            infSyncType = stypeUpload
            ## Delete tmp WS file ...
            DOS.delf(self.infFPathTmp)
            ## Send Watched Info file ...
            self._sendWatchedFile()
            ## Calc progress final steps (2) ...
            self._calcProgressSteps(2, 0)
        
        self._disconnect()
        return infSyncType
    
    
    def putChangesRecord(self, file, watched, position, total, isMovie):
        def _chRecord(file, watched, position, total, vlist):
            Id = -1
            for itm in vlist:
                if itm['file'].endswith(setLower(file)):
                    Id = itm['id'] 
                    vlist.remove(itm)
                    break

            vlist.append({'id':Id, 'file':file, 'watched':watched, 'position':position, 'total':total})           
            return vlist

        _syncInfo, _movPack, _tvsPack = self._getUnpacked(self.infFPath)
        
        tmpList = self._unpack(_movPack if isMovie else _tvsPack)
        tmpList = _chRecord(file.replace(self.vdbSyncLoacalDir, Empty), watched, position, total, tmpList)
        if isMovie : _movPack = self._pack(tmpList)
        else       : _tvsPack = self._pack(tmpList)
        
        _syncInfo = str(time.time())
        
        packed = self.separatorWS3.join([_syncInfo, _movPack, _tvsPack])     
        DOS.file2(self.infFPath, packed, fType=FWrite, fRew=True)
    
    
    def _pack(self, infoList):
        tmpList = []
        for itm in infoList:
           rec = self.separatorWS1.join([str(itm['id']), itm['file'], str(itm['watched']), str(itm['position']), str(itm['total'])])
           tmpList.append(rec)
        return self.separatorWS2.join(tmpList)
    
    
    def createWatchedInfo(self, standalone_progress=False):
        
        moviesList  = self._getmovies(standalone_progress, extreserve=600)
        tvshowsList = self._gettvshows(standalone_progress, extreserve=100)
        
        _syncInfo = str(time.time())
        
        _movPack = self._pack(moviesList)
        _tvsPack = self._pack(tvshowsList)
        packed   = self.separatorWS3.join([_syncInfo, _movPack, _tvsPack])
             
        DOS.file(self.inffName, self.vdbSyncLoacalDir, packed, fType=FWrite, fRew=True)
    
    
    def _setInfoChanges(self, _movPackDBX, _tvsPackDBX, _movPack, _tvsPack):
    
        def _cmpLists(listA, listB):
            result = []
            for itm in listA:
                if itm not in listB : result.append(itm)
            return result
        
        
        _movsDBX = self._unpack(_movPackDBX)  
        _movs    = self._unpack(_movPack)
        _tvssDBX = self._unpack(_tvsPackDBX)
        _tvss    = self._unpack(_tvsPack)
        
        _movChanges = _cmpLists(_movsDBX, _movs)
        _tvsChanges = _cmpLists(_tvssDBX, _tvss)
        
        ## Calc progress steps ...
        #self._calcProgressSteps(len(_movChanges)+len(_tvsChanges))
        
        self._setInfo(_movChanges, isMovie=True)
        self._setInfo(_tvsChanges, isMovie=False)     
    
    
    def _setWatchedInfo(self):
        _syncInfo, _movPack, _tvsPack = self._getUnpacked(self.infFPath)
        self._setUnpacked (_movPack, _tvsPack)
    
    
    def _watchDownloadForce(self):
        self._progressStep(self.prog_msgs[11])
        ### Delete local tmp WS file ...
        DOS.delf(self.infFPathTmp)
        ### Get tmp WS from DBX ...
        self.dbx.get_file(self.infDBX, self.infFPathTmp)
        ### Exit if no tmp(DBX) WS file ...
        if not DOS.exists(self.infFPathTmp) : return
        ### Delete local WS file ...
        DOS.delf(self.infFPath)
        ### Rename tmp WS to local WS file ...
        DOS.rename(self.infFPathTmp, self.infFPath)
        ### Set wathed info ...
        self._setWatchedInfo() 
        ## Calc progress final steps (2) ...
        self._calcProgressSteps(2, 0)
    
    
    def _sendWatchedFile(self):
        ### Delete DBX WS file ...
        self.dbx.delete(self.infDBX)
        ### Send local WS file to DBX ...
        self.dbx.send_file(self.infFPath, self.infDBX)
        
    
    def _watchUploadForce(self):
        ### Create WS file ... 
        self.createWatchedInfo()
        ## Calc progress steps (2) ...
        self._calcProgressSteps(2)
        self._progressStep(self.prog_msgs[12], blank=True)
        ## Send Watched Info file ...
        self._sendWatchedFile()
        ## Calc progress final steps (2) ...
        self._calcProgressSteps(2, 0)
        
    
    def sendWatchedInfo(self): 
        self._setProgress()

        if not self._connect()  : return -1    
        if not self._syncLock() : self._disconnect(); return -2 
        
        self._calcProgressSteps(4)
        self._progressStep(self.prog_msgs[12], blank=True)
        self._sendWatchedFile()
        self._disconnect()

        
    
    def _getUnpacked(self, infoFile):
        packed = DOS.file2(infoFile, fType=FRead)
        if packed == -1 : return Empty, Empty, Empty
        _syncInfo, _movPack, _tvsPack = packed.split(self.separatorWS3)
        return _syncInfo, _movPack, _tvsPack
    
    
    def _setUnpacked(self, _movPack, _tvsPack):        
                
        moviesList  = self._unpack(_movPack) 
        tvshowsList = self._unpack(_tvsPack)
        
        self._setInfo(moviesList, isMovie=True)
        self._setInfo(tvshowsList, isMovie=False)
    
    
    def _unpack(self, packed):
        tmpList = []
        for rec in packed.split(self.separatorWS2):
            Id, file, watched, position, total = rec.split(self.separatorWS1) 
            tmpList.append({'id':int(Id), 'file':file, 'watched':int(watched), 'position':float(position), 'total':float(total)})
        return tmpList  
        
    
    def _setInfo(self, infoList, isMovie):
    
        def _getId(file, vidsList):
            for itm in vidsList:
                if file == itm['file'] : return int(itm['id'])
            return Empty   
    
        def _setResume(Id, watched, position, total, isMovie):
            if isMovie : cmd = self.cmd_set_mov; cmd2 = self.cmd_set_movw
            else       : cmd = self.cmd_set_tvs; cmd2 = self.cmd_set_tvsw
            
            if watched: 
                xbmc.executeJSONRPC(cmd2 % (str(Id), '1'))
                position = 0        
            
            xbmc.executeJSONRPC(cmd % (str(Id), str(position), str(total)))
    
    
        if isMovie : vidsList = self._getmovies(extreserve=900);  self._calcProgressSteps(len(vidsList), 800)
        else       : vidsList = self._gettvshows(extreserve=600); self._calcProgressSteps(len(vidsList), 100)
        
        self._progressStep(self.prog_msgs[19], blank=True) 
    
        for itm in infoList:
            self._progressStep()
            Id = _getId(itm['file'], vidsList)
            if Id : _setResume(Id, itm['watched'], itm['position'], itm['total'], isMovie=isMovie)
            wait(addon.JSIVAL)
    
    
    def _getmovies(self, standalone_progress=False, extreserve=0): 
        if standalone_progress:
            self.progress_show_always = True
            self._setProgress()
        
        self._progressStep(msg=self.prog_msgs[20])
        
        moviesList = []
        movList = self._js(self.cmd_mov, 'movies') 
        
        self._calcProgressSteps(len(movList), reserve=extreserve)
        #self._progressStep(msg='>> Scan movs', blank=True)
        
        for mov in movList:
         
            self._progressStep()
           
            mId      = mov['movieid']
            tmpFile  = mov['file']
            mFile    = DOS.getdir(tmpFile) 
            mDetails = self._js(self.cmd_mov_w % mId, 'moviedetails')
            watched  = mDetails['playcount']
            position = mDetails['resume']['position']
            total    = mDetails['resume']['total']
            rMovie   = {'id':mId, 'file':mFile, 'watched':watched, 'position':position, 'total':total}
            moviesList.append(rMovie)
        
        if standalone_progress:
            self._delProgress()
            self.progress_show_always = True
        
        return moviesList
            
            
    def _gettvshows(self, standalone_progress=False, extreserve=0):
        if standalone_progress:
            self.progress_show_always = True
            self._setProgress()
        
        self._progressStep(msg=self.prog_msgs[21])
        
        tvshowsList = []
        tvsList = self._js(self.cmd_tvs_tvs, 'tvshows')
        
        self._calcProgressSteps(len(tvsList), reserve=extreserve)
        #self._progressStep(msg='>> Scan tvss', blank=True)
         
        for tvs in tvsList:
            
            self._progressStep()
                
            tvsId = tvs['tvshowid']
            epsList = self._js(self.cmd_tvs_eps % tvsId, 'episodes')
            for eps in epsList:     
                epId      = eps['episodeid']  
                tmpFile   = eps['file']
                tmpFl     = DOS.getdir(tmpFile)
                tmpDir    = DOS.getdir(DOS.gettail(tmpFile))
                #epsFile   = tmpFile.replace(DOS.gettail(tmpFile), Empty)
                epsFile   = DOS.join(tmpDir, tmpFl)
                epDetails = self._js(self.cmd_tvs_w % epId, 'episodedetails')
                watched   = epDetails['playcount']
                position  = epDetails['resume']['position']
                total     = epDetails['resume']['total']
                rEpisode  = {'id':epId, 'file':epsFile, 'watched':watched, 'position':position, 'total':total}
                tvshowsList.append(rEpisode)
                
        if standalone_progress:
            self._delProgress()
            self.progress_show_always = True
            
        return tvshowsList
    
    
    def _js(self, cmd, key):
        try    : return eval(xbmc.executeJSONRPC(cmd))['result'][key]
        except : return [] 
                   
    
    ### Addon UID ...
    def getAddonUID(self):
        uid = DOS.file(self.adnUID_file, self.vdbSyncLoacalPrDir, fType=FRead)
        if uid == -1: 
            uid = '{:0>12d}'.format(int(time.time()*100))+'{:0>5d}'.format(randrange(0, 99999))
            DOS.file(self.adnUID_file, self.vdbSyncLoacalPrDir, uid)
        return uid
              