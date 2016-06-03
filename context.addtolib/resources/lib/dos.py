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
########## OS:

### Import modules ...
import os
import xbmc
import xbmcvfs

from resources.lib.deecode import *
from resources.lib.const   import *  
from resources.lib.tools   import *

### OS funtions ... 
copyf   = lambda  fpSrc, fpDest: xbmcvfs.copy (fpSrc, fpDest)
delf    = lambda  path: xbmcvfs.delete  (path)
rmdir   = lambda  path: xbmcvfs.rmdir   (path)
listdir = lambda  path: xbmcvfs.listdir (path)
#listdir = lambda  path: os.listdir      (path)
split   = lambda  path: os.path.split   (path)
#unsl    = lambda  path: os.path.normpath(path)
getdir  = lambda  path: os.path.split   (unsl(path))[1]
gettail = lambda  path: os.path.split   (unsl(path))[0]
#join    = lambda *args: os.path.join    (*jede(*args))
rename  = lambda  path, newPath : xbmcvfs.rename (path, newPath)


def isvfs(path):
    if not exists(path)     : return -1
    if os.path.exists(path) : return  0
    return 1 


def unsl(path):
    if not path : return Empty
    return path[0:-1] if path[-1] in [BkSlash, Slash] else path     

def join (*args):
    jargs  = jede(*args)
    sep    = BkSlash if jargs[0].find(BkSlash) != -1 else os.sep 
    jr     = sep.join(jargs)
    if sep == BkSlash : jr = jr.replace(Slash, BkSlash)
    bdlsep = sep+sep
    protx  = Colon+BkSlash+BkSlash
    protx_ = Colon+Colon
    jr     = jr.replace(protx, protx_)
    jr     = jr.replace(bdlsep, sep)
    jr     = jr.replace(protx_, protx)
    return jr 
         
def mkdirs (path):
    #try    : os.makedirs(esys(de(path)))
    try    : xbmcvfs.mkdirs(esys(de(path)))
    except : pass

def copyfls (pathSrc, pathDst, move=False):
    srcDirList, srcFlsList = listdir(pathSrc)
    for drs in srcDirList :
        srcSubDir = join(pathSrc, drs)
        dstSubDir = join(pathDst, drs)
        mkdirs(dstSubDir); copyfls(srcSubDir, dstSubDir, move)
        
    for fls in srcFlsList:
        srcFl = join(pathSrc, fls)
        dstFl = join(pathDst, fls)
        copyf(srcFl, dstFl) 
        if move : delf(srcFl)
        
    if move: rmdir(pathSrc)
        

def remove (path, delDir=True, maskfn=None):
    dirList, flsList = listdir(path)
    for fls in flsList:
        if maskfn is not None and not maskfn(path, fls) : continue 
        delf  (join(path, fls))
    for drs in dirList : remove(join(path, drs))
    if  delDir         : rmdir(path)
    return True 
    

def walk(path):
    dirs, files = listdir(path)
    if dirs:
        for dir in dirs:
            for sub in walk(join(path, dir)):
                yield sub
    yield path, dirs, files
     

def file(fName, fPath, fContent=Empty, fType=FWrite, fRew = True):

    if not fPath or not fName : return -1
    
    path = join(fPath, fName)

    if exists(path): 
        if fType in (FWrite, FAppend):
            if not fRew : return -1
            else        : delf(path)
    else: 
        if fType == FRead : return -1
    
    data = Empty
    
    #ofile = open(esys(de(path)), fType)
    ofile = xbmcvfs.File(esys(de(path)), fType)
    if   fType in (FWrite, FAppend) : ofile.write(fContent)
    elif fType ==  FRead            : data = ofile.read()
    ofile.close() 
    return data
    
def compath(path1, path2):
    return setLower(unsl(path1)) == setLower(unsl(path2))


def existsVFS(path):
    def _exists(path):
        try    : result = xbmcvfs.exists(esys(de(path)))
        except : result = False
        return True if result else False
    
    path = setLower(path)
    if   _exists(path)         : return True
    elif _exists(path+Slash)   : return True
    elif _exists(path+BkSlash) : return True
    return False


def exists(path):
    path = setLower(path)
    
    base_path   = gettail(path)
    element     = getdir(path)
    list_of_dir = listdir(path)
    elements    = list_of_dir[0] + list_of_dir[1] 
    
    if elements : return True
    
    list_of_dir = listdir(base_path)
    elements    = list_of_dir[0] + list_of_dir[1]

    if not elements : return False
    
    low_elements = [setLower(itm) for itm in elements]
      
    return True if element in low_elements else False


### JSP functions ...
_listdircmd = '{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"properties": ["file", "title"], "directory":"%s", "media":"files"}, "id": "1"}'

def jexists(path):
    import xbmc
    path  = setLower(path)
    spath = gettail(path)
    selem = getdir(path)
    return xbmc.executeJSONRPC(_listdircmd % (path))
    rmain = eval(xbmc.executeJSONRPC(_listdircmd % (path))).get('result', False)
    if rmain : return True
    
    rsub  = eval(xbmc.executeJSONRPC(_listdircmd % (spath))).get('result', False)
    if not rsub : return False
 
    itmlist = [setLower(itm['label']) for itm in rsub['files']]
    #return itmlist     
    return True if selem in itmlist else False