import time
import string
from datetime import datetime
import urllib
import json
import os
from decimal import Decimal
import operator

URL_DISCOVER = 'http://my.hdhomerun.com/discover'
URL_GUIDE_BASE = 'http://my.hdhomerun.com/api/guide.php?DeviceAuth='
URL_RECORDING_RULES = 'http://my.hdhomerun.com/api/recording_rules?DeviceAuth='

class SortType:
    asc = 0
    desc = 1

class GroupType:
    All = 0
    SeriesID = 1
    Category = 2

class SeriesSummary:
    SeriesID = ""
    ImageURL = ""
    
    def __init__(self,SeriesID,ImageURL):
        self.SeriesID = SeriesID
        self.ImageURL = ImageURL
        
    def getSeriesID(self):
        return self.SeriesID

    def getImageURL(self):
        return self.ImageURL

class ChannelInfo:
    GuideNumber = ""
    GuideName = ""
    ImageURL = ""
    Affiliate = ""
    ProgramInfos = []
    VideoCodec = ""
    AudioCodec = ""
    HD =  -1
    URL = ""
    Favorite = -1
    
    def __init__(self):
        return

    def parse(self,parsestr,PyHDHR):
        if 'GuideNumber' in parsestr:
            self.GuideNumber = parsestr['GuideNumber']
        if 'GuideName' in parsestr:
            self.GuideName = parsestr['GuideName']
        if 'ImageURL' in parsestr:
            self.ImageURL = parsestr['ImageURL']
        if 'Affiliate' in parsestr:
            self.Affiliate = parsestr['Affiliate']
        if 'Guide' in parsestr:
            self.ProgramInfos = []
            for guideitem in parsestr['Guide']:
                programinfo = ProgramInfo()
                programinfo.parse(guideitem,PyHDHR)
                self.ProgramInfos.append(programinfo)
        if 'VideoCodec' in parsestr:
            self.VideoCodec = parsestr['VideoCodec']
        if 'AudioCodec' in parsestr:
            self.AudioCodec = parsestr['AudioCodec']
        if 'HD' in parsestr:
            self.HD = parsestr['HD']
        if 'URL' in parsestr:
            self.URL = parsestr['URL']
        if 'Favorite' in parsestr:
            self.Favorite = parsestr['Favorite']

    def getProgramInfos(self):
        return self.ProgramInfos

    def getGuideNumber(self):
        return self.GuideNumber

    def getGuideName(self):
        return self.GuideName

    def getImageURL(self):
        return self.ImageURL
    
    def getAffiliate(self):
        return self.Affiliate

    def getVideoCodec(self):
        return self.VideoCodec
    
    def getAudioCodec(self):
        return self.AudioCodec

    def getHD(self):
        return self.HD

    def getURL(self):
        return self.URL

    def getFavorite(self):
        return self.Favorite

class ProgramInfo:
    SeriesID = ""
    EpisodeNumber = ""
    EpisodeTitle = ""
    Title = ""
    ImageURL = ""
    OriginalAirdate = 0
    Synopsis = ""
    StartTime = 0
    ProgramFilters = []
    EndTime = 0
    
    def __init__(self):
        return
        
    def parse(self,parsestr,PyHDHR):
        if 'SeriesID' in parsestr:
            self.SeriesID = parsestr['SeriesID']
        if 'EpisodeNumber' in parsestr:
            self.EpisodeNumber = parsestr['EpisodeNumber']
        if 'EpisodeTitle' in parsestr:
            self.EpisodeTitle = parsestr['EpisodeTitle']
        if 'Title' in parsestr:
            self.Title = parsestr['Title']
        if 'ImageURL' in parsestr:
            self.ImageURL = parsestr['ImageURL']
        if 'OriginalAirdate' in parsestr:
            self.OriginalAirdate = parsestr['OriginalAirdate']
        if 'Synopsis' in parsestr:
            self.Synopsis = parsestr['Synopsis']
        if 'StartTime' in parsestr:
            self.StartTime = parsestr['StartTime']
        if 'EndTime' in parsestr:
            self.EndTime = parsestr['EndTime']
        if 'Filter' in parsestr:
            for filter in parsestr['Filter']:
                f = PyHDHR.addProgramFilter(ProgramFilter(filter))
                self.addProgramFilter(f)
        
    def getSeriesID(self):
        return self.SeriesID

    def getEpisodeNumber(self):
        return self.EpisodeNumber

    def getEpisodeTitle(self):
        return self.EpisodeTitle

    def getTitle(self):
        return self.Title

    def getImageURL(self):
        return self.ImageURL

    def getOriginalAirdate(self):
        return self.OriginalAirdate

    def getSynopsis(self):
        return self.Synopsis

    def getStartTime(self):
        return self.StartTime

    def addProgramFilter(self,ProgramFilter):
        self.ProgramFilters.append(ProgramFilter)
        
    def getProgramFilters(self):
        return self.ProgramFilters

    def getEndTime(self):
        return self.EndTime

