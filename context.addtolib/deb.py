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
########## DEB:

### Import modules ...
import sys, traceback, time


def addraise(filepath):
    
    current_time_sec = time.localtime(time.time()) 
    err_time = time.strftime('%H:%M:%S', current_time_sec)
    err_date = time.strftime('%x', current_time_sec)
    _err_type, _err_msg, _err_tb = sys.exc_info()
    err_type = str(_err_type)
    err_msg  = str(_err_msg)
    err_tb   = ''.join(traceback.format_tb(_err_tb)) 
    
    line = '--------------------------------------------------------------'
    data = '%s\nEXCEPTION :: %s :: %s \nTraceback ::\n---\n%s---\nType      :: %s\nMessage   :: %s\n---\n' %\
         (line, err_date, err_time, err_tb, err_type, err_msg)
    
    data2 = 'Extended  :: \nPlatform   : %s\nCoding sys : %s\nCoding def : %s\n\n' % (sys.platform, sys.getfilesystemencoding(), sys.getdefaultencoding())

    file = open(filepath, 'a')
    file.write(data+data2)
    file.close()