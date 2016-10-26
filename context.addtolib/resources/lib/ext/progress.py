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
########## PROGRESS:

### Import modules ...
from base import *

class CProgress:
    def __init__(self, maxnum=0, bg=True):
        if bg : self._pbar   = xbmcgui.DialogProgressBG()
        else  : self._pbar   = xbmcgui.DialogProgress()
        self._maxnum = maxnum
        self._curnum = 0
        self._show   = False
        self.bg      = bg
    
    def show(self, title, text=Empty):
        self._show = True
        if self.bg : text = title
        self._pbar.create(title, text)
        self.update(0)
    
    def step(self, mes=Empty, stepv=1):
        if not self._show : return
        self._curnum += stepv
        perc = int(round(float(self._curnum) / self._maxnum * 100, 0))
        self.update(perc, mes)
        
    def update(self, perc, mes=Empty):
        if not self._show : return
        self._pbar.update(perc, mes)
    
    def __del__(self):
        self._pbar.close()
        del self._pbar