from PyHDHR import PyHDHR, Tuner, DVR, ProgramFilter, SortType, GroupType, SeriesSummary
pyhdhr = None

TITLE    = 'HDGrandSlam'
PREFIX   = '/video/hdgrandslam'

ICON = 'icon.png'
ICON_LIVETV = 'livetv.png'
ICON_RECORDINGS = 'recordings.png'
ICON_FAVORITES = 'favorites.png'
ICON_ALLCHANNELS = 'allchannels.png'

def Start():
    ObjectContainer.title1 = TITLE

    DirectoryObject.thumb = R(ICON)
    EpisodeObject.thumb = R(ICON)
    VideoClipObject.thumb = R(ICON)

@handler(PREFIX, TITLE, thumb=ICON)
 
def MainMenu():
    global pyhdhr
    pyhdhr = PyHDHR()
    
    oc = ObjectContainer()
    oc.add(DirectoryObject(key=Callback(ShowLiveTV, title="Live TV"), title="Live TV", thumb=R(ICON_LIVETV)))
    oc.add(DirectoryObject(key=Callback(ShowMainRecordingsMenu, title="Recordings"), title="Recordings", thumb=R(ICON_RECORDINGS)))

    return oc

@route(PREFIX + '/showlivetv')
def ShowLiveTV(title):
    oc = ObjectContainer(title2=title)
    oc.add(DirectoryObject(key=Callback(ShowFavoriteChannels, title="Favorite Channels"), title="Favorite Channels", thumb=R(ICON_FAVORITES)))
    oc.add(DirectoryObject(key=Callback(ShowAllChannels, title="All Channels"), title="All Channels", thumb=R(ICON_ALLCHANNELS)))
    oc.add(DirectoryObject(key=Callback(ShowWhatsOn, title="What's On"), title="What's On", thumb=R(ICON_LIVETV)))
    return oc

@route(PREFIX + '/showfavoritechannels')
def ShowFavoriteChannels(title):
    global pyhdhr
    oc = ObjectContainer(title2=title)
    
    if not pyhdhr:
        pyhdhr = PyHDHR()
        
    cl = pyhdhr.getChannelList()
    for line in cl:
        chan = pyhdhr.getChannelInfo(str(line))
        if chan.getFavorite() == 1:
            oc.add(DirectoryObject(key=Callback(ShowTunedTVStaged,title=str(line),guideno=str(line)), title=str(line),thumb=chan.getImageURL()))
    return oc

@route(PREFIX + '/showallchannels')
def ShowAllChannels(title):
    global pyhdhr
    oc = ObjectContainer(title2=title)
    
    if not pyhdhr:
        pyhdhr = PyHDHR()
        
    cl = pyhdhr.getChannelList()
    for line in cl:
        chan = pyhdhr.getChannelInfo(str(line))
        oc.add(DirectoryObject(key=Callback(ShowTunedTVStaged,title=str(line),guideno=str(line)), title=str(line),thumb=chan.getImageURL()))
    return oc

@route(PREFIX + '/showwhatson')
def ShowWhatsOn(title):
    global pyhdhr
    oc = ObjectContainer(title2=title)
    
    if not pyhdhr:
        pyhdhr = PyHDHR()
    
    progs = pyhdhr.getWhatsOn()
    for guideno in progs:
        oc.add(TVShowObject(key=Callback(ShowTunedTVStaged, title=str(progs[guideno].getTitle() + " - " + progs[guideno].getEpisodeTitle()),guideno=guideno), title=str(progs[guideno].getTitle() + " - " + progs[guideno].getEpisodeTitle()), thumb=progs[guideno].getImageURL(),rating_key=progs[guideno].getSeriesID()))
    return oc
    
@route(PREFIX + '/showtunedtvstaged')
def ShowTunedTVStaged(title,guideno):
    oc = ObjectContainer(title2=title)
    oc.add(ShowTunedTV(guideno=guideno))
    return oc

