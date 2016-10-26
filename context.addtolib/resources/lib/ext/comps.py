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
########## COMPS:

### Import modules ...
from base import *


##### Patterns for file and folder names ...
class PATTERN:
    remove_tags         = ur'\[[^\[\]]*\]'
    file_remove_spch    = ur'[/\\<>:"\|\?\* \t\n\r\u200f]+'
    folder_remove_spch  = ur'[/\\<>:"\|\?\* \t\n\r\u200f]+'
    file_remove_ext     = ur'\.[^.]{1,3}$'
    folder_name_by_file = ur'(.+)([sS]{1}[.]?[\d]+[.]?[eE]{1}[.]?[\d]+)'
    season_and_eps      = ur'([sS]{1}[.]?[\d]+[.]?[eE]{1}[.]?[\d]+)'
    season_only         = ur'([\d]+)'   
    clear_name_by_file  = ur'[^a-zA-ZА-Яа-я\d)]+$'
    remove_fdots        = ur'^[.]+'
    remove_edots        = ur'[.]+$'
    remove_multidots    = ur'[.]{2,}'
    @staticmethod
    def file_remove_ext2 () : return '(\\'+'$)|(\\'.join(TAG_PAR_VIDEOSEXT)+'$)'
    @staticmethod
    def add_season (season, episode): return 's{:0>2}e{:0>2}.'.format(season, episode)
    @staticmethod
    def add_seq    (episode)        : return '{:0>2}.'.format(episode)

### Remove xbmc tags from text ...
compsRemtag = lambda  arg : re.compile(PATTERN.remove_tags).sub(Empty, arg)

##### To create file and folder names ...
def create_name (comps_item, *args, **kwargs):

        sw = {arg for arg in args}
        sw.update([TAG_TYP_ALL])
        
        if sw.issuperset({TAG_TYP_ALL}):
                
                comps_item.lower()
                comps_item.sub (PATTERN.remove_tags)   
        
        
        if sw.issuperset({TAG_TYP_ALL, TAG_TYP_TVS}):
        
                #comps_item.sub   (PATTERN.remove_tags)
                pass
        
        
        if sw.issuperset({TAG_TYP_FOLDER}):
        
                comps_item.sub   (PATTERN.folder_remove_spch, Dot)
        
        
        if sw.issuperset({TAG_TYP_FOLDER, TAG_TYP_TVS}):
        
                comps_item.match (PATTERN.folder_name_by_file)
                comps_item.sub   (PATTERN.clear_name_by_file)
        
        
        if sw.issuperset({TAG_TYP_SRC}):
        
                preSub = comps_item ()
                
                if kwargs['season'] : season = kwargs['season']
                else: 
                    seasoneps = comps(comps_item.search(PATTERN.season_and_eps))
                    season    = seasoneps.search(PATTERN.season_only)
                    del seasoneps 
                  
                comps_item.sub   (PATTERN.folder_name_by_file)
                comps_item.sub   (PATTERN.file_remove_ext)
                comps_item.sub   (PATTERN.remove_fdots) 
                
                tmp_season = Empty
                tmp_discr  = Empty
                
                if season               : tmp_season = ' * %s: %s' % ('Season', season)
                if preSub != comps_item : tmp_discr  = ' (%s)'   % (comps_item())
                
                srcname = kwargs['srcFolder']
                srcname = srcname.replace(tmp_season, Empty)
                srcname = srcname.replace(tmp_discr, Empty)
                
                comps_item(srcname + tmp_discr + tmp_season)
        
            
        if sw.issuperset({TAG_TYP_PREFILE}):
        
              comps_item.recompile(PATTERN.file_remove_spch)
        
        
        if sw.issuperset({TAG_TYP_FILE}):
        
                #comps_item.sub   (PATTERN.file_remove_ext)
                comps_item.sub   (PATTERN.file_remove_ext2())
                
                if kwargs:
                        if   kwargs['Seq']    == True  : comps_item.add(PATTERN.add_seq   (kwargs['Episode']))
                        elif kwargs['Season'] != Empty : comps_item.add(PATTERN.add_season(kwargs['Season'], kwargs['Episode'])) 
                comps_item.sub_compiled(Dot, toself=True)
                
                comps_item.sub   (PATTERN.remove_multidots, rep_text=Dot) 
                comps_item.sub   (PATTERN.remove_fdots)
                comps_item.sub   (PATTERN.remove_edots)


def create_name_once (notFormatedName, *args, **kwargs):
    cmpsName = comps(notFormatedName)
    create_name(cmpsName, *args, **kwargs)
    FormatedName = cmpsName()
    del cmpsName
    return FormatedName


##### Simple RE Object for file and folder names ...
class comps:

    def __init__ (self, data=Empty):
        self.class_data    = data 
        
    def recompile (self, pattern):
        self.class_compile = re.compile(pattern)
    
    def match (self, pattern):
        tmp_match = re.compile(pattern).match(self.class_data)
        self.class_data = tmp_match.group(1) if tmp_match is not None else Empty
    
    def match_compiled (self):
        tmp_match = self.class_compile.match(self.class_data)
        return tmp_match.group(1) if tmp_match is not None else Empty

    def sub (self, pattern, rep_text=Empty):
        self.class_data = re.compile(pattern).sub(rep_text, self.class_data)
        
    def sub_compiled  (self, rep_text=Empty, toself=False):
        if toself : self.class_data = self.class_compile.sub(rep_text, self.class_data)
        else : return self.class_compile.sub(rep_text, self.class_data)
        
    def search(self, pattern):
        tmp_search = re.compile(pattern).search(self.class_data)
        return tmp_search.group(0) if tmp_search is not None else Empty
    
    def add (self, data):
        self.class_data = data + self.class_data
    
    def lower(self):
        self.class_data = setLower(self.class_data)
    
    def isempty(self):
        return True if self.class_data == Empty else False 
    
    def clear (self):
        self.class_data = Empty
        
    def __call__ (self, data=Empty):
        if data != Empty : self.class_data = data 
        else: return self.class_data 
 
