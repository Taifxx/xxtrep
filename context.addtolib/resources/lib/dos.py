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
unsl    = lambda  path: os.path.normpath(path)
getdir  = lambda  path: os.path.split   (unsl(path))[1]
gettail = lambda  path: os.path.split   (unsl(path))[0]
join    = lambda *args: os.path.join    (*jede(*args))
rename  = lambda  path, newPath : xbmcvfs.rename (path, newPath)

def mkdirs (path):
    try    : os.makedirs(esys(de(path)))
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
        

def remove (path, delDir=True):
    dirList, flsList = listdir(path)
    for fls in flsList : delf  (join(path, fls))
    for drs in dirList : remove(join(path, drs))
    if  delDir         : rmdir(path)
    return True 
     

def file(fName, fPath, fContent=Empty, fType=FWrite, fRew = True):

    if not fPath or not fName : return -1
    
    path = join(fPath, fName)

    if exists(path): 
        if fType in (FWrite, FAppend) and not fRew : return -1
    else: 
        if fType ==  FRead                         : return -1
    
    data = Empty
    
    ofile = open(esys(de(path)), fType)
    if   fType in (FWrite, FAppend) : ofile.write(fContent)
    elif fType ==  FRead            : data = ofile.read()
    ofile.close() 
    return data
    
def compath(path1, path2):
    return setLower(unsl(path1)) == setLower(unsl(path2))


def exists(path):
    try:    result = os.path.exists(esys(de(path)))
    except: result = False
    return  result