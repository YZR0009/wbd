import time as t
from genericpath import isfile
import re
from Navigation.prod import SightingsList as S
import math
import Angle
import os
import datetime as d
from numpy import arcsin, arccos

class Fix(object):

    def __init__(self, logFile =  "log.txt"):
        if not isinstance(logFile, str):
            raise ValueError("Fix.__init__:  " + "illegal logFile")
        if logFile == "":
            raise ValueError("Fix.__init__:  " + "illegal logFile")
        self.absolutePathOfLogFile = os.path.abspath(logFile)
        self.absolutePathOfSightingFile = None
        self.absolutePathOfAriesFile = None
        self.absolutePathOfStarFile =None
        self.SHAstar = None
        self.latitude = None
        self.numberOfSightingError = 0
        self.logFormatString = "LOG:\t" + self.getCurrentTime() + ":\t"
        logs = open(self.absolutePathOfLogFile,"a")
        logs.write(self.logFormatString + "Log file:\t" + self.absolutePathOfLogFile + "\n") 
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
            self.absolutePathOfSightingFile = os.path.abspath(sightingFile)
            logs = open(self.absolutePathOfLogFile,"a") 
            logs.write(self.logFormatString + "Sighting file:\t" + self.absolutePathOfSightingFile + "\n")
            logs.close()     
            return self.absolutePathOfSightingFile

    def setAriesFile(self,ariesFile = ".txt"):    
        if not isinstance(ariesFile, str):
            raise ValueError("Fix.setAriesFile:  " + "illegal ariesFile")
        matchSightingF = re.match(r'^\S+\.txt$', ariesFile)
        if not matchSightingF:
            raise ValueError("Fix.setAriesFile:  " + "illegal ariesFile")
        else:
            try:
                open(ariesFile,"r")
            except:
                raise ValueError("Fix.setAriesFile:  " + "ariesFile cannot open")           
            self.absolutePathOfAriesFile = os.path.abspath(ariesFile)
            logs = open(self.absolutePathOfLogFile,'a')
            logs.write(self.logFormatString + "Aries file:\t" + self.absolutePathOfAriesFile + "\n")  
            logs.close()  
            return self.absolutePathOfAriesFile
            
    def setStarFile(self,starFile = ".txt"):  
        if not isinstance(starFile, str):
            raise ValueError("Fix.setStarFile:  " + "illegal starFile")
        matchSightingF = re.match(r'^\S+\.txt$', starFile)
        if not matchSightingF:
            raise ValueError("Fix.setStarFile:  " + "illegal starFile")
        else:    
            try:
                open(starFile,"r")
            except:
                raise ValueError("Fix.setStarFile:  " + "starFile cannot open")           
            self.absolutePathOfStarFile = os.path.abspath(starFile)
            logs = open(self.absolutePathOfLogFile,'a')
            logs.write(self.logFormatString + "Star file:\t" + self.absolutePathOfStarFile + "\n")   
            logs.close() 
            return self.absolutePathOfStarFile
            
    def getSightings(self,assumedLatitude = "0d0.0",assumedLongitude = "0d0.0"):
        if self.absolutePathOfSightingFile == None or self.absolutePathOfAriesFile == None or self.absolutePathOfStarFile == None:
            raise ValueError("Fix.getSightings:  no sighting file or aries file or star file has been set")
        isError1 = self.checkAngle(assumedLatitude, False, True, False)
        isError2 = self.checkAngle(assumedLongitude, False, False,True)
        if isError1 == True or isError2 == True:
            raise ValueError("Fix.getSightings:  parameters violate the specification describe")

        sightingsList = S.SightingsList(self.absolutePathOfSightingFile)
        sightingsList.get_fix()
        sightingsList.get_sightings()
        self.numberOfSighting = sightingsList.get_count()
        bodyList = sightingsList.get_body()
        dateList = sightingsList.get_date()
        timeList = sightingsList.get_time()
        observationList = sightingsList.get_observation()
        heightList = sightingsList.get_height()
        temperatureList = sightingsList.get_temperature()
        pressureList = sightingsList.get_pressure()
        horizonList = sightingsList.get_horizon()

        Errors = sightingsList.checkError()
        
        xml_List = [[] for i in range(self.numberOfSighting)]
        for i in range(self.numberOfSighting):
            xml_List[i].append(bodyList[i])           # 0 --------- body
            xml_List[i].append(dateList[i])           # 1 --------- date
            xml_List[i].append(timeList[i])           # 2 --------- time
            xml_List[i].append(observationList[i])    # 3 --------- observation
            xml_List[i].append(heightList[i])         # 4 --------- height
            xml_List[i].append(temperatureList[i])    # 5 --------- temperature
            xml_List[i].append(pressureList[i])       # 6 --------- pressure
            xml_List[i].append(horizonList[i])        # 7 --------- horizon
            if bodyList[i] == "" or dateList[i] == "" or timeList[i] == "" or observationList[i] == "":
                Errors[i] +=1
        #xml_List.sort( key = lambda l: (l[1], l[2], l[0]) )  
        xml_List2 = sorted(xml_List, key = lambda l: (l[1], l[2], l[0]) ) 
        newErrors = [0 for i in range(self.numberOfSighting)]
        for i in range(self.numberOfSighting):
            for j in range(self.numberOfSighting):
                if xml_List[i] == xml_List2[j]:
                    newErrors[i] = Errors[j]           
        
        logs = open(self.absolutePathOfLogFile,"a")
        adjustAltitudeList = ["" for i in range(self.numberOfSighting)]
        latitudeList = ["" for i in range(self.numberOfSighting)]
        longitudeList = ["" for i in range(self.numberOfSighting)]
        distanceAdjustmentList = [-1 for i in range(self.numberOfSighting)]
        azimuthAdjustmentlist = ["" for i in range(self.numberOfSighting)]
        for i in range(self.numberOfSighting): 
            adjustAltitude = self.calculateAdjustedAltitude(xml_List2[i])
            latitude = self.getLatitude(xml_List2[i])
            longitude = self.calculateLongitude(xml_List2[i])
            if adjustAltitude == None or latitude == None or longitude == None:
                newErrors[i] += 1
            else:
                adjustAltitudeList[i] = adjustAltitude
                latitudeList[i] = latitude
                longitudeList[i] = longitude
                distanceAdjustmentList[i] = self.calculateDistanceAdjustment(adjustAltitude,latitude,longitude,assumedLatitude,assumedLongitude)
                azimuthAdjustmentlist[i] = self.calculateAzimuthAdjustment(latitude,assumedLatitude,distanceAdjustmentList[i])
                #angle = Angle.Angle()
               # angle.setDegrees(azimuthAdjustmentlist[i])
               # azimuthAdjustment = angle.getString()
            if newErrors[i] > 0:
                self.numberOfSightingError += 1
                continue
            logs.write(self.logFormatString + xml_List2[i][0] 
                               + "\t" + xml_List2[i][1] 
                               + "\t" + xml_List2[i][2] 
                               + "\t" + adjustAltitude 
                               + "\t" + latitude
                               + "\t" + longitude 
                               + "\t" + assumedLatitude
                               + "\t" + assumedLongitude 
                               + "\t" + azimuthAdjustmentlist[i] 
                               + "\t" + str(distanceAdjustmentList[i]) + "\n")
            
        approximateLatitude = self.calculateApproximateLatitude(assumedLatitude,distanceAdjustmentList,azimuthAdjustmentlist)
        approximateLongitude = self.calculateApproximateLongitude(assumedLongitude,distanceAdjustmentList,azimuthAdjustmentlist)
        logs.write(self.logFormatString + "Sighting errors:\t" + str(self.numberOfSightingError) + "\n")
        logs.write(self.logFormatString + "ApproximateLatitude:\t" + approximateLatitude + "\t"
                   + "ApproximateLongitude:\t" + approximateLongitude + "\n")
        logs.close()

        return (approximateLatitude,approximateLongitude)
     
    def calculateAdjustedAltitude(self, xmlList):
        natural = "natural"
        if xmlList[7].lower() == natural:
            dig = (-0.97 * math.sqrt(float(xmlList[4]))) / 60
        else:
            dig = 0
        angle = Angle.Angle()
        try:
            altitude = angle.setDegreesAndMinutes( xmlList[3] )
        except:
            return None
        if altitude < (0.1/60):
            return None
        refraction = (-0.00452 * float(xmlList[6])) / (273 + (float(xmlList[5])-32) / 1.8) / (math.tan(math.radians(altitude)))
        adjustAltitude = altitude + dig +refraction
        angle.setDegrees(adjustAltitude)
        adjustAltitude = angle.getString()
        return adjustAltitude
    
    def getLatitude(self, xmlList):
        body = xmlList[0]
        dateStr = xmlList[1]
        try:
            date = d.datetime.strptime(dateStr,'%Y-%m-%d')
            dateStr = date.strftime('%m/%d/%y')
        except:
            return None

        dateEarlier = dateStr
        while True:
            key = body + "\t" + dateEarlier
            matchResult = self.findKey(key, body)
            dateEarlier = self.dateMinusOneDay(dateEarlier)
            if matchResult == "":
                return None
            if matchResult != None:
                break
        matchResult = matchResult.rstrip()
        resultList = matchResult.split("\t")
        self.SHAstar = resultList[2]      
        self.latitude = resultList[3]
        isError1 = self.checkAngle(self.SHAstar,False,False,False)
        isError2 = self.checkAngle(self.latitude,True,False,False)
        if isError1 == True:
            self.SHAstar = None
        if isError2 == True:
            self.latitude = None
        return self.latitude
    
    def findKey(self,key,body):
        star = open(self.absolutePathOfStarFile,'r')
        numberOfBody = 0
        while True:
            result = star.readline()
            if not result.find(key) == -1:
                numberOfBody +=1
                star.close()
                return result
            if not result.find(body) == -1:
                numberOfBody +=1
            if result == "":
                star.close()
                if numberOfBody == 0:
                    return result
                return None
    
    def dateMinusOneDay(self,dateStr):
        date = d.datetime.strptime(dateStr,'%m/%d/%y')
        preDate = date + d.timedelta(days = -1)
        preDateStr = preDate.strftime('%m/%d/%y')
        return preDateStr
    
    def calculateLongitude(self,xmlList):
        SHAstar = self.getSHAstar()
        SHAaries = self.calculateGHAaries(xmlList)
        if SHAaries == None or SHAstar == None:
            return None
        angle1 = Angle.Angle()
        angle1.setDegreesAndMinutes(SHAstar)
        sumAngle = angle1.getDegrees() + SHAaries
        angle1.setDegrees(sumAngle)
        longitude = angle1.getString()
        return longitude
    
    def getSHAstar(self):
        return self.SHAstar
    
    def calculateGHAaries(self,xmlList):
        try:
            dateStr = xmlList[1]
            date = d.datetime.strptime(dateStr,'%Y-%m-%d')
            dateStr = date.strftime('%m/%d/%y')
            timeStr = xmlList[2]
            time = d.datetime.strptime(timeStr,'%H:%M:%S')
            hour = time.strftime('%H')
            hour = str(int(hour))
            minute = float(time.strftime('%M'))
            second = float(time.strftime('%S'))
        except:
            return None
               
        aries = open(self.absolutePathOfAriesFile,'r')
        key = dateStr + "\t" + hour
        while True:
            result = aries.readline()
            if not result.find(key) == -1:
                break
            if result == "":
                aries.close()
                return None
        result = result.rstrip()
        resultList = result.split("\t")
        GHA_aries1 = resultList[2]
                
        result2 = aries.readline()
        if result2 == "":
            aries.close()
            return None
        aries.close()
        result2 = result2.rstrip()
        resultList2 = result2.split("\t")
        GHA_aries2 = resultList2[2]
        
        isError1 = self.checkAngle(GHA_aries1,False,False,False)
        isError2 = self.checkAngle(GHA_aries2,False,False,False)
        if isError1 == True or isError2 == True:
            return None
        angle1 = Angle.Angle()
        angle2 = Angle.Angle()
        angle1.setDegreesAndMinutes(GHA_aries1)
        angle2.setDegreesAndMinutes(GHA_aries2)
        subAngle = abs(angle1.getDegrees()-angle2.getDegrees())
        second += minute*60
        GHA_aries = angle1.getDegrees() + subAngle * (second/3600)
        return GHA_aries
     
    def getCurrentTime(self):
        currentTime = t.strftime("%Y-%m-%d %H:%M:%S", t.localtime(t.time()))
        if t.timezone >= 0:
            currentTime += "-" 
        else:
            currentTime += "+"
        currentTime += t.strftime("%H:%M",t.gmtime(t.timezone))
        return currentTime
    
    def checkAngle(self,angle,isLatitude,isAssumedLatitude,isAssumedLongitude):
        if not isinstance(angle, str):
            return True
        if isAssumedLatitude == True:
            h = angle[0:1]
            if h == "N" or h == "S":
                angle = angle[1:]
        try:
            angleList = angle.split("d")  
            degree = int(angleList[0])
            minute = float(angleList[1])
        except:
            return True
        if isAssumedLatitude == True:
            if (degree < 0) or (degree >= 90) :
                return True            
        elif isAssumedLongitude == True:
            if (degree < 0) or (degree >= 360) :
                return True
        elif isLatitude == True:
            if (degree <= -90) or (degree >= 90) :
                return True
        else:
            if (degree < 0) or (degree >= 360):
                return True
        if (minute < 0.0) or (minute >= 60.0):
            return True
        return False
        
    def calculateApproximateLatitude(self,assumedLatitude,distanceAdjustmentList,azimuthAdjustmentList):
        flag_S = False
        h = assumedLatitude[0:1]
        if h == "N" or h == "S":
            assumedLatitude = assumedLatitude[1:]
            if h == "S":
                flag_S = True
        angle = Angle.Angle()
        sum = 0.0
        for i in range(self.numberOfSighting):
            if distanceAdjustmentList[i] == -1 or azimuthAdjustmentList[i] == "":
                continue
            angle.setDegreesAndMinutes(azimuthAdjustmentList[i])
            azimuthAdjustment = angle.getDegrees()
            sum += distanceAdjustmentList[i] * math.cos(math.radians(azimuthAdjustment)) 
 
        angle.setDegreesAndMinutes(assumedLatitude)
        assumedLatitudeAngle = angle.getDegrees()
        if flag_S == True:
            assumedLatitudeAngle = -assumedLatitudeAngle
        approximateLatitudeAngle = assumedLatitudeAngle + sum / 60
        if approximateLatitudeAngle < 0:
            approximateLatitudeAngle = -approximateLatitudeAngle
            approximateLatitude = "S"
        else:
            approximateLatitude = ""
        angle.setDegrees(approximateLatitudeAngle)
        approximateLatitude += angle.getString()
        return approximateLatitude
        
    def calculateApproximateLongitude(self,assumedLongitude,distanceAdjustmentList,azimuthAdjustmentList):
        sum = 0.0
        angle = Angle.Angle()
        for i in range(self.numberOfSighting):
            if distanceAdjustmentList[i] == -1 or azimuthAdjustmentList[i] == "":
                continue
            angle.setDegreesAndMinutes(azimuthAdjustmentList[i])
            azimuthAdjustment = angle.getDegrees()
            sum += distanceAdjustmentList[i] * math.sin(math.radians(azimuthAdjustment)) 
        angle.setDegreesAndMinutes(assumedLongitude)
        assumedLongitudeAngle = angle.getDegrees()
        approximateLongitudeAngle = assumedLongitudeAngle + sum / 60
        angle.setDegrees(approximateLongitudeAngle)
        approximateLongitude = angle.getString()
        return approximateLongitude
    
    def calculateDistanceAdjustment(self,adjustAltitude,latitude,longitude,assumedLatitude,assumedLongitude):
        flag_S = False
        h = assumedLatitude[0:1]
        if h == "N" or h == "S":
            assumedLatitude = assumedLatitude[1:]
            if h == "S":
                flag_S = True
        
        angle1 = Angle.Angle()
        angle1.setDegreesAndMinutes(longitude)
        longitudeAngle = angle1.getDegrees()
        angle1.setDegreesAndMinutes(assumedLongitude)
        assumedLongitudeAngle = angle1.getDegrees()
        LHA = longitudeAngle + assumedLongitudeAngle
        
        angle1.setDegreesAndMinutes(latitude)
        latitudeAngle = angle1.getDegrees()
        angle1.setDegreesAndMinutes(assumedLatitude)
        assumedLatitudeAngle = angle1.getDegrees()
        if flag_S == True:
            assumedLatitudeAngle = -assumedLatitudeAngle
        sinLat = math.sin(math.radians(latitudeAngle)) * math.sin(math.radians(assumedLatitudeAngle))
        cosLat = math.cos(math.radians(latitudeAngle)) * math.cos(math.radians(assumedLatitudeAngle)) * math.cos(math.radians(LHA))
        intermediateDistance = sinLat + cosLat              
        correctedAltitude = arcsin(intermediateDistance) 
        correctedAltitude = math.degrees(correctedAltitude)       
            
        self.intermediateDistance = intermediateDistance
        self.correctedAltitude = correctedAltitude
        
        angle1.setDegreesAndMinutes(adjustAltitude)
        adjustAltitudeAngle = angle1.getDegrees() 
        distanceAdjustment = correctedAltitude - adjustAltitudeAngle
        distanceAdjustment = int(round(distanceAdjustment*60))
        return distanceAdjustment   
         
    def calculateAzimuthAdjustment(self,latitude,assumedLatitude,distanceAdjustment):
        flag_S = False
        h = assumedLatitude[0:1]
        if h == "N" or h == "S":
            assumedLatitude = assumedLatitude[1:]
            if h == "S":
                flag_S = True
        angle = Angle.Angle()       
        angle.setDegreesAndMinutes(latitude)
        latitudeAngle = angle.getDegrees()
        angle.setDegreesAndMinutes(assumedLatitude)
        assumedLatitudeAngle = angle.getDegrees()
        if flag_S == True:
            assumedLatitudeAngle = -assumedLatitudeAngle

        numerator_result = math.sin(math.radians(latitudeAngle)) - (math.sin(math.radians(assumedLatitudeAngle)) * self.intermediateDistance)
        denominator_result = math.cos(math.radians(assumedLatitudeAngle)) * math.cos(math.radians(self.correctedAltitude))
        result = numerator_result / denominator_result 
        azimuthAdjustment = arccos(result)
        azimuthAdjustment = math.degrees(azimuthAdjustment)
        angle.setDegrees(azimuthAdjustment)
        azimuthAdjustmentStr = angle.getString()
        return azimuthAdjustmentStr
    
        