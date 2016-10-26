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
########## ZIP:

### Import modules ...
from base import *
from zipfile import ZipFile
from progress import CProgress
import dos as DOS


class CZIP:

    def __init__(self, zipfilepath, fmode=FWrite):
        self._zipfile = ZipFile(zipfilepath, fmode)
        
    def __del__(self):
        self.close()
        
    def zipdir(self, path, progress, ttl=Empty, template=Empty):
        flcount = 0
        arch = [itm for itm in DOS.walk(path)] 
        substep = 100.0 / len(arch) 
        for root, dirs, files in arch:
            lenf  = len(files)
            if lenf : stepv = substep / lenf
            else    : progress.step(ttl, substep) 
            for file in files:  
                progress.step(ttl if ttl else file, stepv)
                if template and not self.isTempl(file, template) : continue
                fullpath = DOS.join(root, file)
                base     = fullpath.replace(path, Empty)  
                self._zipfile.write(esys(de(fullpath)), esys(de(base)))
                flcount += 1

        del progress
        return flcount
    
    def isTempl(self, file, template):
        for tmpl in template:
            if file.find(tmpl) != -1 : return True
        return False 
    
    def unzip(self, path):
        self._zipfile.extractall(path)
    
    def crc(self):
        try    : rc = True if self._zipfile.testzip() is None else False
        except : rc = False 
        return   rc
        
    def close(self):
        self._zipfile.close()
