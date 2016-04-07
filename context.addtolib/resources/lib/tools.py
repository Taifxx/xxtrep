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
import time

from resources.lib.deecode import *
from resources.lib.const   import *

#import resources.lib.gui as GUI

### Tools ...
setLower       = lambda text : e(de(text).lower())
setCap         = lambda text : e(de(text).capitalize())
               
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

# def setBoxed (text, strMaxLen, ignoreTagQ = Empty):
#     if len(ignoreTagQ) == 2 :
#         iTagS = ignoreTagQ[0]
#         iTagE = ignoreTagQ[1]
#         ignoreTags = True
#     else:
#         iTagS = Empty
#         iTagE = Empty
#         ignoreTags = False
#     
#     editText = text
#     editText = editText.replace(NewLine, Space+NewLine)
#     if ignoreTags :
#         editText = editText.replace(iTagS, Space+iTagS+Space)
#         editText = editText.replace(iTagE, Space+iTagE+Space)
#         
#     wordList = editText.split(Space)
#     newwordList = []
#     stopLen     = False
#     curLineLen  = 0
#     for word in wordList:
#         if ignoreTags :  
#             if word == iTagS : stopLen = True
#             
#         if stopLen : wordLen = 0  
#         else       : wordLen = len(word) + 1
#         
#         if ignoreTags :  
#             if word == iTagE : stopLen = False
#              
#         if curLineLen + wordLen > strMaxLen :
#             curLineLen = wordLen
#             newwordList.append(NewLine + word)
#         else:
#             curLineLen += wordLen
#             newwordList.append(word)
#             
#         if word.startswith(NewLine): 
#             curLineLen = 0
#         
#     editText = Space.join(newwordList)
#     if ignoreTags :
#         editText = editText.replace(Space+iTagS+Space, iTagS)
#         editText = editText.replace(Space+iTagE+Space, iTagE)
#     editText = editText.replace(Space+NewLine, NewLine)
#                          
#     return editText  
#     
# def setPaged(text, lineLimit):
#     
#     startpos  = 0
#     endpos    = 0
#     lineCount = 0
#     pageNum   = 0
#     pageList  = []
#     
#     #GUI.dlgOk(str( lineLimit ))
#     while True:
#     
#         endpos = text.find(NewLine, endpos+1)
#         if endpos != -1: 
#             lineCount += 1
#             if lineCount > lineLimit:
#                 pageList.append(text[startpos:endpos+1])
#                 pageNum += 1
#                 startpos  = endpos+1
#                 lineCount = 0
#             
#         else :
#              
#             pageList.append(text[startpos:len(text)])
#             break
#     
#     return pageList
#     
         
    
     
    
    