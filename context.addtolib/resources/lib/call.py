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
########## CALL:

### Import modules ...
from ext import *
import sync


## Get handle ...
try    : HANDLE = int(sys.argv[1])
except : HANDLE = -1 

PBTYPES_LIST = [tl(TAG_DLG_PBTT1), tl(TAG_DLG_PBTT2), tl(TAG_DLG_PBTT3), tl(TAG_DLG_PBTT4), tl(TAG_DLG_PBTTRAN)]

## Player ...
class CPlayer(xbmc.Player):

    def __init__(self):
        Core = addon.PCORE
        if   Core == 'Auto'        : xbmc.Player.__init__( self, xbmc.PLAYER_CORE_AUTO ) 
        elif Core == 'VideoPlayer' : xbmc.Player.__init__( self, xbmc.PLAYER_CORE_VideoPlayer )
        elif Core == 'DVDPlayer'   : xbmc.Player.__init__( self, xbmc.PLAYER_CORE_DVDPLAYER )
        elif Core == 'MPlayer'     : xbmc.Player.__init__( self, xbmc.PLAYER_CORE_MPLAYER ) 
        elif Core == 'Custom'      : xbmc.Player.__init__( self, addon.PCOREVAL )
        else : xbmc.Player.__init__( self )
        
    def wait_openlink(self, splash):
        spath = setLower(splash)
        wtime = 0
        errc  = 0
        while True: 
            if self.isPlaying() and spath != setLower(self.getPlayingFile()) : break  
            wait(1); wtime += 1
            if wtime > addon.DEDLPTIME : return False
        return True
    
    def wait_buffering(self):
        wait(1) 
        buflevel = 0
        while buflevel < 3: 
            _oldpos = self.getTime() if self.isPlaying() else 0
            while self.isPlaying() and _oldpos == self.getTime(): wait(1)
            buflevel += 1
        
    def seek(self, pos):
        if addon.WAITBSEEK : wait(addon.WAITBSEEK) 
        if self.isPlaying() : self.seekTime(pos)
        #GUI.seekPlay(pos) 
    
    def try_ISP(self, strmurl, currentCont, skipgo):
        if not skipgo : GUI.goTarget(strmurl)
            
        wtime  = 0
        errorn = 0
        while True: 
             if self.isPlaying() : break
             if currentCont != LI.getCpath():
                 if currentCont != Empty : errorn = 1; break
             wait(1); wtime += 1
             if wtime > addon.DEDLPTIME : errorn = 2; break
        if errorn : wait(1); GUI.back(); 
        return errorn
    
    def wait_folder(self, currentcont):
        wtime  = 0
        lopen  = False
        while True:
            if wtime > addon.DEDLPTIME : return 2
            wait(1); wtime += 1
            if not lopen:
                if currentcont == LI.getCpath() : continue 
                else:  
                    currentcont = LI.getCpath()
                    lopen = True
                    if not LI.itemsCount() : return 1
            
            if self.isPlaying() : break  
            if currentcont != LI.getCpath() : return 2
        return 0
    
    def wait_or_stay(self, currentcont):
        wtime  = 0
        lopen  = False
        while True:
            if wtime > addon.DEDLPTIME : return 1
            wait(1); wtime += 1
            if not lopen:
                if currentcont == LI.getCpath() : continue 
                else:  
                    currentcont = LI.getCpath()
                    lopen = True
            
            if self.isPlaying() : break  
            if currentcont != LI.getCpath() : return 1
        return 0
    
    ## Get playback type (manual) ... 
    def pbTypeSelector(self, strmurl, url_prefix):
        #xbmcplugin.endOfDirectory(HANDLE, True, False, False)
        PBTYPES_LIST_L = PBTYPES_LIST + [tl(TAG_DLG_PBTT5)]
        
        autodetect = False
        tName      = prefixToName(url_prefix)
        
        GUI.dlgOk(tl(TAG_DLG_PBT1), title=tName)
        result = GUI.dlgSel(PBTYPES_LIST_L, tl(TAG_DLG_PBT2))
        if result == 5:
            autodetect = True
            GUI.msg(tl(TAG_DLG_PBTAD1), tl(TAG_DLG_PBTAD2))
            wait(2)
            currentCont = LI.getCpath()
            GUI.goTarget(strmurl)
            
            PTYPE     = 0 
            wtime     = 0
            wplayback = False
            while True: 
                if self.isPlaying() : wplayback = True; break
                if currentCont != LI.getCpath():
                    if currentCont != Empty:
                        if LI.itemsCount() > 0 : PTYPE = 3; break
                        else : break 
                wait(1); wtime += 1
                if wtime > 30:
                    if GUI.dlgYn(tl(TAG_DLG_PBTADTIMEO), title=tName) : wtime = 0  
                    else : break
            
            if not PTYPE:
                if not wplayback: 
                    GUI.back()
                    PTYPE = 1    
                else : PTYPE = 2
            else : GUI.back()
                
        else : PTYPE = result + 1
        
        wait(1)
        if   PTYPE == 1 : GUI.dlgOk(tl(TAG_DLG_PBTADTCLAS), title=tName)
        elif PTYPE == 2 : 
            if autodetect == False : GUI.goTarget(strmurl)
            GUI.dlgOk(tl(TAG_DLG_PBTADTISP), title=tName)
        elif PTYPE == 3 : GUI.dlgOk(tl(TAG_DLG_PBTADTFOLD), title=tName)
        elif PTYPE == 4 : GUI.dlgOk(tl(TAG_DLG_PBTALT), title=tName)
        elif PTYPE == 5 : GUI.dlgOk(tl(TAG_DLG_PBTTRANI), title=tName)       
        
        return PTYPE
            

