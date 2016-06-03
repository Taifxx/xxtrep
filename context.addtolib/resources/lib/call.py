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
import sys
import xbmc
import xbmcgui
import xbmcplugin
import subprocess

from resources.lib.ext import *

class CPlayer(xbmc.Player):

    def __init__(self):
        xbmc.Player.__init__( self, xbmc.PLAYER_CORE_AUTO )
    
    def wait_openlink(self, splash):
        spath = setLower(splash)
        wtime = 0
        errc  = 0
        while True: 
            #if self.isPlayingVideo() and spath != setLower(self.getPlayingFile()) : break
            if self.isPlaying() and spath != setLower(self.getPlayingFile()) : break  
            wait(1); wtime += 1
            if wtime > addon.LNKTIMEOUT : return False
            #if self.isPlaying() and not self.isPlayingVideo() : errc += 1 
            if errc > 2 : return False
            
        return True
    
    def wait_buffering(self):
        wait(1); _oldpos = self.getTime() if self.isPlaying() else 0 
        while self.isPlaying() and _oldpos == self.getTime(): wait(1) 
        
    def seek(self, pos):
        if addon.WAITBSEEK : wait(addon.WAITBSEEK) 
        if self.isPlaying() : self.seekTime(pos)
        #GUI.seekPlay(pos)     
    
        
def simplerun(strmurl):
    listitem = xbmcgui.ListItem (path=strmurl)
    listitem.setProperty('IsPlayable', 'true')
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    GUI.msg(tl(TAG_ERR_DEFEPS))


def callSTRM(strmtype, strmurl, strmfile):

    GUI.stopPlay()
    
    CLASSICPLAY = not addon.NEWPLAYS

    player = CPlayer()
    
    prePath = LIB.tvsf if strmtype == str(TAG_TYP_TVS) else LIB.mov
    
    if not DOS.exists(DOS.join(prePath, strmfile)):
    
        simplerun(strmurl)
    
    else:
    
        strmfileS = DOS.getdir(strmfile)
        strmfldrS = DOS.getdir(DOS.gettail(strmfile))
        
        try:
         
            medinfo = CMedInfo(strmfldrS, strmfileS, strmtype)
            
            listitem = xbmcgui.ListItem (path=strmurl)
            listitem.setProperty('IsPlayable', 'true')
            listitem.setArt(medinfo.art)
            listitem.setIconImage(medinfo.img)
            listitem.setThumbnailImage(medinfo.img)
            
            splashPath = Empty
            
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
            
            listitem.setInfo('video', infpar)
        
        except : simplerun(strmurl); return
        
        if not CLASSICPLAY:
            splashPath = DOS.join(addon.path, *TAG_PAR_SPLASH_FILE)
            splashLI = xbmcgui.ListItem (path=splashPath)
            splashLI.setProperty('IsPlayable', 'true')
            splashLI.setArt(medinfo.art)
            splashLI.setIconImage(medinfo.img)
            splashLI.setThumbnailImage(medinfo.img)
            splashLI.setInfo('video', infpar)
            splashLI.setInfo('video', {'Title':Space}) 
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, splashLI)
            GUI.FocusPayer()
            wait(1) 
        
        if CLASSICPLAY  : xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        else            : player.play(strmurl, listitem)
        
        if not player.wait_openlink(splashPath) : 
            GUI.dlgOk(tl(TAG_ERR_DEDLINK), title=medinfo.title)
            return
        
        wait(1); GUI.FocusPayer()
        
        eodgenMethod = addon.EODGENM 
        if   eodgenMethod == 'Handle reset' : xbmcplugin.endOfDirectory(int(sys.argv[1]), True, False, False)
        elif eodgenMethod == 'Suppression'  : GUI.closeDlgs()
    
        wtime1 = 0
        possleep = True
        if addon.PLAYBCONT:
        
            pbSet = False
            fargs = timefromsec(medinfo.pos, TAG_PAR_TIMENUMFORMAT, TAG_PAR_TIMESEP)
            if addon.RESDLG and medinfo.pos and not addon.AUTORES:
                pbm = GUI.dlgResume([tl(TAG_MNU_SFRBEGIN), tl(TAG_MNU_RFROM) % (fargs[0],fargs[1],fargs[2],fargs[3],fargs[4]), tl(TAG_MNU_CLOSEDLG)], title=medinfo.title)     
                if   pbm == 0 : pbSet = True; medinfo.resetpos()
                elif pbm == 1 : pbSet = True
                elif pbm == 2 : pbSet = False
            
            if (addon.AUTORES or pbSet) and medinfo.pos : player.seek(medinfo.pos) 
            
            player.wait_buffering()
              
            while player.isPlaying():
                
                if wtime1 >= addon.POSUPD and not possleep : medinfo.setpos(player.getTime(), player.getTotalTime(), addon.WPERC); wtime1 = 0
                wait(1); wtime1 += 1
                if wtime1 > addon.POSSLEEP : possleep = False
             

def parseArgs():
    try    : argv1 = sys.argv[1]
    except : argv1 = Empty
    if argv1 and argv1.startswith(TAG_PAR_ACTION) : return int(argv1.replace(TAG_PAR_ACTION, Empty))
    kwargs = get_params()
    if not kwargs : return TAG_CND_NOACTION
    callSTRM(**kwargs)
    return TAG_CND_PLAY 
    
    
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
        
        self.cmd_mov_w   = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": { "properties": ["playcount"], "movieid":%s }, "id": 1}'
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
    
        if self.w : return
    
        if   self.type == TAG_TYP_TVS : cmd = self.cmd_set_tvs; cmd2 = self.cmd_set_tvsw 
        elif self.type == TAG_TYP_MOV : cmd = self.cmd_set_mov; cmd2 = self.cmd_set_movw
        
        if addon.WCHF and wperc:
            if total > 0 and 1.0*pos/total*100 > wperc : 
                xbmc.executeJSONRPC(cmd2 % (str(self.fid), '1'))
                pos = total = 0
            #else : xbmc.executeJSONRPC(cmd2 % (str(self.fid), '0'))        
        
        self._setpos(cmd, pos, total)
        
    def _setpos(self, cmd, pos, total):
        xbmc.executeJSONRPC(cmd % (str(self.fid), str(pos), str(total)))
        
    def resetpos(self):
        self.pos = 0
        self.setpos(0, 0, 0)
        
         