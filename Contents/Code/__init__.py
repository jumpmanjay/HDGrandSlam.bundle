PyHDHR = SharedCodeService.PyHDHR.PyHDHR
Tuner = SharedCodeService.PyHDHR.Tuner
ProgramFilter = SharedCodeService.PyHDHR.ProgramFilter
SortType = SharedCodeService.PyHDHR.SortType
GroupType = SharedCodeService.PyHDHR.GroupType
SeriesSummary = SharedCodeService.PyHDHR.SeriesSummary

pyhdhr = None

TITLE    = 'HDGrandSlam'
PREFIX   = '/video/hdgrandslam'

ICON = 'icon.png'
ICON_LIVETV = 'livetv.png'
ICON_RECORDINGS = 'recordings.png'
ICON_FAVORITES = 'favorites.png'
ICON_ALLCHANNELS = 'allchannels.png'
ICON_SEARCH = 'search.png'
ICON_SETTINGS = 'settings.png'
ICON_UNKNOWN = 'unknown.png'
ICON_BROKEN = 'broken.png'
ICON_RECORDEDBYSERIES = 'recordedbyseries.png'
ICON_ALLRECORDED = 'allrecorded.png'

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
    oc.add(DirectoryObject(key=Callback(ShowLiveTV, title=L('LiveTV')), title=L('LiveTV'), thumb=R(ICON_LIVETV)))
    oc.add(DirectoryObject(key=Callback(ShowMainRecordingsMenu, title=L('Recordings')), title=L('Recordings'), thumb=R(ICON_RECORDINGS)))
    oc.add(InputDirectoryObject(key=Callback(SearchAll), title=L('SearchAll'), thumb=R(ICON_SEARCH)))
    oc.add(PrefsObject(title=L('Settings'), thumb=R(ICON_SETTINGS)))
    return oc

@route(PREFIX + '/showlivetv')
def ShowLiveTV(title):
    oc = ObjectContainer(title2=title)
    oc.add(DirectoryObject(key=Callback(ShowFavoriteChannels, title=L('FavoriteChannels')), title=L('FavoriteChannels'), thumb=R(ICON_FAVORITES)))
    oc.add(DirectoryObject(key=Callback(ShowAllChannels, title=L('AllChannels')), title=L('AllChannels'), thumb=R(ICON_ALLCHANNELS)))
    oc.add(DirectoryObject(key=Callback(ShowWhatsOn, title=L('WhatsOn')), title=L('WhatsOn'), thumb=R(ICON_LIVETV)))
    oc.add(InputDirectoryObject(key=Callback(SearchLiveTV), title=L('SearchLiveTV'), thumb=R(ICON_SEARCH)))
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
            oc.add(DirectoryObject(key=Callback(ShowTunedTVStaged,title=str(line),guideno=str(line)), title=str(line),thumb=(chan.getImageURL() if chan.getImageURL() else R(ICON_BROKEN))))
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
        oc.add(DirectoryObject(key=Callback(ShowTunedTVStaged,title=str(line),guideno=str(line)), title=str(line),thumb=(chan.getImageURL() if chan.getImageURL() else R(ICON_BROKEN))))
    return oc

@route(PREFIX + '/showwhatson')
def ShowWhatsOn(title):
    global pyhdhr
    oc = ObjectContainer(title2=title)
    
    if not pyhdhr:
        pyhdhr = PyHDHR()
    
    progs = pyhdhr.getWhatsOn()
    for guideno in progs:
        oc.add(DirectoryObject(key=Callback(ShowTunedTVStaged, title=str(progs[guideno].getTitle() + " - " + progs[guideno].getEpisodeTitle()),guideno=guideno), title=str(progs[guideno].getTitle() + " - " + progs[guideno].getEpisodeTitle()), thumb=(progs[guideno].getImageURL() if progs[guideno].getImageURL() else R(ICON_UNKNOWN))))
    return oc
    
@route(PREFIX + '/showtunedtvstaged')
def ShowTunedTVStaged(title,guideno):
    oc = ObjectContainer(title2=title)
    oc.add(ShowTunedTV(guideno=guideno))
    return oc

@route(PREFIX + '/showmainrecordingsmenu')
def ShowMainRecordingsMenu(title):
    oc = ObjectContainer(title2=title)
    oc.add(DirectoryObject(key=Callback(ShowAllRecordings, title=L('AllRecordings')), title=L('AllRecordings'), thumb=R(ICON_ALLRECORDED)))
    oc.add(DirectoryObject(key=Callback(ShowRecordingsBySeriesMenu, title=L('BySeries')), title=L('BySeries'), thumb=R(ICON_RECORDEDBYSERIES)))
    oc.add(InputDirectoryObject(key=Callback(SearchRecorded), title=L('SearchRecorded'), thumb=R(ICON_SEARCH)))
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
            obj = ShowRecording(recprogkey=r.getProgramID())
            if obj:
                oc.add(obj)
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
            oc.add(TVShowObject(key=Callback(ShowRecordingsBySeries, title=str(titlekey), seriesid=series[titlekey].getSeriesID()), title=str(titlekey), thumb=(series[titlekey].getImageURL() if series[titlekey].getImageURL() else R(ICON_UNKNOWN)),episode_count=(series[titlekey].getEpisodeCount()-1),rating_key=series[titlekey].getSeriesID()))
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
            obj = ShowRecording(recprogkey=r.getProgramID())
            if obj:
                oc.add(obj)
    return oc

