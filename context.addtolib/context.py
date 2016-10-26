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
########## ADDON STARTER:

### Import modules ...
import li
### Scan listitems ...
li.DETVIDEXT = True
items = li.vidItems()

### Import next modules ...
import xbmcaddon, os, pickle

### Define ...
SCRIPT_ID  = 'context.addtolib'
LOCK_FILE  = 'lock_started'
PAR_ACTION = 'action='
Empty      = ''

msgProcessError = 'Process ERROR'

COLOR_FORMAT = '[COLOR %s]%s[/COLOR]'

ITD_FILE   = 'li_dump'
error_file = '_errors_'

### Get standalone info ...
addon = xbmcaddon.Addon(id=SCRIPT_ID)
profile_nc = li.xbmc.translatePath(addon.getAddonInfo('profile'))
try    : profile = os.path.normpath(profile_nc.decode('utf-8'))
except : profile = os.path.normpath(profile_nc)

### Base functions ...
def pic(filename, pObject):
    file = open(os.path.join(profile, filename), 'wb')
    pickle.dump(pObject, file)
    file.close()


### Arguments Parsing ...
def parsingArguments():
    try    : argv1 = sys.argv[1]
    except : argv1 = Empty
        
    argv1 = int(argv1.replace(PAR_ACTION, Empty)) if argv1 and argv1.startswith(PAR_ACTION) else Empty
    if argv1 : return [argv1] 
     
    kwargs = get_params()
    if not kwargs : return ['noaction'] 
    return ['play', kwargs] 
    

### Get add-on params (as link) ...    
def get_params():
    param=[]
    try    : paramstring=sys.argv[2]
    except : paramstring=Empty
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?#','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&#')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=#')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
                            
    return param


### Main function ...   
def Main():
    
    loadad_from_memory = True if addon.getSetting('uselfm') == 'true' and \
        addon.getSetting('srvstatusv') == 'true' and addon.getSetting('usesrv') == 'true' else False
    
    ## Parsing arguments and start addon ...
    addon_args = parsingArguments()
    action_id  = Empty
    if addon_args[0] == 'play':
        import context_ex
        context_ex.callSTRM(**addon_args[1])
         
    elif addon_args[0] != 'noaction':
        import context_ex
        context_ex.plgMain(addon_args[0])
    
    else:
        if not loadad_from_memory:
            import context_ex
            context_ex.plgMain(loadLI=items)
        else:
            pic(ITD_FILE, items)
    

##### Start main ...
if __name__ == '__main__':
    try:
        try:  
            Main()
        except:
            import xbmcgui, deb
            title = COLOR_FORMAT % (addon.getSetting('mnucolor'), addon.getAddonInfo('name'))
            xbmcgui.Dialog().notification(title, msgProcessError, xbmcgui.NOTIFICATION_ERROR)
            lf = os.path.join(profile, LOCK_FILE)
            if os.path.exists(lf) : os.remove(lf)
            deb.addraise(os.path.join(profile, error_file))
            raise
    except :
        #raise 
        pass
    