@route(PREFIX + '/viewchannel')
def ViewChannel(title):
    oc = ObjectContainer(header="Empty", message="Unable to display videos for this show right now.")      
    return oc

@route(PREFIX + '/showmainrecordingsmenu')
def ShowMainRecordingsMenu(title):
    oc = ObjectContainer(title2=title)
    oc.add(DirectoryObject(key=Callback(ShowAllRecordings, title="All Recordings"), title="All Recordings", thumb='https://www.silicondust.com/wp-content/uploads/2016/03/dvr-logo.png'))
    oc.add(DirectoryObject(key=Callback(ShowRecordingsBySeriesMenu, title="By Series"), title="By Series", thumb='https://www.silicondust.com/wp-content/uploads/2016/03/dvr-logo.png'))
    return oc

@route(PREFIX + '/showallrecordings')
def ShowAllRecordings(title):
    global pyhdhr
    oc = ObjectContainer(title2=title)
    
    if not pyhdhr:
        pyhdhr = PyHDHR()
        
    rp = pyhdhr.getFilteredRecordedPrograms(SortType.asc,GroupType.All,None)
    if rp:
        for r in rp:
            oc.add(ShowRecording(recprogkey=r.getProgramID()))
    return oc
    
@route(PREFIX + '/showrecordingsbyseriesmenu')
def ShowRecordingsBySeriesMenu(title):
    global pyhdhr
    oc = ObjectContainer(title2=title)
    
    if not pyhdhr:
        pyhdhr = PyHDHR()

    series = pyhdhr.getRecordedSeries()
    
    if series:
        for titlekey in sorted(series):
            oc.add(TVShowObject(key=Callback(ShowRecordingsBySeries, title=str(titlekey), seriesid=series[titlekey].getSeriesID()), title=str(titlekey), thumb=series[titlekey].getImageURL(),episode_count=(series[titlekey].getEpisodeCount()-1),rating_key=series[titlekey].getSeriesID()))
    return oc

@route(PREFIX + '/showrecordingsbyseries')
def ShowRecordingsBySeries(title,seriesid):
    global pyhdhr
    oc = ObjectContainer(title2=title)
    
    if not pyhdhr:
        pyhdhr = PyHDHR()

    rp = pyhdhr.getFilteredRecordedPrograms(SortType.asc,GroupType.SeriesID,seriesid)
    if rp:
        for r in rp:
            oc.add(ShowRecording(recprogkey=r.getProgramID()))
    return oc

@route(PREFIX + '/showtunedtv')
def ShowTunedTV(guideno,include_container=False,plat=None):
    global pyhdhr
    if not pyhdhr:
        pyhdhr = PyHDHR()
    
    if not plat:
        plat = Client.Platform
    
    liveurl = pyhdhr.getLiveTVURL(guideno)
    if not liveurl:
        return ObjectContainer(header="Empty", message="Could not fetch url")
    
    chaninfo = pyhdhr.getChannelInfo(guideno)
    if chaninfo:
        p_title = ""
        p_stitle = ""
        p_synopsis = ""
        p_imageurl = ""
        
        proginfo = pyhdhr.getWhatsOn(guideno)
        if not proginfo:
            p_title=chaninfo.getGuideNumber()
            p_stitle=chaninfo.getGuideName()
            p_synopsis=""
            p_imageurl=chaninfo.getImageURL()
        else:
            p_title=proginfo.getTitle()
            p_stitle=proginfo.getEpisodeTitle()
            p_synopsis=proginfo.getSynopsis()
            p_imageurl=proginfo.getImageURL()
        
        vcodec = ""
        if chaninfo.getVideoCodec() == "MPEG2":
            vcodec = "mpeg2video"
        elif chaninfo.getVideoCodec() == "H264":
            vcodec = "H.264"
        else:
            Log.Critical("Unknown video codec")
            oc = ObjectContainer(header="Empty", message="Unknown video codec")
            return oc

        acodec = ""
        if chaninfo.getAudioCodec() == "AAC":
            acodec = "aac"
        elif chaninfo.getAudioCodec() == "AC3":
            acodec = "ac3"
        else:
            Log.Critical("Unknown audio codec")
            oc = ObjectContainer(header="Empty", message="Unknown audio codec")
            return oc
            
        brate = None
        aratio = None
        vpix = None
        
        if chaninfo.getHD() == 1:
            aratio = "1.78"
            vpix = 1080
            if vcodec == "mpeg2video":
                brate = 13000
            else:
                brate = 4000
        else:
            aratio = "1.33"
            vpix = 480
            if vcodec == "mpeg2video":
                brate = 13000
            else:
                brate = 4000
            
        obj = EpisodeObject(
            key=Callback(ShowTunedTV,guideno=guideno,include_container=True,plat=plat),
            url=liveurl,
            title=p_title,
            source_title=p_stitle,
            summary=p_synopsis,
            duration=14400000,
            thumb=p_imageurl,
            items = [   
                MediaObject(
                    parts = [
                        PartObject(
                            key=liveurl
                        )
                    ],
                    container = 'mpegts',
                    video_codec = vcodec,
                    audio_codec = acodec,
                    optimized_for_streaming = True,
                    bitrate = brate,
                    aspect_ratio=aratio,
                    video_resolution=vpix
                )
            ]  
        )
          
        if include_container:
            return ObjectContainer(objects=[obj])
        else:
            return obj
    else:
        return ObjectContainer(header="Empty", message="Unknown error fetching program")