class ProgramFilter:
    Name = ""
    
    def __init__(self,Name):
        self.Name = Name      

    def getName(self):
        return self.Name

class RecordedProgram:
    Category =  ""
    ChannelAffiliate = ""
    ChannelImageURL =  ""
    ChannelName =  ""
    ChannelNumber =  ""
    EndTime = 0
    EpisodeNumber =  ""
    EpisodeTitle = ""
    FirstAiring = 0
    ImageURL =  ""
    OriginalAirdate = 0
    ProgramID =  ""
    RecordEndTime = 0
    RecordStartTime = 0
    RecordSuccess = -1
    SeriesID =  ""
    StartTime = 0
    Synopsis =  ""
    Title =  ""
    DisplayGroupID =  ""
    DisplayGroupTitle =  ""
    PlayURL =  ""
    CmdURL =  ""
    
    def __init__(self):
        return
        
    def parse(self,parsestr):
        if 'Category' in parsestr:
            self.Category = parsestr['Category']
        if 'ChannelAffiliate' in parsestr:
            self.ChannelAffiliate = parsestr['ChannelAffiliate']
        if 'ChannelImageURL' in parsestr:
            self.ChannelImageURL = parsestr['ChannelImageURL']
        if 'ChannelName' in parsestr:
            self.ChannelName = parsestr['ChannelName']
        if 'ChannelNumber' in parsestr:
            self.ChannelNumber = parsestr['ChannelNumber']
        if 'EndTime' in parsestr:
            self.EndTime = parsestr['EndTime']
        if 'EpisodeNumber' in parsestr:
            self.EpisodeNumber = parsestr['EpisodeNumber']
        if 'EpisodeTitle' in parsestr:
            self.EpisodeTitle = parsestr['EpisodeTitle']
        if 'FirstAiring' in parsestr:
            self.FirstAiring = parsestr['FirstAiring']
        if 'ImageURL' in parsestr:
            self.ImageURL = parsestr['ImageURL']
        if 'OriginalAirdate' in parsestr:
            self.OriginalAirdate = parsestr['OriginalAirdate']
        if 'ProgramID' in parsestr:
            self.ProgramID = parsestr['ProgramID']
        if 'RecordEndTime' in parsestr:
            self.RecordEndTime = parsestr['RecordEndTime']
        if 'RecordStartTime' in parsestr:
            self.RecordStartTime = parsestr['RecordStartTime']
        if 'RecordSuccess' in parsestr:
            self.RecordSuccess = parsestr['RecordSuccess']
        if 'SeriesID' in parsestr:
            self.SeriesID = parsestr['SeriesID']
        if 'StartTime' in parsestr:
            self.StartTime = parsestr['StartTime']
        if 'Synopsis' in parsestr:
            self.Synopsis = parsestr['Synopsis']
        if 'Title' in parsestr:
            self.Title = parsestr['Title']
        if 'DisplayGroupID' in parsestr:
            self.DisplayGroupID = parsestr['DisplayGroupID']
        if 'DisplayGroupTitle' in parsestr:
            self.DisplayGroupTitle = parsestr['DisplayGroupTitle']
        if 'PlayURL' in parsestr:
            self.PlayURL = parsestr['PlayURL']
        if 'CmdURL' in parsestr:
            self.CmdURL = parsestr['CmdURL']

    def getCategory(self):
        return self.Category
        
    def getChannelAffiliate(self):
        return self.ChannelAffiliate

    def getChannelImageURL(self):
        return self.ChannelImageURL

    def getChannelName(self):
        return self.ChannelName

    def getChannelNumber(self):
        return self.ChannelNumber

    def getEndTime(self):
        return self.EndTime

    def getEpisodeNumber(self):
        return self.EpisodeNumber

    def getEpisodeTitle(self):
        return self.EpisodeTitle

    def getFirstAiring(self):
        return self.FirstAiring

    def getImageURL(self):
        return self.ImageURL

    def getOriginalAirdate(self):
        return self.OriginalAirdate

    def getProgramID(self):
        return self.ProgramID

    def getRecordEndTime(self):
        return self.RecordEndTime

    def getRecordStartTime(self):
        return self.RecordStartTime

    def getRecordSuccess(self):
        return self.RecordSuccess

    def getSeriesID(self):
        return self.SeriesID

    def getStartTime(self):
        return self.StartTime

    def getSynopsis(self):
        return self.Synopsis

    def getTitle(self):
        return self.Title

    def getDisplayGroupID(self):
        return self.DisplayGroupID

    def getDisplayGroupTitle(self):
        return self.DisplayGroupTitle

    def getPlayURL(self):
        return self.PlayURL

    def getCmdURL(self):
        return self.CmdURL

