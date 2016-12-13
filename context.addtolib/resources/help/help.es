[COLOR grey](apologies for the translation)[/COLOR]

Add-on to add links to the TV shows and movies in [COLOR ##COLOR##]Kodi[/COLOR] video library from other add-ons.

Add-on creates links to episodes and movies as [COLOR ##COLOR##].strm[/COLOR] files and places them in folders [COLOR ##COLOR##]'TV shows'[/COLOR] and [COLOR ##COLOR##]'Movies'[/COLOR]. To add you need focuses on playable link to movie file or to be in a folder containing the TV show episodes (season of TV show), open the context menu and use [COLOR ##COLOR##]'Add to Lib'[/COLOR] menu item.

Add-on creates [COLOR ##COLOR##].strm[/COLOR] files into local folders [COLOR ##COLOR##]'TV Shows'[/COLOR] and [COLOR ##COLOR##]'Movies'[/COLOR] (as default). Path: <home folder> \ userdata \ addon_data \ context.addtolib \ LIB \. You can change the folder names in the [COLOR ##COLOR##]add-on settings[/COLOR].


    [B][COLOR ##COLOR##](!)[/COLOR][/B]   You must one-time add folders [COLOR ##COLOR##]'TV shows'[/COLOR] and [COLOR ##COLOR##]'Movies'[/COLOR] as sources in the Kodi video library, and choose scrapers for them.


[B]Adding movie:[/B]

To add a movie, you need focuses on playable link to movie file, open the context menu and use [COLOR ##COLOR##]'Add to Lib'[/COLOR] menu item. In add-on menu select [COLOR ##COLOR##]'Add to library as a movie'[/COLOR].  After action, the movie will be added to the [COLOR ##COLOR##]'Movies'[/COLOR] folder (default).


[B]Adding episodes (season):[/B]

To add the episodes  (TV show season), you need to be in a folder containing playable links to episodes files, open context menu of any of episodes and select [COLOR ##COLOR##]'Add to Lib'[/COLOR]. In add-on menu select [COLOR ##COLOR##]'Add to library as TV show season'[/COLOR]. 

When add-on was able to determine name of the TV show and this TV show has exists, the episodes will be added to an existing TV show. Item [COLOR ##COLOR##]'Update episodes'[/COLOR] is used to add new episodes from source to the already added episodes.

When you add episodes of new or exists TV show automatically added [COLOR ##COLOR##]'episodes source'[/COLOR] (a link to the folder from which you add episodes). The add-on can scan this folder (source) and report about new episodes. One TV show may include a plurality of sources. The sources are managed in [COLOR ##COLOR##]'source management'[/COLOR] menu item.

For the TV show manually can be added [COLOR ##COLOR##]'seasons source'[/COLOR] (a link to folder containing a list of the seasons of the TV show). In this case, the add-on will scan folder for the presence of the new season.

TV show are managed in [COLOR ##COLOR##]'TV show management'[/COLOR] menu item.


[B]Update episodes (seasons) manually:[/B]

To check update of the current TV show, select [COLOR ##COLOR##]'Check for new episodes'[/COLOR]. To check all TV shows you need using [COLOR ##COLOR##]'Global check for updates'[/COLOR] menu item. If updates are detected, the add-on will display a list of them. If you select source of proposed update, the update will take place automatically.

You can disable check for new episodes or seasons in [COLOR ##COLOR##]'update management'[/COLOR] menu item.


[B]Update episodes (seasons) automatically:[/B]

To check update of the all TV shows in background mode (or during Kodi startup), you need turn-on this options in add-on settings. If add-on find new seasons in sources, add-on will show you appropriate message. Use 'Continue las update' to see it.  

On your choise you can set semiautomatic update mode disabling some update options in add-on settings. 


[B]Callable URL:[/B]

In this add-on is realized the possibility of obtaining full information from the library for playable [COLOR ##COLOR##].strm[/COLOR] files (posters, fan art, progress, etc.). To use this feature is necessary to create links into [COLOR ##COLOR##].strm[/COLOR] files that call this add-on when playing a file. In the case of playing [COLOR ##COLOR##].strm[/COLOR] file with callable link during playback will be available to the data of the episode, TV show, a feature to store the position and [COLOR ##COLOR##]'Watched status'[/COLOR].

You can enable or disable this feature in the add-on settings.

If you want to receive information about the currently playing movie (episode), but do not want to use a storing of current position and [COLOR ##COLOR##]'Watched status'[/COLOR] (may increase the load on the processor), disable the [COLOR ##COLOR##]'Playback control'[/COLOR] in add-on settings.


    [B][COLOR ##COLOR##](!)[/COLOR][/B]   When you enable (disable) the option [COLOR ##COLOR##]'Callable URL'[/COLOR], there is no change in URL into the previously created [COLOR ##COLOR##].strm[/COLOR] files. To create a new 
            files with a simple or callable URL by use [COLOR ##COLOR##]'Restore TV show'[/COLOR] or [COLOR ##COLOR##]'Restore all TV shows'[/COLOR] menu items.


[B]Using CORE:[/B]

Typically for most users, leave the 'Player CORE' in add-on settings as 'Default'. If user uses modified playcorefactory.xml then the CORE change makes sense.

In all playback types except alternate changes in CORE only affects the interaction of ADD To Lib and player. I.e. if user has changed default player and he had problems with playback control module than it is necessary to set CORE settings.

If user additionally uses a certain player in playcorefactory.xml then to play with this player you need to choose 'Alternative' playback type and to specify the desired CORE. If CORE is not in the list, you must select 'Custom' and specify the number manually.


    [B][COLOR ##COLOR##](!)[/COLOR][/B]   If you select wrong CORE may result in an error. CORE Auto is not available for Kodi 17, and CORE VideoPlayer is not available for 
            Kodi 15.


[B]Playback types:[/B]

Playback modes are used to work with Addons that do not support the standard (classic) method of playing. For example, attempting to launch a window appears 'Open stream', you see a black screen and interface freezes, plays the wrong file, etc.

To work with the playback modes, in add-on settings 'Playback type as default'  should be selected as 'Predefined'. In this case, if  playback type is already selected for addon-source, system will automatically start the playback, if not, prompts user to select type. Option 'autodetect' will allow system to try to automatically determine the appropriate type.


    [B][COLOR ##COLOR##](!)[/COLOR][/B]   During 'autodetect' interface might freeze for 3-15 seconds.
    

Classic and Alternative types – standard types to play. An alternative type may resolve some of problems with the launching of problem Addons.

ISP (Internal source player) allows to start playback with internal addon player. It should be noted that information about media content (title, cover, roles, etc.) are transferred to player from source addon.

ISP-Transmition - extended ISP. Use it if ISP don't work correctly. 

Catalog type – using ISP, but allowing choice of movie (series) in the library to open addon folder with link to a file. If You need to add a movie (TV series) to run in this mode, you need use 'forced adding' and add folder, not file itself.


[B]Sync:[/B]

Starting with version 1.0.12 ADD to Lib allows for [COLOR ##COLOR##]sync[/COLOR] video database and watched statuses with [COLOR ##COLOR##]Dropbox[/COLOR]. Thus, multiple remotely located devices unable to change video database and watched statuses without server.

To sync with Dropbox, you must have [COLOR ##COLOR##]Dropbox account[/COLOR]. Then navigate to [COLOR ##COLOR##]ADD to Lib settings[/COLOR], choose [COLOR ##COLOR##]'Sync'[/COLOR], [COLOR ##COLOR##]'Connect to Dropbox'[/COLOR].

After receiving message about successful connection to Dropbox in addon main menu you can see [COLOR ##COLOR##]'Sync'[/COLOR]. To enable synchronization in [COLOR ##COLOR##]automatic mode[/COLOR] or on startup you need to go to ADD to Lib settings, Synchronize.

[COLOR ##COLOR##]Forced uploading:[/COLOR]:
Allows full upload data (video data base/watched statuses) to Dropbox (deletes the current database in Dropbox).

[COLOR ##COLOR##]Forced downloading:[/COLOR]:
Allows full download data (video data base/watched statuses) from Dropbox (removes the local ADD to Lib database).

[COLOR ##COLOR##]Send changes:[/COLOR]:
Upload changes made in local database.

[COLOR ##COLOR##]Automatic mode:[/COLOR]:
Checks whether database is new, obsolete or actual in comparison with database in Dropbox and then downloads or uploads changes.

[COLOR ##COLOR##]Unlock synchronization:[/COLOR]:
Synchronization can be locked for several reason: another device synchronizing now, process of synchronizing on any device is not completed correctly. If you are sure that a lock caused by a bug, you can perform 'unlock sync'.

[COLOR ##COLOR##]Lock synchronization:[/COLOR]:
Used when you need to block synchronization for other devices.

If you need stop synchronization before it starts at startup, you must use a special command [COLOR ##COLOR##]nos[/COLOR] or [COLOR ##COLOR##]bckupex[/COLOR] (see below).

When synchronizing in automatic mode, used check date of synchronization signatures. If signature of local database is newer than signature database in Dropbox, addon starts uploading changes if opposite - starts downloading. Any changes in local database (with ADD to Lib) updates synchronization signature. It should be noted that Dropbox is not a server able to process requests to add/save data in a queue. Device with newer signature uploads changes to Dropbox and makes database in Dropbox is identical to its local database. Any other device during synchronization downloads this changes. In the case of use  sync only in manual mode it is necessary to trace this process to avoid losing  local changes.

Sync with Dropbox can take a long time. This is due to long requests processing in Dropbox API (roughly one file (episode/movie) - 1 second). In case of errors upload/download data, you need to increase in synchronization settings number of attempts sending a request to Dropbox as well as intervals between them.

Download of watched statuses, can be a long time process too. This is due to long processing JSON request. To accelerate you can reduce interval between requests but this may lead to freezing of Kodi interface.


[B]Services:[/B]

Starting with version 1.0.12 ADD to Lib is used threads separation. Threads separation was managed by 'Main service' also responsible for start of backup, sync and updates in automatically mode. If the user does not use these functions, he can disable Main service in addon settings.

Also starting with version 1.0.12 is available launching addon from memory ([COLOR ##COLOR##]LFM[/COLOR] mode). This method of launching is controlled by auxiliary LFM service and allows you to speed up launch of addon to 40% on some systems. LFM-service controlled by main service and cannot be run standalone. You can turn on LFM mode is in the settings addon.


[B]Errors handling:[/B]

Threads separation prevents to catch all errors during addon runtime and write them to Kodi log. To resolve this problem created an additional file with errors '_errors_' located: Kodi \ userdata \ addon_data \ context.addtolib \ _errors_


[B]Special commands:[/B]

For using special external commands (SEC) you need to create file with command name in ..\ Kodi \ userdata \ addon_data \ context.addtolib \

Services commands:
    nos     : Block starting services (don't stop already starting services, don't delete after execution)
    stopsrv : Stop already starting services (don't block startup services, delete after execution)
    nocln   : Don't remove old (tmp) files on startup (delete after execution)
    bckupex : Launch backup and stop services (delete after execution)


[B]Other actions:[/B]

[COLOR ##COLOR##]'Show all exists TV shows'[/COLOR] - Displays a list of exists TV shows added via Add to Lib. When you select the TV show he becomes the current TV show.
[COLOR ##COLOR##]'Re-index TV shows'[/COLOR] - Rescan TV shows for restore the inner table of links, allowing to define the TV shows from source link or title.
[COLOR ##COLOR##]'Restore TV show'[/COLOR] - Restore lost episodes of the TV show, in the event of accidental deletion or rename (change the type of URL).
[COLOR ##COLOR##]'Open source'[/COLOR] - Allows you to go to the source folder.
[COLOR ##COLOR##]'Rescan current source'[/COLOR] - Replace already added episodes of source on actual episodes of source (useful in case of change of the links within a folder).
[COLOR ##COLOR##]'Advanced add'[/COLOR] - Add episodes (TV show season) with advanced settings.

    [B][COLOR red](!)[/COLOR][/B]   For stable operation of the add-on, to physically remove or rename the TV shows use the tools of this add-on.