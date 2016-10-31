import time as t
from genericpath import isfile
import re
from Navigation.prod import SightingsList as S
import math
import Angle

class Fix(object):

    def __init__(self, logFile =  "log.txt"):
        if not isinstance(logFile, str):
            raise ValueError("Fix.__init__:  " + "illegal logFile")
        if logFile == "":
            raise ValueError("Fix.__init__:  " + "illegal logFile")
        self.nameOfLogFile = logFile
        self.nameOfSightingFile = None
        self.logFormatString = "LOG:\t" + self.getCurrentTime() + ":\t"
        logs = open(self.nameOfLogFile,"a")
        logs.write(self.logFormatString + "Start of log" + "\n")  
        logs.close()  
        if not isfile(logFile):
            raise ValueError("Fix.__init__:  " + "logFile can not create")         
    
    def setSightingFile(self,sightingFile = ".xml"):
        if not isinstance(sightingFile, str):
            raise ValueError("Fix.setSightingFile:  " + "illegal sightingFile")
        matchSightingF = re.match(r'^\S+\.xml$', sightingFile)
        if not matchSightingF:
            raise ValueError("Fix.setSightingFile:  " + "illegal sightingFile")
        else:
            try:
                self.sightingfile = open(sightingFile,"r")
            except:
                raise ValueError("Fix.setSightingFile:  " + "sightingFile cannot open")
            self.nameOfSightingFile = sightingFile
            logs = open(self.nameOfLogFile,"a")
            logs.write(self.logFormatString + "Start of sighting file: " + sightingFile + "\n") 
            logs.close()     
            return sightingFile
            
    def getSightings(self):
        if self.nameOfSightingFile == None:
            raise ValueError("Fix.getSightings:  no sighting file has been set")
        try:
            sightingsList = S.SightingsList(self.nameOfSightingFile)
            sightingsList.get_fix()
            sightingsList.get_sightings()
            numberOfSighting = sightingsList.get_count()
            bodyList = sightingsList.get_body()
            dateList = sightingsList.get_date()
            timeList = sightingsList.get_time()
            observationList = sightingsList.get_observation()
            heightList = sightingsList.get_height()
            temperatureList = sightingsList.get_temperature()
            pressureList = sightingsList.get_pressure()
            horizonList = sightingsList.get_horizon()
        except:
            raise ValueError("Fix.getSightings:  missing a mandatory tag in sighting file")
        isError = sightingsList.checkError()
        if isError == True:
            raise ValueError("Fix.getSightings:  the info associated with a tag is invalid")
        
        xml_List = [[] for i in range(numberOfSighting)]
        for i in range(numberOfSighting):
            xml_List[i].append(bodyList[i])
            xml_List[i].append(dateList[i])
            xml_List[i].append(timeList[i])
            xml_List[i].append(observationList[i])
            xml_List[i].append(heightList[i])
            xml_List[i].append(temperatureList[i])
            xml_List[i].append(pressureList[i])
            xml_List[i].append(horizonList[i])
            print(xml_List[i])
        xml_List.sort( key = lambda l: (l[1], l[2], l[0]) )  
        
        adjustAltitudes = [[]for i in range(numberOfSighting)]
        logs = open(self.nameOfLogFile,"a")
        for i in range(numberOfSighting): 
            adjustAltitude = self.calculateAdjustedAltitude(xml_List[i])
            logs.write(self.logFormatString + xml_List[i][0] + "\t" 
                               +  xml_List[i][1] + "\t" + xml_List[i][2] + "\t" + adjustAltitude + "\n")
            adjustAltitudes[i].append(adjustAltitude)
        logs.write(self.logFormatString + "End of sighting file: " + self.nameOfSightingFile + "\n")
        logs.close()
#        return adjustAltitudes
        approximateLatitude = "0d0.0"
        approximateLongitude = "0d0.0"
        return (approximateLatitude,approximateLongitude)
     
    def calculateAdjustedAltitude(self, xmlList):
        if xmlList[7] == "Natural" or xmlList[7] == "natural":
            dig = (-0.97 * math.sqrt(float(xmlList[4]))) / 60
        else:
            dig = 0
        angle = Angle.Angle()
        try:
            altitude = angle.setDegreesAndMinutes( xmlList[3] )
        except:
            raise ValueError("Fix.getSightings:  altitude must .GE. 0.1 arc-minutes")
        if altitude < (0.1/60):
            raise ValueError("Fix.getSightings:  altitude must .GE. 0.1 arc-minutes")
        refraction = (-0.00452 * float(xmlList[6])) / (273 + (float(xmlList[5])-32) / 1.8) / (math.tan(math.radians(altitude)))
        adjustAltitude = altitude + dig +refraction
        angle.setDegrees(adjustAltitude)
        adjustAltitude = angle.getString()
        return adjustAltitude
     
    def getCurrentTime(self):
        currentTime = t.strftime("%Y-%m-%d %H:%M:%S", t.localtime(t.time()))
        if t.timezone >= 0:
            currentTime += "-" 
        else:
            currentTime += "+"
        currentTime += t.strftime("%H:%M",t.gmtime(t.timezone))
        return currentTime
        