class RecordingRule:
    SeriesID = ""
    Title = ""
    ImageURL = ""
    RecentOnly = 0
    Priority = 0
    Synopsis = ""
    EndPadding = 0
    StartPadding = 0
    RecordingRuleID = ""
    
    def __init__(self):
        return
        
    def parse(self,parsestr):
        if 'SeriesID' in parsestr:
            self.SeriesID = parsestr['SeriesID']
        if 'Title' in parsestr:
            self.Title = parsestr['Title']
        if 'ImageURL' in parsestr:
            self.ImageURL = parsestr['ImageURL']
        if 'RecentOnly' in parsestr:
            self.RecentOnly = parsestr['RecentOnly']
        if 'Priority' in parsestr:
            self.Priority = parsestr['Priority']
        if 'Synopsis' in parsestr:
            self.Synopsis = parsestr['Synopsis']
        if 'EndPadding' in parsestr:
            self.EndPadding = parsestr['EndPadding']
        if 'StartPadding' in parsestr:
            self.StartPadding = parsestr['StartPadding']
        if 'RecordingRuleID' in parsestr:
            self.RecordingRuleID = parsestr['RecordingRuleID']
        
    def getSeriesID(self):
        return self.SeriesID

    def getTitle(self):
        return self.Title

    def getImageURL(self):
        return self.ImageURL

    def setRecentOnly(self,RecentOnly):
        self.RecentOnly = RecentOnly
    
    def getRecentOnly(self):
        return self.RecentOnly

    def setPriority(self,Priority):
        self.Priority = Priority
    
    def getPriority(self):
        return self.Priority

    def getSynopsis(self):
        return self.Synopsis

    def setEndPadding(self,EndPadding):
        self.EndPadding = EndPadding
    
    def getEndPadding(self):
        return self.EndPadding

    def setStartPadding(self,StartPadding):
        self.StartPadding = StartPadding
    
    def getStartPadding(self):
        return self.StartPadding

    def getRecordingRuleID(self):
        return self.RecordingRuleID
    
class BaseDevice:
    LocalIP = ""
    BaseURL = ""
    DiscoverURL = ""
    
    def __init__(self):
        return
        
    def getLocalIP(self):
        return self.LocalIP

    def getBaseURL(self):
        return self.BaseURL

    def getDiscoverURL(self):
        return self.DiscoverURL

