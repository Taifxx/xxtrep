#!/usr/bin/python
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
########## ERRORS:

##### Import modules ...
from resources.lib.ext       import *

### Parse some errors ...
def errord (errordef, errorn):

    ## Re define error tag ...
    error = errordef if errorn == TAG_ERR_OK else errorn   

    ## Parse Ok message ...
    if   error == TAG_ERR_OK          : GUI.msg   (tl(TAG_ERR_OK))
    elif error == TAG_ERR_OK_MOVADD   : GUI.msg   (tl(TAG_ERR_OK_MOVADD), tl(TAG_ERR_OK))
    elif error == TAG_ERR_OK_TVSADD   : GUI.msg   (tl(TAG_ERR_OK_TVSADD), tl(TAG_ERR_OK))
    elif error == TAG_ERR_OK_TVSUPD   : GUI.msg   (tl(TAG_ERR_OK_TVSUPD), tl(TAG_ERR_OK))
    elif error == TAG_ERR_OK_RESCAN   : GUI.msg   (tl(TAG_ERR_OK_RESCAN), tl(TAG_ERR_OK))
    elif error == TAG_ERR_OK_RESTOR   : GUI.msg   (tl(TAG_ERR_OK_RESTOR), tl(TAG_ERR_OK))
    elif error == TAG_ERR_OK_REMSRC   : GUI.msg   (tl(TAG_ERR_OK_REMSRC))
    elif error == TAG_ERR_OK_DELETE   : GUI.msg   (tl(TAG_ERR_OK_DELETE))
    elif error == TAG_ERR_OK_TVSREN   : GUI.msg   (tl(TAG_ERR_OK_TVSREN))
    elif error == TAG_ERR_OK_ADDFOL   : GUI.msg   (tl(TAG_ERR_OK_ADDFOL))
    ## Parse Errors ...
    elif error == TAG_ERR_NOTFILE     : GUI.msg   (tl(TAG_ERR_NOTFILE))            
    elif error == TAG_ERR_INCINPUT    : GUI.dlgOk(tl(TAG_ERR_INCINPUT),  tl(TAG_ERR_ABORT))
    elif error == TAG_ERR_LISTEMPTY   : GUI.dlgOk(tl(TAG_ERR_LISTEMPTY), tl(TAG_ERR_ABORT))