## Emegrency running ...        
def simplerun(strmurl):
    listitem = xbmcgui.ListItem (path=strmurl)
    listitem.setProperty('IsPlayable', 'true')
    xbmcplugin.setResolvedUrl(HANDLE, True, listitem)
    GUI.msg(tl(TAG_ERR_DEFEPS))


## Run splash video ...
def runsplash(medinfo, infpar):
    splashPath = DOS.join(addon.path, *TAG_PAR_SPLASH_FILE)
    splashLI = xbmcgui.ListItem (path=splashPath)
    splashLI.setProperty('IsPlayable', 'true')
    splashLI.setArt(medinfo.art)
    splashLI.setIconImage(medinfo.img)
    splashLI.setThumbnailImage(medinfo.img)
    splashLI.setInfo('video', infpar)
    splashLI.setInfo('video', {'Title':Space}) 
    xbmcplugin.setResolvedUrl(HANDLE, True, splashLI)
    del splashLI   
    return splashPath


## Main function ...
def callSTRM(strmtype, strmurl, strmfile):

    ## Stop theme ...
    GUI.stopPlay()
    wait(1)
    
    ## Exit if empty URL ...
    if not strmurl : GUI.dlgOk(tl(TAG_ERR_DEDLINK)); return
    
    ## Get playback main type (0 - predefined) ...
    SPBMETHOD = addon.PBMETHOD
    if   SPBMETHOD == 'Classic only'                    : PBMETOD = 1
    elif SPBMETHOD == 'Alternate only (CORE dependent)' : PBMETOD = 2
    else : PBMETOD = 0 
    
    ## Init ...
    PTYPE  = 0 
    player = CPlayer()
    prePath = LIB.tvsf if strmtype == str(TAG_TYP_TVS) else LIB.mov
    #print ('     @@@@@ '+prePath+' :: '+strmfile+' :: '+DOS.join(prePath, strmfile))
    ## Check playback launching from Kodi library ...
    if not DOS.exists(DOS.join(prePath, strmfile)):
    
        ## If not from library ...
        simplerun(strmurl)
        del player
        return
    
    else:
    
        ## Get strm file ...
        strmfileS = DOS.getdir(strmfile)
        strmfldrS = DOS.getdir(DOS.gettail(strmfile))
        
        ## PreInit values ...
        listitem  = None
        pli       = Empty
        
        try    : playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        except : playlist = Empty
        
        ## Try get media info ...
        try:
         
            ## Get medinfo ...
            medinfo = CMedInfo(strmfldrS, strmfileS, strmtype)
            
            ## Init main listitem (playable element) ...
            listitem = xbmcgui.ListItem (path=strmurl)
            listitem.setProperty('IsPlayable', 'true')
            listitem.setArt(medinfo.art)
            listitem.setIconImage(medinfo.img)
            listitem.setThumbnailImage(medinfo.img)
            
            ## PreInit values ...
            splashPath    = Empty
            skipgo        = False
            keepcontainer = LI.getCpath()
             
            ## Transmit information to player ...
            if strmtype == str(TAG_TYP_TVS):
                infpar = {'Title': medinfo.title, 'Genre': medinfo.genre, 'Year': medinfo.year, 'Rating': medinfo.rating, 'Plot': medinfo.plot, 
                          'Country': medinfo.country, 'tvshowtitle': medinfo.showtitle, 'director': medinfo.director,
                          'votes': medinfo.votes, 'mpaa': medinfo.mpaa, 'studio': medinfo.studio, 'writer': medinfo.writer, 'season': medinfo.season, 
                          'episode': medinfo.episode, 'originaltitle': medinfo.originaltitle, 'premiered': medinfo.date, 'aired': medinfo.date,
                          'date': medinfo.date, 'cast': medinfo.cast, 'castandrole': medinfo.castandrole}
                
            else:
                infpar = {'Title': medinfo.title, 'Genre': medinfo.genre, 'Year': medinfo.year, 'Rating': medinfo.rating, 'Plot': medinfo.plot, 
                          'Country': medinfo.country, 'director': medinfo.director,
                          'votes': medinfo.votes, 'mpaa': medinfo.mpaa, 'studio': medinfo.studio, 'writer': medinfo.writer, 
                          'originaltitle': medinfo.originaltitle, 'premiered': medinfo.date, 'aired': medinfo.date,
                          'date': medinfo.date, 'cast': medinfo.cast, 'castandrole': medinfo.castandrole}
                
                ## Clear playlist if movie was running ...
                if playlist : playlist.clear()
            
            listitem.setInfo('video', infpar)
           
        ## Emergency running ...
        except: 
            simplerun(strmurl)
            del player  
            return
        
        ## PLAYBACK TYPES:
        
        url_prefix = getURLPrefix(strmurl)
        ### Predefined type ...
        if PBMETOD == 0:
            if url_prefix:
                pTable = playersTable(strmurl)
                PTYPE  = pTable.getPType()
                if PTYPE == -1:
                    splashPath = runsplash(medinfo, infpar)
                    wait(1); player.stop()
                    PTYPE = player.pbTypeSelector(strmurl, url_prefix)
                    pTable.setPType(url_prefix, PTYPE)
                    
                    if   PTYPE == 1 : del listitem, player; return
                    elif PTYPE == 2 : skipgo = True
            
            else : PTYPE = 1
        
        ### Classic type ...
        if PBMETOD == 1 or PTYPE == 1:
            xbmcplugin.setResolvedUrl(HANDLE, True, listitem)
            
            
        ### ISP type ...
        if PTYPE == 2:
            if not splashPath:
                splashPath = runsplash(medinfo, infpar)
                wait(1); player.stop()
            wait(1); errorn = player.try_ISP(strmurl, keepcontainer, skipgo)
            if errorn:
                if errorn == 1 : GUI.dlgOk(tl(TAG_ERR_INCPBTYPE) % (prefixToName(url_prefix) if url_prefix else tl(TAG_DLG_NPDIRL)), title=medinfo.title)
                if errorn == 2 : GUI.dlgOk(tl(TAG_ERR_DEDLINK), title=medinfo.title)
                del listitem, player
                return
        
        ### Folder type ...
        if PTYPE == 3:
            if not splashPath: 
                splashPath = runsplash(medinfo, infpar)
                wait(1); player.stop()
            wait(1); GUI.goTarget(strmurl)
    
        ### Alternate type ...
        if PBMETOD == 2 or PTYPE == 4:
            if not splashPath:
                splashPath = runsplash(medinfo, infpar)
                wait(1); player.stop()
            wait(1); player.play(strmurl, listitem)
        
        ### ISPSAW
        if PTYPE == 5:
           pli  = getPLI(playlist)           
           cwnd = xbmcgui.getCurrentWindowId()
           if not splashPath:
                splashPath = runsplash(medinfo, infpar)
                wait(1); player.stop()
           xbmc.executebuiltin('ActivateWindow(%s, %s)' % (cwnd, strmurl))
        
        
        ## Wait link opening for classic and alternate types ...
        if PTYPE not in [2, 3, 5] and not player.wait_openlink(splashPath): 
            GUI.dlgOk(tl(TAG_ERR_DEDLINK), title=medinfo.title)
            del listitem, player
            return
        
        ## Wait link opening for folder type ...
        elif PTYPE == 3: 
            errorn = player.wait_folder(keepcontainer)
            if errorn:
                if errorn == 1: 
                    GUI.dlgOk(tl(TAG_ERR_INCPBTYPE) % (prefixToName(url_prefix) if url_prefix else tl(TAG_DLG_NPDIRL)), title=medinfo.title)
                    if player.isPlaying() : player.stop()
                if errorn == 2 : GUI.dlgOk(tl(TAG_ERR_DEDLINK), title=medinfo.title)
                del listitem, player
                return
        
        ## Auto back to video library ...
        elif PTYPE == 5:
           errorn = player.wait_or_stay(keepcontainer) 
           xbmc.executebuiltin('ActivateWindow(%s, %s)' % (cwnd, keepcontainer))
           setPLI(playlist, pli)
           if errorn:
               GUI.dlgOk(tl(TAG_ERR_DEDLINK), title=medinfo.title)
               del listitem, player
               return  
        
        '''
        ## Forced closing dialogs ...
        eodgenMethod = addon.EODGENM 
        if eodgenMethod == 'Suppression' : wait(3); GUI.dlgOk(tl(TAG_DLG_SUPPRES)); wait(3); GUI.closeDlgs(); wait(3)
        '''  
        
        ## Set focus to player ...
        wait(2); GUI.FocusPayer()
            
        ## Run Playback Control ...
        wtime1 = 0
        possleep = True
        if addon.PLAYBCONT:
    
            pnTimer = 5
    
            ### Resume ...
            pbSet = False
            fargs = timefromsec(medinfo.pos, TAG_PAR_TIMENUMFORMAT, TAG_PAR_TIMESEP)
            if addon.RESDLG and medinfo.pos and not addon.AUTORES:
                pbm = GUI.dlgResume([tl(TAG_MNU_SFRBEGIN), tl(TAG_MNU_RFROM) % (fargs[0],fargs[1],fargs[2],fargs[3],fargs[4]), tl(TAG_MNU_CLOSEDLG)], title=medinfo.title)     
                if   pbm == 0 : pbSet = True; medinfo.resetpos()
                elif pbm == 1 : pbSet = True  
                elif pbm == 2 : pbSet = False
                pnTimer = 0
             
            if (addon.AUTORES and medinfo.pos) or pbSet : player.seek(medinfo.pos)
            
            ### Buffering ...
            player.wait_buffering()
            
            ### Get plaing file for control ...
            if player.isPlaying() : playing_file = player.getPlayingFile() 
            else                  : del listitem, player; return 
            
            if addon.USENOWPLAY:
                PBM = [PBTYPES_LIST[0], PBTYPES_LIST[3]]
                
                inf = tl(TAG_DLG_NPINFO).replace('**', NewLine) % (medinfo.title, medinfo.year, tl(TAG_DLG_NPINFRAT), medinfo.rating, tl(TAG_DLG_NPINFSRC), 
                prefixToName(url_prefix) if url_prefix else tl(TAG_DLG_NPDIRL), 
                tl(TAG_DLG_NPINFPBT), PBTYPES_LIST[PTYPE-1] if PTYPE else PBM[PBMETOD-1])
                
                nowPlay(inf, medinfo.img, addon.NOWPLAYTIME, pnTimer, player.isPlaying)
            
            ### Keep playback control while playback ...
            cp_totime = 0; cp_time = 0; cp_watched = 0   
            while player.isPlaying():
                
                ### Get playback position (skip if skipping by time is ON) ...
                if wtime1 >= addon.POSUPD and not possleep:
                    ### Cancel if file name was changed ...
                    if playing_file != player.getPlayingFile() : break
                    cp_time   = player.getTime()
                    cp_totime = player.getTotalTime()
                    cp_watched = medinfo.setpos(cp_time, cp_totime, addon.WPERC)
                    wtime1 = 0
                
                ### Inc. timer ...
                wait(1); wtime1 += 1
                
                ### Turn off skipping by time ...
                if wtime1 > addon.POSSLEEP : possleep = False
            
        ## End operations ...
        if PTYPE == 5 and playlist and cp_totime-cp_time < addon.POSUPD : player.play(playlist)
        
        wait(1); del listitem, player
        
        if PTYPE == 3: 
            wait(1) 
            if keepcontainer != LI.getCpath() : GUI.back()
    
        #if addon.USEWS and addon.ACSSTKN and cp_time : sync.dbxSync().watchSync(upload=True)
        if addon.USEWS and addon.ACSSTKN and (cp_time or cp_watched):
            dbx = sync.dbxSync()
            dbx.putChangesRecord(strmfile, cp_watched, cp_time, cp_totime, True if strmtype == str(TAG_TYP_MOV) else False)
            dbx.sendWatchedInfo()
            del dbx 
            
        #GUI.msg('>> END')
  
        
