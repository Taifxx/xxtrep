﻿# -*- coding: utf-8 -*-
#
#     Copyright (C) 2011-2014 Martijn Kaijser
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
########## DEFINE TAGS:

### Params ...
TAG_PAR_LIB_FOLDER          = 'LIB'

TAG_PAR_TMP                 = '.TMP'
TAG_PAR_TMPA                = '.TMPA'

TAG_PAR_DEFAULT_DEBUG_FILE  = '__debug1'
TAG_PAR_DEFAULT_DEBUG_EXT   = '.debf'

TAG_PAR_SCRIPT_ID           = 'context.addtolib'
TAG_PAR_SERVICE_PY          = 'service.py'
TAG_PAR_ADDON_PY            = 'context.py'
TAG_PAR_SERVICE             = 'special://home/addons/%s/%s' % (TAG_PAR_SCRIPT_ID, TAG_PAR_SERVICE_PY)
TAG_PAR_ADDON               = 'special://home/addons/%s/%s' % (TAG_PAR_SCRIPT_ID, TAG_PAR_ADDON_PY)
TAG_PAR_STRINGSXML_PATH     = ['resources','language','english']
TAG_PAR_STRINGSXML_FILE     = 'strings.xml'
TAG_PAR_TVSPACK_FILE        = 'tvs.pack'
TAG_PAR_TVSRAWFILE          = 'tvs.eraw'
TAG_PAR_STL_FILE            = 'linktable'
TAG_PAR_TVSUPD_FILE         = '.tvsupd'
TAG_PAR_TVSUPDNOW_FILE      = '.updnow'
TAG_PAR_LOCKF               = '.lock'
TAG_PAR_STRARTF             = '.start'
TAG_PAR_STRARTAF            = '.act'
TAG_PAR_FSET_FILE           = 'fset'
TAG_PAR_COLORS_FILE         = 'colors'
TAG_PAR_TVSDEFSEASON        = '01' 
TAG_PAR_VIDEOSEXT           = ['.avi', '.mpeg', '.wmv', 'asf', '.flv', '.mkv', '.mka', '.mp4', '.m4a', '.aac', '.ogg', '.ogm', '.ram', '.rm', '.rv', '.ra', '.rmvb', '.3gp']
TAG_PAR_SETDEF              = 'Default'
TAG_PAR_RESFOLDER           = 'resources'
TAG_PAR_IMGFOLDER           = 'img'
TAG_PAR_BSFOLDER            = 'bs'
TAG_PAR_MNUCOLORFORMAT      = '[COLOR %s]%s[/COLOR]'
TAG_PAR_COLORTAG            = '##COLOR##'
TAG_PAR_ADDONLABEL_TMPL     = '<string id="29999">%s</string>'
TAG_PAR_ADDONLABEL_PATT     = TAG_PAR_ADDONLABEL_TMPL % ('(.*)')
TAG_PAR_ADDONLABEL          = TAG_PAR_ADDONLABEL_TMPL % ('ADD to [COLOR %s]Lib[/COLOR]')
TAG_PAR_ZIPCN               = 'CN'
TAG_PAR_ZIPST               = 'atl.backup.'
TAG_PAR_ZIPTMPL             = TAG_PAR_ZIPST + '%s.%s.'+ TAG_PAR_ZIPCN + '.zip'

### XML
TAG_PAR_XMLW_SELDLG         = 'XDialogSelect.xml' 


### Help ...
TAG_PAR_BKG                 = 'bkg.png'
TAG_PAR_LN                  = 'line.png'
TAG_PAR_XBMCTAGQ            = '[]'
TAG_PAR_HELPFILE            = 'help.'
TAG_PAR_HLPFOLDER           = 'help'
TAG_PAR_HLPBORDERSIZE       = 20
TAG_PAR_HLPSCROLL           = 5

TAG_PAR_RESX                = 1280
TAG_PAR_RESY                = 720

### Time ...
TAG_PAR_TIMENUMFORMAT       = '{:0>2}'
TAG_PAR_TIMESEP             = ':'

### URL ...
TAG_PAR_CALLURLTMPL         = 'plugin://%s//?#strmtype=#%s&#strmfile=#%s&#strmurl=#'
TAG_PAR_REPFN               = '%s'
TAG_PAR_ACTION              = 'action='

### tvs.pack separators ...
TAG_PAR_TVSPACK_LSEP        = '<**LSTSEP**>'
TAG_PAR_TVSPACK_SSEP        = '<**SRCSEP**>'
TAG_PAR_TVSPACK_FSEP        = '<**FRCSEP**>'
TAG_PAR_TVSPACK_ESEP        = '<**EPSSEP**>'
TAG_PAR_TVSPACK_PSEP        = '<**PRTSEP**>'

### Containers starts with ...
TAG_CON_STARTSW_EXT         =  'plugin:'
TAG_CON_STARTSW_VID         =  'videodb:'
TAG_CON_STARTSW_PVD         =  'playlistvideo:'