@route(PREFIX + '/searchall')
def SearchAll(query):
    global pyhdhr
    oc = ObjectContainer(title2="search all...")
    
    if not pyhdhr:
        pyhdhr = PyHDHR()

    progs = pyhdhr.searchWhatsOn(query)

    if len(progs) > 0:
        for guideno in progs:
            oc.add(TVShowObject(key=Callback(ShowTunedTVStaged, title=str(progs[guideno].getTitle() + " - " + progs[guideno].getEpisodeTitle()),guideno=guideno), title=str(progs[guideno].getTitle() + " - " + progs[guideno].getEpisodeTitle()), thumb=(progs[guideno].getImageURL() if progs[guideno].getImageURL() else R(ICON_UNKNOWN)),rating_key=progs[guideno].getSeriesID()))

    progs = pyhdhr.searchRecorded(query)

    if len(progs) > 0:
        for recprogkey in progs:
            oc.add(ShowRecording(recprogkey=recprogkey))    
    oc.objects.sort(key = lambda obj: obj.title)
    return oc

@route(PREFIX + '/searchlivetv')
def SearchLiveTV(query):
    global pyhdhr
    oc = ObjectContainer(title2="search live tv...")
    
    if not pyhdhr:
        pyhdhr = PyHDHR()

    progs = pyhdhr.searchWhatsOn(query)

    if len(progs) > 0:
        for guideno in progs:
            oc.add(TVShowObject(key=Callback(ShowTunedTVStaged, title=str(progs[guideno].getTitle() + " - " + progs[guideno].getEpisodeTitle()),guideno=guideno), title=str(progs[guideno].getTitle() + " - " + progs[guideno].getEpisodeTitle()), thumb=(progs[guideno].getImageURL() if progs[guideno].getImageURL() else R(ICON_UNKNOWN)),rating_key=progs[guideno].getSeriesID()))
    return oc

@route(PREFIX + '/searchrecorded')
def SearchRecorded(query):
    global pyhdhr
    oc = ObjectContainer(title2='Search Results for \''+str(query)+'\'')
    
    if not pyhdhr:
        pyhdhr = PyHDHR()

    progs = pyhdhr.searchRecorded(query)

    if len(progs) > 0:
        for recprogkey in progs:
            oc.add(ShowRecording(recprogkey=recprogkey))    
    return oc

