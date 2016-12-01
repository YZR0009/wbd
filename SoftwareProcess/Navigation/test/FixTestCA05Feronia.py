import unittest
import uuid
import os
import Navigation.prod.Fix as F

class TestFix(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.className = "Fix."
        cls.logStartString = "Log file:"
        cls.starSightingString = "Sighting file:"
        cls.starSightingErrorString = "Sighting errors:"
        cls.ariesFileString = "Aries file:"
        cls.starFileString = "Star file:"
        cls.DEFAULT_LOG_FILE = "log.txt"
        cls.mylog = "mylog2.txt"
        cls.ariesFileName = "CA03_Valid_Aries.txt"
        cls.starFileName = "CA03_Valid_Stars.txt"
        cls.testToFileMap = [
            ["validStarSightingFile", "CA02_200_ValidStarSightingFile.xml"],
            ["validAriesFile", "CA03_Valid_Aries.txt"],           
            ["validStarFile", "CA03_Valid_Stars.txt"], 
            ["genericValidStarSightingFile", "CA02_300_GenericValidStarSightingFile.xml"], 
            ["genericValidSightingFileWithMixedIndentation", "CA02_300_ValidWithMixedIndentation.xml"],
            ["validOneStarSighting", "CA02_300_ValidOneStarSighting.xml"],
            ["validMultipleStarSighting", "CA02_300_ValidMultipleStarSighting.xml"],
            ["validMultipleStarSightingSameDateTime", "CA02_300_ValidMultipleStarSightingSameDateTime.xml"],
            ["validWithNoSightings", "CA02_300_ValidWithNoSightings.xml"],
            ["validWithExtraneousTags", "CA02_300_ValidWithExtraneousTags.xml"],
            ["validOneStarNaturalHorizon","CA02_300_ValidOneStarNaturalHorizon.xml"],
            ["validOneStarArtificialHorizon", "CA02_300_ValidOneStarArtificialHorizon.xml"],
            ["validOneStarWithDefaultValues", "CA02_300_ValidOneStarWithDefaultValues.xml"],
            ["invalidWithMissingMandatoryTags","CA02_300_InvalidWithMissingMandatoryTags.xml"],
            ["invalidBodyTag","CA02_300_InvalidBody.xml"],
            ["invalidDateTag","CA02_300_InvalidDate.xml"],
            ["invalidTimeTag","CA02_300_InvalidTime.xml"],
            ["invalidObservationTag","CA02_300_InvalidObservation.xml"],
            ["invalidHeightTag","CA02_300_InvalidHeight.xml"],
            ["invalidTemperatureTag", "CA02_300_InvalidTemperature.xml"],
            ["invalidPressureTag","CA02_300_InvalidPressure.xml"],
            ["invalidHorizonTag","CA02_300_InvalidHorizon.xml"],
            ["validLatLon", "CA03_300_ValidStarLatLon.xml"],
            ["validLatLonInterpolated", "CA03_300_ValidStarLatLonInterpolationRequired.xml"]
            ]  



        
#----------          
    def setUp(self):
        if(os.path.isfile(self.DEFAULT_LOG_FILE)):
            os.remove(self.DEFAULT_LOG_FILE) 
        # generate random log file name
        self.RANDOM_LOG_FILE = "log" + str(uuid.uuid4())[-12:] + ".txt"
        self.deleteNamedLogFlag = False
    
    def tearDown(self):
        if(self.deleteNamedLogFlag):
            try:
                if(os.path.isfile(self.RANDOM_LOG_FILE)):
                    os.remove(self.RANDOM_LOG_FILE)  
            except:
                pass
            
            
#==================== Fix.getSightings ===================         
# 300 getSightings
#    Analysis
#        inputs:
#            via parm:  none
#            via file:  xml description of sighting
#        outputs:
#            returns:    ("0d0.0", "0d0.0")
#|            via file:    writes body/tdate/ttime/tadjustedAltitude/tlongitude/tlatitude
#                        sorted by date, time, body
#        entry criterion:
#            setSightingsFile must be called first
#
#    Happy tests:
#        sighting file 
#            test 010:     file with valid sightings -> should return ("0d0.0", "0d0.0")
#            valid file with mixed indentation -> should not indicate any errors
#            valid file with one sighting  -> should log one star body
#            valid file with multiple sightings -> should log star bodies in sorted order
#            valid file with multiple sightings at same date/time -> should log star bodies in order sorted by body 
#            valid file with zero sightings -> should not log any star bodies
#            valid file with extraneous tag -> should log star(s) without problem
#        sighting file contents
#            valid body with natural horizon -> should calculate altitude with dip
#            valid body with artificial horizon -> should calculate altitude without dip
#            valid body with default values -> should calculate altitude with height=0, temperature=72, pressure=1010, horizon-natural
#            sighting file with invalid mandatory tag (one of each:  fix, body, date, time, observation)
#            sighting file with invalid tag value (one of each:  date, time, observation, height, temperature, pressure, horizon)
#    Sad tests:
#        sightingFile:
#            sighting file not previously set
#            star file not previously set
#            aries file not previously set
#+++++++++++++++++++ Happy Path Tests ++++++++++++++++++++  

        
         
#-----------        
    def test300_010_ShouldLogStarLatLonWithSample2(self):
        'log geographical position'
        testFile = "CA05sightings.xml"
        targetStringList = ["Pollux", None, None, None, "27d59.1", "87d30.8","N27d59.5","85d33.4","7d21.1","-2919"]
        theFix = F.Fix(self.DEFAULT_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        assumedLatitude = "N27d59.5"
        assumedLongitude = "85d33.4"
        theFix.getSightings(assumedLatitude,assumedLongitude)
        
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Lat/Lon entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        print(self.RANDOM_LOG_FILE)
       # self.deleteNamedLogFlag = True  
        
    def test300_020_ShouldReturnCorrectTupleWithSample2(self):
        'parse sighting file that valid tags'
        testFile = "CA05sightings.xml"
        expectedResult = ("S20d15.5", "79d19.9")
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setStarFile(self.starFileName)
        theFix.setAriesFile(self.ariesFileName)
        assumedLatitude = "N27d59.5"
        assumedLongitude = "85d33.4"
        result = theFix.getSightings(assumedLatitude,assumedLongitude)
        self.assertTupleEqual(expectedResult, result, 
                              "Minor:  incorrect return value from getSightings")  
        
    def test300_030_ShouldLogStarLatLonWithSample1(self):
        'log geographical position'
        testFile = "CA05sightings2.xml"
        targetStringList = ["Rigil Kent.", None, None, None, "-60d53.8", "318d09.9","S53d38.4","74d35.3","125d37.7","2159"]
        theFix = F.Fix(self.DEFAULT_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        assumedLatitude = "S53d38.4"
        assumedLongitude = "74d35.3"
        theFix.getSightings(assumedLatitude,assumedLongitude)
        
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Lat/Lon entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        print(self.RANDOM_LOG_FILE)
       # self.deleteNamedLogFlag = True

    def test300_040_ShouldLogStarLatLonWithSample1(self):
        'log geographical position'
        testFile = "CA05sightings2.xml"
        targetStringList = ["Acrux", None, None, None, "-63d11.3", "351d30.3","S53d38.4","74d35.3","132d48.3","434"]
        theFix = F.Fix(self.DEFAULT_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        assumedLatitude = "S53d38.4"
        assumedLongitude = "74d35.3"
        theFix.getSightings(assumedLatitude,assumedLongitude)
        
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Lat/Lon entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        print(self.RANDOM_LOG_FILE)
       # self.deleteNamedLogFlag = True

    def test300_050_ShouldLogStarLatLonWithSample1(self):
        'log geographical position'
        testFile = "CA05sightings2.xml"
        targetStringList = ["Aldebaran", None, None, None, "16d32.3", "109d27.8","S53d38.4","74d35.3","173d34.4","-3988"]
        theFix = F.Fix(self.DEFAULT_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        assumedLatitude = "S53d38.4"
        assumedLongitude = "74d35.3"
        theFix.getSightings(assumedLatitude,assumedLongitude)
        
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Lat/Lon entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        print(self.RANDOM_LOG_FILE)
        #self.deleteNamedLogFlag = True  
        
    def test300_060_ShouldReturnCorrectTupleWithSample1(self):
        'parse sighting file that valid tags'
        testFile = "CA05sightings2.xml"
        expectedResult = ("S13d28.0", "101d42.2")
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setStarFile(self.starFileName)
        theFix.setAriesFile(self.ariesFileName)
        assumedLatitude = "S53d38.4"
        assumedLongitude = "74d35.3"
        result = theFix.getSightings(assumedLatitude,assumedLongitude)
        self.assertTupleEqual(expectedResult, result, 
                              "Minor:  incorrect return value from getSightings")  
        
#sad path
    def test300_090_ShouldLogStarWithDefaultSightingValues(self):
        'log adjusted altitude for star using default values'
        testFile = self.mapFileToTest("validOneStarWithDefaultValues")

        targetStringList = ["Hadar", "2017-03-01", "23:40:01", "29d59.9"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Log entry is not correct for getSightings")
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True
 
#-----------        
    def test300_091_ShouldLogErrorOnMissingMandatoryTag(self):
        'Verify that missing mandatory tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidWithMissingMandatoryTags")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for missing mandatory tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True  

#----------
    def test300_092_ShouldLogErrorOnInvalidBody(self):
        'Verify that invalid body tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidBodyTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Minor:  failure to log number of sighting error for invalid body tag " + self.RANDOM_LOG_FILE)
        self.deleteNamedLogFlag = True

#----------
    def test300_093_ShouldLogErrorOnInvalidDate(self):
        'Verify that invalid date tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidDateTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for invalid date tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True

#----------
    def test300_094_ShouldLogErrorOnInvalidTime(self):
        'Verify that invalid time tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidTimeTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for invalid time tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True
        
#----------
    def test300_095_ShouldLogErrorOnInvalidObservation(self):
        'Verify that invalid observation tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidObservationTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for invalid observation tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True
        

#----------
    def test300_096_ShouldLogErrorOnInvalidHeight(self):
        'Verify that invalid height tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidHeightTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for invalid height tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True
        

#----------
    def test300_097_ShouldLogErrorOnInvalidTemperature(self):
        'Verify that invalid temperature tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidTemperatureTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setStarFile(self.starFileName)
        theFix.setAriesFile(self.ariesFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for invalid temperature tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True
        

#----------
    def test300_098_ShouldLogErrorOnInvalidPressure(self):
        'Verify that invalid pressure tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidPressureTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for invalid pressure tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True

#----------
    def test300_099_ShouldLogErrorOnInvalidHorizon(self):
        'Verify that invalid horizon tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidHorizonTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setStarFile(self.starFileName)
        theFix.setAriesFile(self.ariesFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for invalid horizon tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True        

    def test300_100_ShouldLogStarLatLon(self):
        'log geographical position with no interpolation of observation'
        testFile = self.mapFileToTest("validLatLon")
        targetStringList = ["Sabik", None, None, None, "-15d44.4", "247d23.7"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Lat/Lon entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True  
        
         
#-----------        
    def test300_110_ShouldLogStarLatLonWithInterpolation(self):
        'log geographical position'
        testFile = self.mapFileToTest("validLatLonInterpolated")
        targetStringList = ["Betelgeuse", None, None, None, "7d24.3", "75d54.3"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Lat/Lon entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True  
        
    def test300_120_ShouldLogStarLatLonWithBorderAssumedLatitude(self):
        'log geographical position with boder valid assumed latitude'
        testFile = self.mapFileToTest("validLatLon")
        targetStringList = ["Sabik", None, None, None, "-15d44.4", "247d23.7"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        assumedLatitude = "0d42.2"
        assumedLongitude = "300d52.0"
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Lat/Lon entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True  
        
    def test300_121_ShouldLogStarLatLonWithBorderAssumedLatitude(self):
        'log geographical position with boder valid assumed latitude'
        testFile = self.mapFileToTest("validLatLon")
        targetStringList = ["Sabik", None, None, None, "-15d44.4", "247d23.7"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        assumedLatitude = "N160d0.0"
        assumedLongitude = "300d52.0"
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Lat/Lon entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True     
         
    def test300_130_ShouldLogStarLatLonWithBorderAssumedLongitude(self):
        'log geographical position with boder valid assumed longitude'
        testFile = self.mapFileToTest("validLatLon")
        targetStringList = ["Sabik", None, None, None, "-15d44.4", "247d23.7"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        assumedLatitude = "S160d36.6"
        assumedLongitude = "0d52.0"
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Lat/Lon entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True  
        
    def test300_131_ShouldLogStarLatLonWithBorderAssumedLongitude(self):
        'log geographical position with boder valid assumed longitude'
        testFile = self.mapFileToTest("validLatLon")
        targetStringList = ["Sabik", None, None, None, "-15d44.4", "247d23.7"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        assumedLatitude = "S160d36.6"
        assumedLongitude = "300d59.9"
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Lat/Lon entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True  
#---------- 
    def test300_910_ShouldRaiseExceptionOnNotSettingSightingsFile(self):
        'Raise exception on failure to set sighting file'
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to set sighting file before getSightings()") 
    
    def test300_920_ShouldRaiseExceptionOnNotSettingStarFile(self):
        'Raise exception on failure to set star file'
        expectedDiag = self.className + "getSightings:"
        testFile = self.mapFileToTest("validOneStarSighting")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to set star file before getSightings()")   

    def test300_930_ShouldRaiseExceptionOnNotSettingAriesFile(self):
        'Raise exception on failure to set aries file'
        expectedDiag = self.className + "getSightings:"
        testFile = self.mapFileToTest("validOneStarSighting")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setStarFile(self.ariesFileName)   
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to set aries file before getSightings()") 
    
    def test300_940_ShouldRaiseExceptionOnInvalidAssumedLatitude(self):
        'Raise exception on invalid assumed latitude'
        expectedDiag = self.className + "getSightings:"
        testFile = "CA05sightings.xml"
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName) 
        theFix.setStarFile(self.ariesFileName)   
        assumedLatitude = "N90d59.2"
        assumedLongitude = "120d52.0"
        with self.assertRaises(ValueError) as context:
            theFix.getSightings(assumedLatitude,assumedLongitude)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to raise exception on invalid assumed latitude")    
 
    def test300_941_ShouldRaiseExceptionOnInvalidAssumedLatitude(self):
        'Raise exception on invalid assumed latitude'
        expectedDiag = self.className + "getSightings:"
        testFile = "CA05sightings.xml"
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName) 
        theFix.setStarFile(self.ariesFileName)   
        assumedLatitude = "S60d62.2"
        assumedLongitude = "120d52.0"
        with self.assertRaises(ValueError) as context:
            theFix.getSightings(assumedLatitude,assumedLongitude)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to raise exception on invalid assumed latitude") 
        
    def test300_942_ShouldRaiseExceptionOnInvalidAssumedLatitude(self):
        'Raise exception on invalid assumed latitude'
        expectedDiag = self.className + "getSightings:"
        testFile = "CA05sightings.xml"
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName) 
        theFix.setStarFile(self.ariesFileName)   
        assumedLatitude = "60d62.2"
        assumedLongitude = "120d52.0"
        with self.assertRaises(ValueError) as context:
            theFix.getSightings(assumedLatitude,assumedLongitude)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to raise exception on invalid assumed latitude")
        
    def test300_943_ShouldRaiseExceptionOnInvalidAssumedLatitude(self):
        'Raise exception on invalid assumed latitude'
        expectedDiag = self.className + "getSightings:"
        testFile = "CA05sightings.xml"
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName) 
        theFix.setStarFile(self.ariesFileName)   
        assumedLatitude = "S0d0.0"
        assumedLongitude = "120d52.0"
        with self.assertRaises(ValueError) as context:
            theFix.getSightings(assumedLatitude,assumedLongitude)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to raise exception on invalid assumed latitude")          

    def test300_950_ShouldRaiseExceptionOnInvalidAssumedLongitude(self):
        'Raise exception on invalid assumed latitude'
        expectedDiag = self.className + "getSightings:"
        testFile = "CA05sightings.xml"
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName) 
        theFix.setStarFile(self.ariesFileName)   
        assumedLatitude = "S60d42.2"
        assumedLongitude = "360d52.0"
        with self.assertRaises(ValueError) as context:
            theFix.getSightings(assumedLatitude,assumedLongitude)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to raise exception on invalid assumed latitude")

    def test300_951_ShouldRaiseExceptionOnInvalidAssumedLongitude(self):
        'Raise exception on invalid assumed latitude'
        expectedDiag = self.className + "getSightings:"
        testFile = "CA05sightings.xml"
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName) 
        theFix.setStarFile(self.ariesFileName)   
        assumedLatitude = "S60d42.2"
        assumedLongitude = "320d62.0"
        with self.assertRaises(ValueError) as context:
            theFix.getSightings(assumedLatitude,assumedLongitude)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to raise exception on invalid assumed latitude")

#  helper methods
    def indexInList(self, target, searchList):
        for index in range(len(searchList)):
            if(target in searchList[index]):
                return index
        return -1
    
    def mapFileToTest(self, target):
        for item in self.testToFileMap:
            if(item[0] == target):
                return item[1]
        return None