class Tuner(BaseDevice):
    PyHDHR = None
    DeviceID = ""
    LineupURL = ""
    TunerCount = ""
    DeviceAuth = ""
    ModelNumber = ""
    FriendlyName = ""
    FirmwareName = ""
    FirmwareVersion = ""
    ConditionalAccess = ""
    ChannelInfos = {}
    LastDiscover = 0
    
    def __init__(self,PyHDHR):
        self.PyHDHR = PyHDHR
        
    def parse(self,parsestr):
        if 'DeviceID' in parsestr:
            self.DeviceID = parsestr['DeviceID']
        if 'LocalIP' in parsestr:
            self.LocalIP = parsestr['LocalIP']
        if 'BaseURL' in parsestr:
            self.BaseURL = parsestr['BaseURL']
        if 'DiscoverURL' in parsestr:
            self.DiscoverURL = parsestr['DiscoverURL']
        if 'LineupURL' in parsestr:
            self.LineupURL = parsestr['LineupURL']
        
    def getDeviceID(self):
        return self.DeviceID
        
    def getLineupURL(self):
        return self.LineupURL

    def getTunerCount(self):
        return self.TunerCount

    def getDeviceAuth(self):
        return self.DeviceAuth

    def getModelNumber(self):
        return self.ModelNumber

    def getFriendlyName(self):
        return self.FriendlyName

    def getFirmwareName(self):
        return self.FirmwareName

    def getFirmwareVersion(self):
        return self.FirmwareVersion

    def getConditionalAccess(self):
        return self.ConditionalAccess
        
    def getChannelInfos(self):
        return self.ChannelInfos

    def discover(self):
        if time.time() - self.LastDiscover < 60:
            return True

        try:
            response = urllib.urlopen(self.DiscoverURL)
            data = json.loads(response.read())
            if 'TunerCount' in data:
                self.TunerCount = data['TunerCount']
            if 'DeviceAuth' in data:
                self.DeviceAuth = data['DeviceAuth']
                self.PyHDHR.setDeviceAuth(self.DeviceID,self.DeviceAuth)
            if 'ModelNumber' in data:
                self.ModelNumber = data['ModelNumber']
            if 'FriendlyName' in data:
                self.FriendlyName = data['FriendlyName']
            if 'FirmwareName' in data:
                self.FirmwareName = data['FirmwareName']
            if 'FirmwareVersion' in data:
                self.FirmwareVersion = data['FirmwareVersion']
            if 'ConditionalAccess' in data:
                self.ConditionalAccess = data['ConditionalAccess']
            return True
        except Exception as e:
            print "Tuner.discover"
            print(type(e))
            print(e)
            return False

    def processLineup(self,PyHDHR):
        self.discover()
        try:
            response = urllib.urlopen(self.LineupURL)
            data = json.loads(response.read())
            for item in data:
                if 'GuideNumber' in item:
                    if item['GuideNumber'] in self.ChannelInfos:
                        self.ChannelInfos[item['GuideNumber']].parse(item,self.PyHDHR)
                    else:
                        chaninfo = ChannelInfo()
                        chaninfo.parse(item,self.PyHDHR)
                        self.ChannelInfos[item['GuideNumber']] = chaninfo
                    PyHDHR.registerChannelInfo(self.ChannelInfos[item['GuideNumber']],self)
            return True
        except Exception as e:
            print "Tuner.processLineup"
            print(type(e))
            print(e)
            return False

    def processGuide(self,PyHDHR):
        if not self.DeviceAuth:
            return False
        try:
            response = urllib.urlopen(URL_GUIDE_BASE + self.DeviceAuth)
            data = json.loads(response.read())
            for item in data:
                if 'GuideNumber' in item:
                    if item['GuideNumber'] in self.ChannelInfos:
                        self.ChannelInfos[item['GuideNumber']].parse(item,self.PyHDHR)
                    else:
                        chaninfo = ChannelInfo()
                        chaninfo.parse(item,self.PyHDHR)
                        self.ChannelInfos[item['GuideNumber']] = chaninfo
                    PyHDHR.registerChannelInfo(self.ChannelInfos[item['GuideNumber']],self)
            return True
        except Exception as e:
            print "Tuner.processGuide"
            print(type(e))
            print(e)
            return False