## Playlist restoring ...
def getPLI(playlist):
    if not playlist : return Empty
    vidItems = LI.vidItems()
    return vidItems.getOnlyNexts()

def setPLI(playlist, pli):
    if not pli : return
    playlist.clear()
    for itm in pli:
        playlist.add(itm)      


def nowPlay(text, img=Empty, showtime=5, pretime=0, stopIf=None):
    GUI.Thrd(GUI.dlgNowPlayX, text, img, showtime, pretime, stopIf)

## Arguments Parsing ...
def parseArgs():
    try    : argv1 = sys.argv[1]
    except : argv1 = Empty
    
    argv1 = int(argv1.replace(TAG_PAR_ACTION, Empty)) if argv1 and argv1.startswith(TAG_PAR_ACTION) else Empty  
    if argv1 : return [argv1] 
     
    kwargs = get_params()
    if not kwargs : return [TAG_CND_NOACTION] 
    callSTRM(**kwargs)
    return [TAG_CND_PLAY] 
    

## Get add-on params (as link) ...    
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


## Media info class ...
class CMedInfo:

    def __init__(self, fname, fname2, stype):
    
        self.fname   = fname
        self.fname2  = fname2
        self.type    = int(stype)
        self.id      = 0
        self.fid     = 0
        self.w       = 0
        self.pos     = 0
        self.path    = Empty
        self.patheps = Empty
        self.title   = Empty
        self.year    = Empty  
        self.rating  = Empty
        self.genre   = Empty
        self.plot    = Empty
        self.img     = Empty
        self.season  = Empty
        
        self.votes         = Empty 
        self.episode       = Empty
        self.showtitle     = Empty
        self.writer        = Empty
        self.originaltitle = Empty
        self.studio        = Empty
        self.mpaa          = Empty
        self.director      = Empty
        self.date          = Empty
        self.art           = Empty
        
        self.cast          = []
        self.castandrole   = []
        
        self.cmd_mov     = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "properties": ["file", "thumbnail", "title", "year", "rating", "genre", "plot", "country", "director", "originaltitle", "writer", "studio", "mpaa", "votes", "cast", "art"] },  "id": 1}'
        self.cmd_tvs_tvs = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": { "properties": ["file", "genre", "year", "studio", "mpaa"] },  "id": 1}'
        self.cmd_tvs_eps = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": { "properties": ["season", "plot", "file", "rating", "votes", "episode", "showtitle", "writer", "originaltitle", "director", "firstaired", "art", "cast"], "tvshowid":%s },  "id": 1}'
        self.cmd_tvs_sea = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetSeasons", "params": { "properties": ["season", "thumbnail"], "tvshowid":%s },  "id": 1}'
        
        self.cmd_mov_w   = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": { "properties": ["playcount", "resume"], "movieid":%s }, "id": 1}'
        self.cmd_tvs_w   = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": { "properties": ["playcount", "resume"], "episodeid": %s }, "id": 1}'
        
        self.cmd_set_mov = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid":%s, "resume": {"position":%s, "total":%s} }, "id": 1}'
        self.cmd_set_tvs = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid":%s, "resume": {"position":%s, "total":%s} }, "id": 1}'
        
        self.cmd_set_movw = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid":%s, "playcount": %s }, "id": 1}'
        self.cmd_set_tvsw = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid":%s, "playcount": %s }, "id": 1}'

        if   self.type == TAG_TYP_TVS : self.gettvs()
        elif self.type == TAG_TYP_MOV : self.getmov()
    
    
    def getmov(self):
       self.path = DOS.join(LIB.mov, self.fname2) 
       
       movList = self.js(self.cmd_mov, 'movies') 
       for mov in movList:
         if DOS.compath ( mov['file'], self.path ) : 
            self.img     = mov['thumbnail']
            self.title   = mov['title']
            self.year    = mov['year']  
            self.rating  = mov['rating']
            self.genre   = mov['genre']
            self.plot    = mov['plot']
            self.fid     = mov['movieid']
            self.country = mov['country']
            
            self.director      = mov['director']
            self.originaltitle = mov['originaltitle']
            self.writer        = mov['writer']
            self.studio        = mov['studio']
            self.mpaa          = mov['mpaa']
            self.votes         = mov['votes']
            self.art           = mov['art']
            cast               = mov['cast']
            
            for itm in cast: 
                self.cast.append(itm['name'])
                if itm['role'] : self.castandrole.append(itm['name'] + tl(TAG_TTL_CAST) % (itm['role']))
            
            break
            
       mvd = self.js(self.cmd_mov_w % self.fid, 'moviedetails')
       self.w      = mvd['playcount']
       self.pos    = mvd['resume']['position']
            
    
    def gettvs(self):
       self.path    = LIB.tvs(self.fname) 
       self.patheps = DOS.join(self.path, self.fname2)
    
       tvsList = self.js(self.cmd_tvs_tvs, 'tvshows') 
       for tvs in tvsList:
         if DOS.compath ( tvs['file'], self.path ) : 
            self.id      = tvs['tvshowid']
            self.genre   = tvs['genre']
            self.year    = tvs['year']
            self.country = Empty
            
            self.studio  = tvs['studio']
            self.mpaa    = tvs['mpaa']
            
            break
       
       epsList = self.js(self.cmd_tvs_eps % (self.id), 'episodes')
       for eps in epsList:    
         if DOS.compath ( eps['file'], self.patheps ) : 
            self.title  = eps['label']  
            self.rating = eps['rating']
            self.plot   = eps['plot']
            self.season = eps['season']
            self.fid    = eps['episodeid']  
            
            self.votes         = eps['votes']
            self.episode       = eps['episode']
            self.showtitle     = eps['showtitle']
            self.writer        = eps['writer']
            self.originaltitle = eps['originaltitle']
            self.director      = eps['director']
            self.date          = eps['firstaired']
            self.art           = eps['art']
            cast               = eps['cast']
            
            for itm in cast: 
                self.cast.append(itm['name'])
                if itm['role'] : self.castandrole.append(itm['name'] + tl(TAG_TTL_CAST) % (itm['role']))
            
            break
             
       seaList = self.js(self.cmd_tvs_sea % (str(self.id)), 'seasons')
       for sea in seaList:
            if sea['season'] == self.season : self.img = sea['thumbnail']
       
       epd = self.js(self.cmd_tvs_w % self.fid, 'episodedetails')
       self.w = epd['playcount']
       self.pos = epd['resume']['position']
       
    
    def js(self, cmd, key):
        return eval(xbmc.executeJSONRPC(cmd))['result'][key]
                
    def setpos(self, pos, total, wperc=0):
    
        if self.w : return 1
    
        if   self.type == TAG_TYP_TVS : cmd = self.cmd_set_tvs; cmd2 = self.cmd_set_tvsw 
        elif self.type == TAG_TYP_MOV : cmd = self.cmd_set_mov; cmd2 = self.cmd_set_movw
        
        watched = 0
        
        if addon.WCHF and wperc:
            if total > 0 and 1.0*pos/total*100 > wperc : 
                xbmc.executeJSONRPC(cmd2 % (str(self.fid), '1'))
                pos = total = 0
                watched = 1
            #else : xbmc.executeJSONRPC(cmd2 % (str(self.fid), '0'))        
        
        self._setpos(cmd, pos, total)
        
        return watched
        
    def _setpos(self, cmd, pos, total):
        xbmc.executeJSONRPC(cmd % (str(self.fid), str(pos), str(total)))
        
    def resetpos(self):
        self.pos = 0
        self.setpos(0, 0, 0)