@route(PREFIX + '/showtunedtv')
def ShowTunedTV(guideno,include_container=False):
    global pyhdhr
    if not pyhdhr:
        pyhdhr = PyHDHR()
    
    liveurl = pyhdhr.getLiveTVURL(guideno)
    if not liveurl:
        return ObjectContainer(header="Empty", message="Could not fetch url")
    
    chaninfo = pyhdhr.getChannelInfo(guideno)
    if chaninfo:
        cont = 'mpegts'
        vcodec = 'mpeg2video'
        acodec = 'ac3'
        
        t = chaninfo.getTuner()
        Log.Debug("Tuner: " + t.getModelNumber())
        
        if t.getModelNumber() == "HDTC-2US":
            if Prefs['UseDefaultTranscoding'] == True:
                transcodeoption = t.getTranscodeOption()
                if not transcodeoption:
                    liveurl = liveurl + "?transcode=none"
                    Log.Debug("Could not get tuner transcode option, using none")
                else:
                    Log.Debug("Tuner transcode option: " + transcodeoption)
                    if transcodeoption != "none":
                        cont = 'mp4'
                        vcodec = 'h264'
                        acodec = 'ac3'
                    liveurl = liveurl + "?transcode="+transcodeoption
            else:
                liveurl = liveurl + "?transcode=none"
        else:
            if chaninfo.getVideoCodec() == "MPEG2":
                cont = 'mpegts'
                vcodec = 'mpeg2video'
            elif chaninfo.getVideoCodec() == "H264":
                cont = 'mp4'
                vcodec = 'h264'
            else:
                msg = "Unknown video codec: " + chaninfo.getVideoCodec()+". Using default"
                Log.Critical(msg)

            if chaninfo.getAudioCodec() == "AAC":
                acodec = 'aac'
            elif chaninfo.getAudioCodec() == "AC3":
                acodec = 'ac3'
            else:
                msg = "Unknown audio codec: " + chaninfo.getAudioCodec()+". Using default"
                Log.Critical(msg)
        
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
        
        brate = None
        aratio = None
        vpix = None
        
        if chaninfo.getHD() == 1:
            aratio = "1.78"
            vpix = 1080
            if vcodec == 'mpeg2video' or vcodec == 'mpeg1video':
                brate = 13000
            else:
                brate = 4000
        else:
            aratio = "1.33"
            vpix = 480
            if vcodec == 'mpeg2video' or vcodec == 'mpeg1video':
                brate = 4000
            else:
                brate = 1500
            
        Log.Debug("Using the following MediaObject profile:\ncontainer: "+cont+",\nvideo codec: "+vcodec+",\naudio codec: "+acodec+",\nbitrate: "+str(brate)+",\naspect_ratio: "+aratio+",\nvideo_resolution: "+str(vpix))
        
        obj = EpisodeObject(
            key=Callback(ShowTunedTV,guideno=guideno,include_container=True),
            url=liveurl,
            title=p_title,
            source_title=p_stitle,
            summary=p_synopsis,
            duration=14400000,
            thumb=(p_imageurl if p_imageurl else R(ICON_UNKNOWN)),
            items = [   
                MediaObject(
                    parts = [
                        PartObject(
                            key=liveurl
                        )
                    ],
                    container = cont,
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
        msg = "Unknown error fetching channel info for ChannelNumber: "+guideno
        Log.Critical(msg)
        return ObjectContainer(header="Empty", message=msg)

@route(PREFIX + '/showrecording')
def ShowRecording(recprogkey,include_container=False):
    global pyhdhr
    if not pyhdhr:
        pyhdhr = PyHDHR()
    
    prog = pyhdhr.getRecordedProgram(recprogkey)
    if prog:
        
        cont = 'mpegts'
        vcodec = 'mpeg2video'
        acodec = 'ac3'
        brate = 13000
        aratio = "1.78"
        vpix = 1080
        
        chaninfo = pyhdhr.getChannelInfo(prog.getChannelNumber())
        if chaninfo:
            t = chaninfo.getTuner()
            Log.Debug("Tuner: " + t.getModelNumber())
            
            if t.getModelNumber() == "HDTC-2US":
                transcodeoption = t.getTranscodeOption()
                if not transcodeoption:
                    Log.Debug("Could not get tuner transcode option, using none")
                    vcodec = 'mpeg2video'
                    acodec = 'ac3'
                else:                
                    Log.Debug("Tuner transcode option: " + transcodeoption)
                    if transcodeoption == "none":
                        cont = 'mpegts'
                        vcodec = 'mpeg2video'
                        acodec = 'ac3'
                    else:
                        cont = 'mp4'
                        vcodec = 'h264'
                        acodec = 'ac3'
            else:
                if chaninfo.getVideoCodec() == "MPEG2":
                    cont = 'mpegts'
                    vcodec = 'mpeg2video'
                elif chaninfo.getVideoCodec() == "H264":
                    cont = 'mp4'
                    vcodec = 'h264'
                else:
                    msg = "Unknown video codec: " + chaninfo.getVideoCodec()+". Using default"
                    Log.Critical(msg)

                if chaninfo.getAudioCodec() == "AAC":
                    acodec = 'aac'
                elif chaninfo.getAudioCodec() == "AC3":
                    acodec = 'ac3'
                else:
                    msg = "Unknown audio codec: " + chaninfo.getAudioCodec()+". Using default"
                    Log.Critical(msg)
            
            if chaninfo.getHD() == 1:
                aratio = "1.78"
                vpix = 1080
                if vcodec == 'mpeg2video':
                    brate = 13000
                else:
                    brate = 4000
            else:
                aratio = "1.33"
                vpix = 480
                if vcodec == 'mpeg2video':
                    brate = 13000
                else:
                    brate = 4000
        else:
            msg = "Error fetching channel info for ChannelNumber: "+str(prog.getChannelNumber())+". Most likely, the tuner or the channel on the tuner this was recorded on is no longer in the lineup. Using default values- cross your fingers."
            Log.Critical(msg)

        Log.Debug("Using the following MediaObject profile:\ncontainer: "+cont+",\nvideo codec: "+vcodec+",\naudio codec: "+acodec+",\nbitrate: "+str(brate)+",\naspect_ratio: "+aratio+",\nvideo_resolution: "+str(vpix))
                
        obj = EpisodeObject(
            key=Callback(ShowRecording,recprogkey=recprogkey,include_container=True),
            url=prog.getPlayURL(),
            title=prog.getTitle(),
            source_title=prog.getEpisodeTitle(),
            summary=prog.getSynopsis(),
            duration=((prog.getRecordEndTime() - prog.getRecordStartTime()) * 1000),
            thumb=(prog.getImageURL() if prog.getImageURL() else R(ICON_UNKNOWN)),
            items = [   
                MediaObject(
                    parts = [
                        PartObject(
                            key=prog.getPlayURL()
                        )
                    ],
                    container = cont,
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
        msg = "Unknown error fetching program info for ProgramID: "+recprogkey
        Log.Critical(msg)
        return None