### Const Tags ...
DEFAULT                 = 10000
TAG_DEBUG_FILE_PATH     = DEFAULT

### Types ...
TAG_TYP_ALL             = 10001
TAG_TYP_MOV             = 10002
TAG_TYP_TVS             = 10003
TAG_TYP_SRC             = 10004
TAG_TYP_FOLDER          = 10005
TAG_TYP_PREFILE         = 10006
TAG_TYP_FILE            = 10007

### Containers ...
TAG_CON_LOCAL           = 10071
TAG_CON_EXT             = 10072
TAG_CON_VID             = 10073
TAG_CON_PVD             = 10074

TAG_CND_FOUND           = 10075
TAG_CND_NOTFOUND        = 10076
TAG_CND_LISTEMPTY       = 10077
TAG_CND_NEWSRC          = 10078
TAG_CND_OLDSRC          = 10079
TAG_CND_NOUPD           = 10080
TAG_CND_NEWFRC          = 10081
TAG_CND_OLDFRC          = 10082
TAG_CND_UPDPRC          = 10083
TAG_CND_NOUPDPRC        = 10084
TAG_CND_NOGL            = 10085
TAG_CND_NOACTION        = 10086
TAG_CND_PLAY            = 10087

### Free actions ...
TAG_ACT_LPRESET         = 10200
TAG_ACT_SHADOWUPD       = 10201
TAG_ACT_DONOTHING       = 10202
TAG_ACT_CHCOLOR         = 10203
TAG_ACT_RENAMER         = 10204
TAG_ACT_BACKUP          = 10205
TAG_ACT_REMBACK         = 10206
TAG_ACT_RESTBACK        = 10207
TAG_ACT_RESETTBU        = 10208
TAG_ACT_AUTOBACKUP      = 10209

### Language ...
TAG_LNG_ID              = 30000

### Menue ...
TAG_MNU_MOV             = 30001
TAG_MNU_TVS             = 30002
TAG_MNU_TVSU            = 30003
TAG_MNU_OPEN            = 30004
TAG_MNU_RESCAN          = 30005                             
TAG_MNU_REMSRC          = 30006
TAG_MNU_RESTORE         = 30007
TAG_MNU_DELETE          = 30008
TAG_MNU_VIDLIBU         = 30009
TAG_MNU_CHKNEW          = 30010
TAG_MNU_JOIN            = 30011
TAG_MNU_TVSREN          = 30012
TAG_MNU_SRCREN          = 30013
TAG_MNU_UPDMAN          = 30014
TAG_MNU_ADDEXIST        = 30015
TAG_MNU_ADDNEW          = 30016
TAG_MNU_SM              = 30017
TAG_MNU_SHOWALL         = 30018
TAG_MNU_SRCMAN          = 30019
TAG_MNU_TVSMAN          = 30020
TAG_MNU_QR              = 30021
TAG_MNU_QL              = 30022
TAG_MNU_NEW             = 30023
TAG_MNU_ADDFOL          = 30024
TAG_MNU_SRE             = 30025
TAG_MNU_UPDFOL          = 30026
TAG_MNU_VIDLIBCLN       = 30027
TAG_MNU_SHDIR           = 30028
TAG_MNU_REBSTL          = 30029
TAG_MNU_DEFNMMOV        = 30030
TAG_MNU_NEWNMMOV        = 30031
TAG_MNU_ATVSNM          = 30032
TAG_MNU_ATVSNUMT        = 30033
TAG_MNU_ATVSNUM         = 30034
TAG_MNU_DEFNM           = 30035
TAG_MNU_SEQNUM          = 30036
TAG_MNU_SEANUM          = 30037
TAG_MNU_STARTADD        = 30038
TAG_MNU_ATVS            = 30039
TAG_MNU_ATVSSERT        = 30040
TAG_MNU_SERDEF          = 30041
TAG_MNU_SERTPL          = 30042
TAG_MNU_SEASON          = 30043
TAG_MNU_RFROM           = 30044
TAG_MNU_SFRBEGIN        = 30045
TAG_MNU_ADVADD          = 30046
TAG_MNU_CHKNEWGL        = 30047
TAG_MNU_RESTOREALL      = 30048
TAG_MNU_SMM             = 30049
TAG_MNU_RAWADD          = 30050
TAG_MNU_BRWSREN         = 30051
TAG_MNU_CONTUPD         = 30052
TAG_MNU_RESCANALLS      = 30053
TAG_MNU_RESCANFULL      = 30054

TAG_MNU_MORE            = 30090
TAG_MNU_BACKMAIN        = 30091
TAG_MNU_OK              = 30092
TAG_MNU_HELP            = 30096
TAG_MNU_SET             = 30097
TAG_MNU_BACK            = 30098
TAG_MNU_CANCEL          = 30099