class DVR(BaseDevice):
    StorageID = ""
    StorageURL = ""
    FreeSpace = ""
    Version = ""
    FriendlyName = ""
    
    def __init__(self):
        return
        
    def parse(self,parsestr):
        if 'StorageID' in parsestr:
            self.StorageID = parsestr['StorageID']
        if 'LocalIP' in parsestr:
            self.LocalIP = parsestr['LocalIP']
        if 'BaseURL' in parsestr:
            self.BaseURL = parsestr['BaseURL']
        if 'DiscoverURL' in parsestr:
            self.DiscoverURL = parsestr['DiscoverURL']
        if 'StorageURL' in parsestr:
            self.StorageURL = parsestr['StorageURL']
        
    def getStorageID(self):
        return self.StorageID
        
    def getStorageURL(self):
        return self.StorageURL
        
    def getFreeSpace():
        return self.FreeSpace

    def getVersion():
        return self.Version

    def getFriendlyName():
        return self.FriendlyName
        
    def discover(self):
        try:
            response = urllib.urlopen(self.DiscoverURL)
            data = json.loads(response.read())
            if 'FreeSpace' in data:
                self.FreeSpace = data['FreeSpace']
            if 'Version' in data:
                self.Version = data['Version']
            if 'FriendlyName' in data:
                self.FriendlyName = data['FriendlyName']
            return True
        except Exception as e:
            print "DVR.discover"
            print(type(e))
            print(e)
            return False
        
