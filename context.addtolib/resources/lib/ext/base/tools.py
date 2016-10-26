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
########## TOOLS:

### Import modules ...
import pyperclip
import time

from const   import *
from tags    import *
from deecode import *


### Tools ...
setLower       = lambda text : e(de(text).lower())
setCap         = lambda text : e(de(text).capitalize())
setUpper       = lambda text : e(de(text).upper())
setCapAll      = lambda text : e(de(text).title()) 
               
sbool          = lambda sval : True if sval in ['True', 'true'] else False

normName       = lambda name : setCap(name.replace(Dot, Space))

wait           = lambda intv : time.sleep(intv)

inte           = lambda val  : int(val) if val else 0


def timefromsec(seccount, numform, sep):
    lsec = seccount
    lmin = lsec / 60
    lhou = lmin / 60
    rmin = lmin - lhou*60
    rsec = lsec - lmin*60
    
    _sep = sep
    _tpl = lambda val : numform.format(val)
    
    HOU = [_tpl(lhou), _sep] if lhou else [Empty, Empty]
    MIN = [_tpl(rmin), _sep]
    SEC = [_tpl(rsec)]
    
    return HOU+MIN+SEC 
       


def isWait(cond, fnc, timeout):
    waitTime = 0
    while True:
        if cond != fnc()      : return True
        if waitTime > timeout : return False
        time.sleep(1); waitTime += 1


def getUniqname(item, seq):
    uniqname = item
    for idx in range(len(seq)): 
        if uniqname not in seq : return uniqname  
        uniqname = '%s - %d' % (item, idx+1)
    return uniqname  
    

class struct:
    def __setattr__(self, name, value):
        self.__dict__.update({name:value})
    
    def __del__(self):
        self.__dict__.clear()
    
        
def getdate():
    return time.strftime('%d-%m-%y')

def getunftime():
    return time.strftime('%H-%M-%S')

def getdtcode(strtime):
    return time.strftime('%d.%m.%y.%H.%M.%S', time.gmtime(strtime)) if strtime else Empty 


def cmpListsRem(listA, listB):
    resList = []
    for elemA in listA:
        if elemA not in listB : resList.append(elemA)
    return resList     

def clipCopy(text):
    pyperclip.copy(text)

def clipPaste():
    return pyperclip.paste()
     
    
    