@route(PREFIX + '/showrecording')
def ShowRecording(recprogkey,include_container=False,plat=None):
    global pyhdhr
    if not pyhdhr:
        pyhdhr = PyHDHR()
    
    if not plat:
        plat = Client.Platform

    prog = pyhdhr.getRecordedProgram(recprogkey)
    if prog:
        chaninfo = pyhdhr.getChannelInfo(prog.getChannelNumber())
        
        vcodec = ""
        if chaninfo.getVideoCodec() == "MPEG2":
            vcodec = "mpeg2video"
        elif chaninfo.getVideoCodec() == "H264":
            vcodec = "H.264"
        else:
            Log.Critical("Unknown video codec")
            oc = ObjectContainer(header="Empty", message="Unknown video codec")
            return oc

        acodec = ""
        if chaninfo.getAudioCodec() == "AAC":
            acodec = "aac"
        elif chaninfo.getAudioCodec() == "AC3":
            acodec = "ac3"
        else:
            Log.Critical("Unknown audio codec")
            oc = ObjectContainer(header="Empty", message="Unknown audio codec")
            return oc
            
        brate = None
        aratio = None
        vpix = None
        
        if chaninfo.getHD() == 1:
            aratio = "1.78"
            vpix = 1080
            if vcodec == "mpeg2video":
                brate = 13000
            else:
                brate = 4000
        else:
            aratio = "1.33"
            vpix = 480
            if vcodec == "mpeg2video":
                brate = 13000
            else:
                brate = 4000
            
        obj = EpisodeObject(
            key=Callback(ShowRecording,recprogkey=recprogkey,include_container=True,plat=plat),
            url=prog.getPlayURL(),
            title=prog.getTitle(),
            source_title=prog.getEpisodeTitle(),
            summary=prog.getSynopsis(),
            duration=((prog.getRecordEndTime() - prog.getRecordStartTime()) * 1000),
            thumb=prog.getImageURL(),
            items = [   
                MediaObject(
                    parts = [
                        PartObject(
                            key=prog.getPlayURL()
                        )
                    ],
                    container = 'mpegts',
                    video_codec = vcodec,
                    audio_codec = acodec,
                    optimized_for_streaming = True,
                    bitrate = brate,
                    aspect_ratio=aratio,
                    video_resolution=vpix
                )
            ]  
        )
          
        if include_container:
            return ObjectContainer(objects=[obj])
        else:
            return obj
    else:
        return ObjectContainer(header="Empty", message="Unknown error fetching program")