### Confirms ...
TAG_CFR_RESCAN          = 30071
TAG_CFR_REMSRC          = 30072                            
TAG_CFR_RESTORE         = 30073
TAG_CFR_DELETE          = 30074
TAG_CFR_TVSREN          = 30075
TAG_CFR_JOIN            = 30076
TAG_CFR_CLEANVL         = 30077
TAG_CFR_DEFNM           = 30078
TAG_CFR_RESTOREALL      = 30079
TAG_CFR_RESCANALLS      = 30080
TAG_CFR_RESCANFULL      = 30081
TAG_CFR_RENAMER         = 30082
TAG_CFR_UNLOCK          = 30083
TAG_CFR_REMBACK         = 30084
TAG_CFR_RESTBACK        = 30085

### Dialogs messages ...
TAG_DLG_OK              = 30100
TAG_DLG_NX              = 30101  
TAG_DLG_PR              = 30102
TAG_DLG_INNM            = 30103 
TAG_DLG_INSE            = 30104

### Titles ...
TAG_TTL_NM              = 30150
TAG_TTL_ENTNAME         = 30151
TAG_TTL_CHSNAME         = 30152
TAG_TTL_ADDTVS          = 30153
TAG_TTL_NEWEPS          = 30154
TAG_TTL_EXITVS          = 30155
TAG_TTL_CHKUPD          = 30156
TAG_TTL_ADDMOV          = 30157
TAG_TTL_ENTNAMEM        = 30158
TAG_TTL_ADVADD          = 30159
TAG_TTL_RESTOREALL      = 30160
TAG_TTL_CHKUPDGL        = 30161
TAG_TTL_POSHLP          = 30162
TAG_TTL_CAST            = 30163
TAG_TTL_BRWSREN         = 30164
TAG_TTL_BRWSRENEP       = 30165
TAG_TTL_COLORIZE        = 30166
TAG_TTL_SEASON          = 30167
TAG_TTL_BACKUP          = 30168
TAG_TTL_RESTBACK        = 30169
TAG_TTL_RESTLIB         = 30170
TAG_TTL_RESTRL          = 30171
TAG_TTL_RESTUL          = 30172
TAG_TTL_RESTCHK         = 30173
TAG_TTL_BCKNM           = 30174
TAG_TTL_RESTAT          = 30175
TAG_TTL_RESTATC         = 30176
TAG_TTL_RESTRTMP        = 30177
TAG_TTL_PACK            = 30178
TAG_TTL_REMOLDBCK       = 30179
TAG_TTL_CLRERRDT        = 30180
TAG_TTL_CLRERRD         = 30181

TAG_SET_RENAMER         = 30436

### Ok messages ...
TAG_ERR_OK              = 30301 
TAG_ERR_OK_MOVADD       = 30302 
TAG_ERR_OK_TVSADD       = 30303 
TAG_ERR_OK_TVSUPD       = 30304 
TAG_ERR_OK_RESCAN       = 30305 
TAG_ERR_OK_RESTOR       = 30306
TAG_ERR_OK_REMSRC       = 30307
TAG_ERR_OK_DELETE       = 30308  
TAG_ERR_OK_CHKNEW       = 30309
TAG_ERR_OK_TVSREN       = 30310
TAG_ERR_OK_SRCREN       = 30311
TAG_ERR_OK_JOIN         = 30312
TAG_ERR_OK_ADDFOL       = 30313
TAG_ERR_OK_UPDFOL       = 30314
TAG_ERR_OK_SETUPD       = 30315
TAG_ERR_OK_VIDLIBU      = 30316
TAG_ERR_OK_REBSTL       = 30317
TAG_ERR_OK_RESTOREALL   = 30318
TAG_ERR_OK_BRWSREN      = 30319
TAG_ERR_OK_NEWFRC       = 30320
TAG_ERR_OK_RESCANALLS   = 30321
TAG_ERR_OK_RESCANFULL   = 30322
TAG_ERR_OK_RENAMER      = 30323
TAG_ERR_OK_BACKUP       = 30324
TAG_ERR_OK_REMBACK      = 30325
TAG_ERR_OK_RESTBACK     = 30326
TAG_ERR_OK_NOBACK       = 30327

### Errors ...
TAG_ERR_NOTFILE         = 30201
TAG_ERR_INCINPUT        = 30202
TAG_ERR_LISTEMPTY       = 30203
TAG_ERR_ABORT           = 30204
TAG_ERR_NOTOJOIN        = 30205
TAG_ERR_DEDLINK         = 30206
TAG_ERR_NONAME          = 30207
TAG_ERR_NONAME2         = 30208
TAG_ERR_DEFEPS          = 30209
TAG_ERR_BROKENLINK      = 30210
TAG_ERR_BROKENLINK2     = 30211
TAG_ERR_LIB             = 30212
TAG_ERR_LIBACT          = 30213
TAG_ERR_LOCK            = 30214
TAG_ERR_OL              = 30215
TAG_ERR_BADZIP          = 30216
TAG_ERR_NOBCKPATH       = 30217
TAG_ERR_NOBCKPATHM      = 30218

