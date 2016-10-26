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
########## DROPBOX ATL API:

### Import modules ...
import dropbox 
from ext import *


### DBX Main Class ...
class dropboxConnect():

    def __init__(self, limit_time, limit_count, raise_report):
        self.accessTokenPath = LIB.lib
        self.app_key         = TAG_PAR_DBXAPPKEY
        self.app_secret      = TAG_PAR_DBXAPPSECRET
        self.accessTokenFile = TAG_PAR_DBXACCESSTOKEN_FILE
        self.access_token    = self.loadAccessToken()
        self.client          = Empty
        
        self.limit_time      = limit_time
        self.limit_count     = limit_count
        self.raise_report    = raise_report
        
        self.progstepfnc     = None
        self.progmsgdefault  = Empty
        self.progmsg         = self.progmsgdefault
        self.prog_msgs       = []
            
    
    
    def progress_setmsgdecorator(msgn):
        def _inside_decorator(decfunct):
            def _set_msg(*args, **kwargs):
                self = args[0]
                #GUI.msg(self.prog_msgs[msgn])
                self.progmsg = self.prog_msgs[msgn]
                if self.progstepfnc is not None : self.progstepfnc(self.progmsg, blank=True)   
                result = decfunct(*args, **kwargs)
                self.progmsg = self.progmsgdefault
                return result  
            return _set_msg
        return _inside_decorator
    
    
    def progress_decorator(decfunct):
        def _use_progress(*args, **kwargs):
            self = args[0]
            if self.progstepfnc is not None : self.progstepfnc(self.progmsg)
            return decfunct(*args, **kwargs)
        return _use_progress 
    
    
    def limit_decorator(decfunct):
        def _try_by_limit(*args, **kwargs):
            self = args[0]
            attempt = 0
            while True:
                try:
                    result = decfunct(*args, **kwargs)
                    return result
                #except dropbox.rest.ErrorResponse as err:
                except :
                    if attempt < self.limit_count : attempt += 1; wait(self.limit_time)
                    else :
                        self.raise_report() 
                        raise
    
        return _try_by_limit
    
    
    def Connect(self):
        if not self.access_token : return False 
        self.client = dropbox.client.DropboxClient(self.access_token)
        try    : accinfo = self.client.account_info()
        except : return False
        return True  
    
    
    def Disconnect(self):
        del self.client
        self.client = Empty
    
    
    def disableAToken(self):
        self.client = dropbox.client.DropboxClient(self.access_token)
        self.client.disable_access_token()
        del self.client; self.client = Empty
        DOS.delf(DOS.join(self.accessTokenPath, self.accessTokenFile))
        
    
    def isAToken(self):
        return True if self.access_token else False     
        
      
    def loadAccessToken(self):  
        atBuffer = DOS.file(self.accessTokenFile, self.accessTokenPath, fType=FRead)
        return Empty if atBuffer == -1 else atBuffer
    

    def authorize_dropbox(self, inboxWnd):
        error = True
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)
        authorize_url = flow.start()
        code = inboxWnd(0, authorize_url)
        if code:
            try    : self.access_token, user_id = flow.finish(code)
            except : inboxWnd(2); return False
            if not self.Connect() : inboxWnd(2); return False
            DOS.file(self.accessTokenFile, self.accessTokenPath, str(self.access_token), fType=FWrite, fRew=True)
            inboxWnd(1)
            return True
        else : return False
    
    
    @progress_decorator
    @limit_decorator
    def send_file(self, local_file, dbx_file):
        sendFile = DOS.file2(local_file, fType=FRead)
        response = self.client.put_file(dbx_file, sendFile, overwrite=True)
    
    
    @progress_decorator
    @limit_decorator
    def get_file(self, dbx_file, local_file):
        # try:
        #     getFile, metadata = self.client.get_file_and_metadata(dbx_file)
        # except : return Empty
        
        if not self.exists(dbx_file) : return Empty
        getFile, metadata = self.client.get_file_and_metadata(dbx_file)
        
        DOS.mkdirs(DOS.gettail(local_file)) 
        
        DOS.file2(local_file, getFile.read(), fType=FWrite)
        getFile.close()
        return metadata
    
    
    @progress_setmsgdecorator(0)
    def copy_dir(self, from_path, to_path, move=False):
        dbxDirList, dbxFlsList = self.listdir(from_path)
        for drs in dbxDirList:
            drsName = drs.replace(from_path, Empty)
            drsTarget = self.join(to_path, drsName) 
            self.copy_dir(drs, drsTarget, move=move)
            
        for fls in dbxFlsList:
            flsName = fls.replace(from_path, Empty)
            flsTarget = self.join(to_path, flsName)
            self.copy_file(fls, flsTarget) 
            if move : self.delete(fls)
            
        if move: self.delete(from_path)
    
    
    @progress_decorator
    @limit_decorator
    def copy_file(self, from_path, to_path):
        self.client.file_copy(from_path, to_path)
        #self.client.file_move(from_path, to_path)
    
    
    @progress_setmsgdecorator(1)
    def get_filesList(self, dbx_flist, dbx_prefix, local_path):
        for dbx_file in dbx_flist:
            separator  = DOS.pathsep(local_path)
            local_file = DOS.join(local_path, self.convertToLocal(dbx_file, dbx_prefix, separator))
            self.get_file(dbx_file, local_file)
    
    
    @progress_setmsgdecorator(2)
    def send_filesList(self, local_flist, local_prefix, dbx_dir):
        for local_file in local_flist:
            dbx_file = self.join(dbx_dir, self.convertToDBX(local_file, local_prefix))
            self.send_file(local_file, dbx_file)
    
    
    @progress_setmsgdecorator(3)
    def delete_filesList(self, dbx_flist):
        for dbx_file in dbx_flist:
            self.delete(dbx_file)
    
    
    def convertToDBX(self, local_file, local_prefix):
        fl_nopr = local_file.replace(local_prefix, Empty)
        fl_DBX  = fl_nopr.replace(Slash, BkSlash)
        if fl_DBX[0] == BkSlash : fl_DBX = fl_DBX[1:]      
        return fl_DBX
    
    
    def convertToLocal(self, dbx_file, dbx_prefix, separator):
        fl_nopr  = dbx_file.replace(dbx_prefix, Empty)
        fl_local = DOS.convpath(fl_nopr, separator)
        if fl_local[0] == separator : fl_local = fl_local[1:]      
        return fl_local
            
    
    @limit_decorator
    def create_dir(self, dbx_dirpath):
        self.client.file_create_folder(dbx_dirpath)
        
    
    @progress_setmsgdecorator(4)
    def send_dir(self, local_dir, dbx_dir, move=False, template=Empty):
        def isTempl(file, template):
            for tmpl in template:
                if file.find(tmpl) != -1 : return True
            return False 
       
        localDirList, localFlsList = DOS.listdir(local_dir)
        for drs in localDirList :
            localSubDir = DOS.join(local_dir, drs)
            dbxSubDir   = self.join(dbx_dir, drs)
            self.create_dir(dbxSubDir); self.send_dir(localSubDir, dbxSubDir, move, template=template)
            
        for fls in localFlsList:
            if template and not isTempl(fls, template) : continue
            localFl = DOS.join(local_dir, fls)
            dbxFl   = self.join(dbx_dir, fls)
            self.send_file(localFl, dbxFl) 
            if move : DOS.delf(localFl)
            
        if move: DOS.rmdir(local_dir)
    
    
    @limit_decorator
    def listdir (self, dbx_path):
        dirs = []; fls = [] 
        if not self.exists(dbx_path) : return Empty, Empty
        meta = self.client.metadata(dbx_path)
        for con_rec in meta['contents']:
            if str(con_rec.get('is_deleted', 'False')) == 'True' : continue
            if con_rec['is_dir'] == True : dirs.append(con_rec['path']) 
            else                         : fls.append(con_rec['path'])
        return dirs, fls
    
    
    def walkFiles(self, dbx_dir, template=Empty):
        def isTempl(file, template):
            for tmpl in template:
                if file.find(tmpl) != -1 : return True
            return False 
       
        filesList = []
        dbxDirList, dbxFlsList = self.listdir(dbx_dir)
        for drs in dbxDirList :
            filesList += self.walkFiles(drs, template=template)
            
        for fls in dbxFlsList:
            if template and not isTempl(fls, template) : continue
            filesList.append(fls)
        
        return filesList
    
    
    def exists(self, dbx_path):
        try: 
            meta = self.client.metadata(dbx_path)
            isdel = meta.get('is_deleted', 'False')
            if str(isdel) != 'True' : return True
            else : return False    
        except dropbox.rest.ErrorResponse as err:
            if err.status == 404 : return False
            else : raise err  
    
    
    @progress_setmsgdecorator(5)
    def get_dir(self, dbx_dir, local_dir, move=False, template=Empty):
        def isTempl(file, template):
            for tmpl in template:
                if file.find(tmpl) != -1 : return True
            return False 
       
        dbxDirList, dbxFlsList = self.listdir(dbx_dir)
        for drs in dbxDirList :
            dbxSubDir   = drs
            localSubDir = DOS.join(local_dir, drs.replace(dbx_dir, Empty))
            #DOS.mkdirs(localSubDir); self.get_dir(dbxSubDir, localSubDir, move, template=template)
            self.get_dir(dbxSubDir, localSubDir, move, template=template)
            
        for fls in dbxFlsList:
            if template and not isTempl(fls, template) : continue
            localFl = DOS.join(local_dir, fls.replace(dbx_dir, Empty))
            dbxFl   =  fls
            self.get_file(dbxFl, localFl) 
            if move : self.delete(dbxFl)
            
        if move: self.delete(dbx_dir)
           
    
    def join (self, *args):
        jargs  = DOS.jede(*args)  
        jr = BkSlash.join(jargs)
        return jr 
    
    @progress_decorator
    @limit_decorator
    def delete (self, dbx_path):
        # try:
        #     self.client.file_delete(dbx_path)
        # except : pass
        if not self.exists(dbx_path) : return
        self.client.file_delete(dbx_path) 
        
    
    @limit_decorator
    def rename(self, dbx_pathName, dbx_newPathName):
        self.client.file_move(dbx_pathName, dbx_newPathName)
            