class playersTable():

    def __init__(self, strmurl=Empty):
        self._SEP1 = TAG_PAR_TVSPACK_LSEP
        self._SEP2 = TAG_PAR_TVSPACK_SSEP + NewLine
        
        self._file_name = TAG_PAR_PTYPETABLE_FILE
        self._path      = addon.libpath
    
        self.strmurl = strmurl
        self.pTable  = [] 
        self.loadTable()
    
    def getPType(self):
        if not self.strmurl : return -2
        if not self.pTable  : return -1 
        for plug, num in self.pTable:
            if self.strmurl.startswith(plug) : return int(num)
        return -1
    
    def setPType(self, plug, ptype):
        newType = True
        if self.pTable:
            for idx, rec in enumerate(self.pTable): 
                if rec[0] == plug: 
                    self.pTable[idx][1] = str(ptype)
                    newType = False
                    break
                   
        if newType : self.pTable.append([plug, str(ptype)])
        self.saveTable()
    
    def removePType(self, plug):
        if self.pTable:
            for idx, rec in enumerate(self.pTable): 
                if rec[0] == plug: 
                    self.pTable.pop(idx)
                    break
                    
        self.saveTable()
    
    def loadTable(self):
        unpack = DOS.file(self._file_name, self._path, fType=FRead)
        if unpack == -1 or not unpack : return
        self.pTable = [rec.split(self._SEP1) for rec in unpack.split(self._SEP2)]  
    
    def saveTable(self):
        pack = self._SEP2.join([self._SEP1.join([rec1, rec2]) for rec1, rec2 in self.pTable]) 
        DOS.file(self._file_name, self._path, pack, FWrite) 
    
    def getall(self):
        if self.pTable : return [rec[0] for rec in self.pTable], [rec[1] for rec in self.pTable] 
        else           : return Empty, Empty

## Get source add-on name (URL prefix) ... 
def getURLPrefix(strmurl):
    prefix  = Empty
    PPREFIX = 'plugin://'
    if strmurl.startswith(PPREFIX):
        tmpURL = strmurl.replace(PPREFIX, Empty)
        fidx   = tmpURL.find('/')
        if fidx > 0 : prefix = PPREFIX + tmpURL[:fidx+1]
    
    return prefix   

def prefixToName(url_prefix):
    turl = url_prefix
    turl = turl.replace('plugin://plugin.', Empty)
    turl = turl.replace('video.', Empty)
    turl = turl.replace('/', Empty)
    turl = turl.replace('.', Space)
    turl = setCapAll(turl)
    return turl    
        
                 
        
        
         