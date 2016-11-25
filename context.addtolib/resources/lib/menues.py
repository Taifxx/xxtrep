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
########## MENUES:

### Import local modules ...
from ext import *
  

### Menues ... 
class tagMenue:

    def __init__(self, *args, **kwargs):
                
        self._cancelTag = kwargs['cancelTag']
        self._backTag   = kwargs['backTag']
        self._nextTag   = kwargs['nextTag']
        self._title     = kwargs.get('title', Empty)
        self._addict    = kwargs.get('addict', Empty)
        
        visCond         = kwargs['visCond']
        pageCLimit      = kwargs['pageLimit'] 
        
        itmList = args
            
        refPage          = []
        RPunFormMnuItems = []
        unFormMnuItems   = []
        for itm in itmList:
            if not self._xin(itm['hideCond'], visCond) or itm['hideCond'] == {} : 
                try:    
                    refPage.append(itm['refPage'])
                    RPunFormMnuItems.append(itm)
                except: 
                    unFormMnuItems.append(itm)
        
        unSortMnuItems   = [[itm['pos'], itm['tag']] for itm in unFormMnuItems]
        unSortMnuItems.sort()
        mnuItems         = [itm[1] for itm in unSortMnuItems]
        
        RPunSortMnuItems = [[itm['pos'], itm['refPage'], itm['tag']] for itm in RPunFormMnuItems]
        RPunSortMnuItems.sort()
        RPmnuItems       = [[itm[1], itm[2]] for itm in RPunSortMnuItems]
        
        itmListNoAddCount = len(mnuItems)
        itmListAddCount   = 0
        pageNum           = 0
        exiList           = []
        self._mnuPages    = []
        
        pageCLimit -= 1
        
        while itmListNoAddCount > 0:
        
            pageLimit          = pageCLimit - len(exiList) 
         
            isEnd, addCount    = (False, pageLimit) if itmListNoAddCount >= pageLimit else (True, itmListNoAddCount)
            refCount           = refPage.count(pageNum) if pageNum in refPage else 0
            needNext           = True if addCount + refCount > pageLimit or not isEnd else False
            refOver            = True if refCount + int(needNext) > pageLimit else False
            
            if needNext: 
                    addCount  -= 1 if not isEnd else 0 
                    isEnd      = False 
                    nxt        = [self._nextTag]
            else:   nxt        = []                    
            
            if refCount: 
                    addCount  -= refCount if needNext else 0 
                    refList    = [itm[1] for itm in RPmnuItems if itm[0] == pageNum]
            else:   refList    = []
              
            if refOver: 
                    addCount   = 0 
                    isEnd      = False
            
            if addCount:
                    addList    = mnuItems[itmListAddCount : itmListAddCount + addCount]
            else:   addList    = [] 
              
            addList = exiList + addList + nxt + refList
            exiList = []
            
            itmListNoAddCount -= addCount
            itmListAddCount   += addCount
                
            if isEnd: 
                    mnuItems   = [itm[1] for itm in RPmnuItems if itm[0] > pageNum]
                    if mnuItems:
                            exiList    = addList
                            addList    = []
                            RPmnuItems = []
                            refPage    = []
                            
                            itmListNoAddCount = len (mnuItems)
                            itmListAddCount   = 0
                    else:   itmListNoAddCount = 0
                        
            else:   pageNum   += 1 
            
            if addList : self._mnuPages.append(addList)
        
        if self._mnuPages : self._mnuPages[0].append(self._cancelTag) 
        for idx in range(len(self._mnuPages))[1:] : self._mnuPages[idx].append(self._backTag)
    
    
    def _xin(self, seqQ, seqV):
        for itm in seqQ:
            if type(itm) == tuple:      
                if seqV.issuperset(itm) : return True     
            else: 
                if itm in seqV          : return True
        return False 
    
    
    def _showPage(self, pageNum):
        
        if self._mnuPages :
            mnuVals  = self._mnuPages[pageNum]
            mnuNames = [tl(itm) for itm in self._mnuPages[pageNum]]
            if self._title : args = [mnuNames, self._title]
            else           : args = [mnuNames]
            _plen = len(self._mnuPages)   
            _msg  = self._addict + (TAG_PAR_LNPAGE % (str(pageNum+1), str(_plen)) if _plen > 1 else Empty) 
            return mnuVals[GUI.dlgSel(*args, lnmsg=_msg)] 
        else: return self._cancelTag
    
    def show(self, pageNum = 0):
        result = Empty
        while result in [Empty, self._backTag, self._nextTag]:
            result = self._showPage(pageNum)
            if   result == self._backTag : pageNum -= 1
            elif result == self._nextTag : pageNum += 1
                
        return pageNum, result


class simpleMenue:

    def __init__(self, mnuNames, mnuVals, cancelName, cancelVal, mnuMultiSel=False, mnuSelMark=Empty, mnuTitle=Empty, mnuSelDef=None, resetItm=Empty):
        self._cancelVal   = cancelVal
        self._cancelName  = cancelName
        self._mnuNames    = mnuNames
        self._mnuVals     = mnuVals
        self._title       = mnuTitle
        self._mnuMultiSel = mnuMultiSel
        self._mnuSelMark  = mnuSelMark
        self._mnuSelDef   = mnuSelDef
        self._resetItm    = resetItm 
    
    
    def show(self):
    
        ## Add Cancel ...
        self._mnuVals.append (self._cancelVal)
        self._mnuNames.append(self._cancelName)
        
        args    = [self._mnuNames]
        selMark = [self._mnuSelMark]
        
        if self._title : title = [self._title]
        else           : title = []
        
        if self._mnuSelDef : selDef = {'selDef':self._mnuSelDef}
        else               : selDef = dict()
        
        selDef.update({'resetItm':self._resetItm})
        
        ## Show Menue and parse result ...
        if self._mnuMultiSel:
            args += selMark + title 
            resList = GUI.dlgSelmul(*args, **selDef)
            result  = []
            for idx in resList : result.append(self._mnuVals[idx])       
        else:
            args += title
            result = self._mnuVals[GUI.dlgSel(*args)]
        return  result


def subMenue (submNames, submVals=Empty, default=Empty, title=Empty, defidx=0, cancelVal=TAG_MNU_BACKMAIN, cancelName=Empty, multiSel=False, multiSelDefList=None, selMarkm=Empty, resetItm=Empty):
    if not submVals: 
        submCVals  = submNames
        submCNames = [tl(itm) for itm in submNames]
    else: 
        submCVals  = submVals
        submCNames = submNames
    
    if default in submCVals :
        idx    = submCVals.index(default)
        submCVals.pop(idx)
        srcNm  = submCNames.pop(idx)
        srcQNm = tl(TAG_MNU_QR) +srcNm+ tl(TAG_MNU_QL)
        
        submCVals.insert(defidx, default)
        submCNames.insert(defidx, srcQNm)
        
    if multiSelDefList : multiDef = [submCNames[idx] for idx in multiSelDefList]
    else               : multiDef = []
        
    if cancelName : cnlName = tl(cancelName) 
    else          : cnlName = tl(TAG_MNU_BACKMAIN)
                 
    Menue = simpleMenue(cancelName  = cnlName,
                        cancelVal   = cancelVal,
                        mnuVals     = submCVals, 
                        mnuNames    = submCNames,
                        mnuTitle    = title,
                        mnuMultiSel = multiSel,
                        mnuSelMark  = selMarkm,
                        mnuSelDef   = multiDef,
                        resetItm    = resetItm)
                        
    result = Menue.show(); del Menue
    return result  