class PyHDHR:
    Tuners = {}
    DVRs = {}
    ProgramFilters = {}
    DeviceAuths = {}
    RecordingRules = {}
    ChannelLineup = {}
    ChannelArray = []
    ChannelInfos = {}
    LastDiscover = 0
    RecordedPrograms = {}
    
    def __init__(self):
        return
        
    def getTuners(self):
        self.discover()
        return self.Tuners

    def getDVRs(self):
        self.discover()
        return self.DVRs

    def setDeviceAuth(self,DeviceID,DeviceAuth):
        self.DeviceAuths[DeviceID] = DeviceAuth
        
    def getDeviceAuth(self):
        retstr = ""
        for key in self.DeviceAuths:
            retstr += self.DeviceAuths[key]
        return retstr
    
    def addProgramFilter(self,pf):
        if pf.getName() not in self.ProgramFilters:
            self.ProgramFilters[pf.getName()] = pf
        return self.ProgramFilters[pf.getName()]
        
    def getProgramFilters(self):
        self.discover()
        return self.ProgramFilters
        
    def registerChannelInfo(self,chaninfo,tuner):
        if chaninfo.getGuideNumber() in self.ChannelLineup:
            if tuner not in self.ChannelLineup[chaninfo.getGuideNumber()]:
                self.ChannelLineup[chaninfo.getGuideNumber()].append(tuner)
        else:
            self.ChannelArray.append(Decimal(chaninfo.getGuideNumber()))
            chans = []
            chans.append(tuner)
            self.ChannelLineup[chaninfo.getGuideNumber()] = chans
        self.ChannelInfos[chaninfo.getGuideNumber()] = chaninfo
        
    def getChannelInfo(self,guideno):
        if guideno in self.ChannelInfos:
            return self.ChannelInfos[guideno]
        else:
            return None
        
    def getChannelList(self):
        self.discover()
        self.ChannelArray.sort()
        return self.ChannelArray
        
    def getWhatsOn(self,guideno=None):
        self.discover()
        
        if not guideno:
            onprogs = {}
            for key in self.ChannelInfos:
                progs = self.ChannelInfos[key].getProgramInfos()
                if len(progs) > 0:
                    onprogs[self.ChannelInfos[key].getGuideNumber()] = progs[0]
            return onprogs        
        else:
            if guideno in self.ChannelInfos:
                progs = self.ChannelInfos[guideno].getProgramInfos()
                if len(progs) > 0:
                    return progs[0]
        
    def getLiveTVURL(self,guideno):
        self.discover(True)
        for tunerkey in self.Tuners:
            chaninfos = self.Tuners[tunerkey].getChannelInfos()
            if guideno in chaninfos:
                return chaninfos[guideno].getURL()
        return None
                
    def getRecordedPrograms(self):
        self.discover()
        self.RecordedPrograms = {}
        for key in self.DVRs:
            try:
                response = urllib.urlopen(self.DVRs[key].getStorageURL())
                data = json.loads(response.read())
                for item in data:
                    recprog = RecordedProgram()
                    recprog.parse(item)
                    self.RecordedPrograms[recprog.getProgramID()] = recprog
                return self.RecordedPrograms
            except Exception as e:
                print "PyHDHR.getRecordedPrograms"
                print(type(e))
                print(e)
                return None

    def getFilteredRecordedPrograms(self,sortby,grouptype,groupby):
        self.discover()
        progs = self.getRecordedPrograms()
        
        filteredprogs = []
        for prog in (sorted(progs.values(), key=operator.attrgetter('RecordEndTime'), reverse=(True if sortby == SortType.asc else False))):
            if grouptype == GroupType.All:
                filteredprogs.append(prog)
            elif grouptype == GroupType.SeriesID:
                if groupby == prog.getSeriesID():
                    filteredprogs.append(prog)
            elif grouptype == GroupType.Category:
                if groupby == prog.getCategory():
                    filteredprogs.append(prog)
            else:
                pass
        return filteredprogs
    
    def getRecordedProgram(self,key):
        if key in self.RecordedPrograms:
            return self.RecordedPrograms[key]
        else:
            return None
            
    def getRecordedSeries(self):
        self.discover()
        progs = self.getRecordedPrograms()
        series = {}
        for key in progs:
            if progs[key].getDisplayGroupTitle() not in series:
                ss = SeriesSummary(progs[key].getSeriesID(),progs[key].getImageURL())
                series[progs[key].getDisplayGroupTitle()] = ss
        return series
        
    def getRecordingRules(self):
        self.discover()
        self.processRecordingRules()
        return self.RecordingRules
        
    def processRecordingRules(self):
        if not self.getDeviceAuth():
            return False
        try:
            response = urllib.urlopen(URL_RECORDING_RULES+self.getDeviceAuth())
            data = json.loads(response.read())
            for item in data:
                if 'RecordingRuleID' in item:
                    if item['RecordingRuleID'] in self.RecordingRules:
                        self.RecordingRules[item['RecordingRuleID']].parse(item)
                    else:
                        recordrule = RecordingRule()
                        recordrule.parse(item)
                        self.RecordingRules[item['RecordingRuleID']] = recordrule
            return True
        except Exception as e:
            print "PyHDHR.processRecordingRules"
            print(type(e))
            print(e)
            return False
        
    def discover(self,force=False):
        if not force:
            if time.time() - self.LastDiscover < 60:
                return True
            
        self.LastDiscover = time.time()
            
        try:
            response = urllib.urlopen(URL_DISCOVER)
            data = json.loads(response.read())
            for item in data:
                if 'StorageID' in item and 'StorageURL' in item:
                    #DVR
                    if item['StorageID'] in self.DVRs:
                        self.DVRs[item['StorageID']].parse(item)
                        self.DVRs[item['StorageID']].discover()
                    else:
                        dvr = DVR()
                        dvr.parse(item)
                        dvr.discover()
                        self.DVRs[item['StorageID']] = dvr
                elif 'DeviceID' in item and 'LineupURL' in item:
                    #Tuner
                    if item['DeviceID'] in self.Tuners:
                        self.Tuners[item['DeviceID']].parse(item)
                        self.Tuners[item['DeviceID']].discover()
                        self.Tuners[item['DeviceID']].processLineup(self)
                        self.Tuners[item['DeviceID']].processGuide(self)
                    else:
                        tuner = Tuner(self)
                        tuner.parse(item)
                        tuner.discover()
                        tuner.processLineup(self)
                        tuner.processGuide(self)
                        self.Tuners[item['DeviceID']] = tuner
                else:
                    print "ERROR: could not determine device type - " + str(item)
            return True
        except Exception as e:
            print "PyHDHR.discover"
            print(type(e))
            print(e)
            return False