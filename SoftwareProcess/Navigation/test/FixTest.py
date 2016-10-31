import unittest
import uuid
import os
import Navigation.prod.Fix as F
from numpy import absolute

class TestFix(unittest.TestCase):
    
    def setUp(self):
        self.className = "Fix."
        self.logStartString = "Log file:"
        self.logSightingString = "Sighting file:"
        self.logAriesString = "Aries file:"
        self.logStarString = "Star file:"
        
        # set default log file name
        self.DEFAULT_LOG_FILE = "log.txt"
        self.MYLOG = "mylog.txt"
        if(os.path.isfile(self.DEFAULT_LOG_FILE)):
            os.remove(self.DEFAULT_LOG_FILE)
        
        # generate random log file name
        self.RANDOM_LOG_FILE = "log" + str(uuid.uuid4())[-12:] + ".txt"
        
        self.SIGHTINGS_FILE = "sightingFile.xml"
        
        self.ARIES_FILE = "aries.txt"
        self.STAR_FILE = "stars.txt"
    

# 100 Constructor
#    Analysis
#        inputs:
#            logFile: string, optional, unvalidated, len >= 1
#        outputs:
#            returns:  instance of Fix
#            also:    writes "Start of log" to log file
#
#    Happy tests:
#        logFile:  
#            omitted  -> Fix()
#            new logfile  -> Fix("randomName.txt")
#            existing logfile  -> Fix("myLog.txt") (assuming myLog.txt exits)
#    Sad tests:
#        logFile:
#            nonstring -> Fix(42)
#            length error -> Fix("")
#            
    def test100_010_ShouldConstructFix(self):
        'Fix.__init__'
        self.assertIsInstance(F.Fix(), F.Fix, 
                              "Major error:  Fix not created")
         
    def test100_020_ShouldConstructFixWithDefaultFile(self):
        theFix = F.Fix()
        try:
            theLogFile = open(self.DEFAULT_LOG_FILE, 'r')
            entry = theLogFile.readline()
            del theLogFile
            self.assertNotEquals(-1, entry.find(self.logStartString), 
                                 "Minor:  first line of log is incorrect")
        except IOError:
            self.fail()
        self.assertIsInstance(theFix, F.Fix, 
                              "Major:  log file failed to create")
        
    def test100_025_ShouldConstructWithKeywordParm(self):
        try:
            theFix = F.Fix(logFile=self.RANDOM_LOG_FILE)
            self.assertTrue(True)
        except:
            self.fail("Minor: incorrect keyword specified")
            self.cleanup()
 
         
    def test100_030_ShouldConstructFixWithNamedFile(self):
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        try:
            theLogFile = open(self.RANDOM_LOG_FILE, 'r')
            entry = theLogFile.readline()
            del theLogFile
            self.assertNotEquals(-1, entry.find(self.logStartString), 
                                 "Minor:  first line of log is incorrect")
        except IOError:
            self.fail()
        self.assertIsInstance(theFix, F.Fix, "major:  log file failed to create")
        self.cleanup()  
        
    def test100_040_ShouldConstructFixWithExistingFile(self):
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        try:
            theLogFile = open(self.RANDOM_LOG_FILE, 'r')
            numberOfExpectedEntries = 2
            for _ in range(numberOfExpectedEntries):
                entry = theLogFile.readline()
                self.assertNotEquals(-1, entry.find(self.logStartString), 
                                     "Minor:  first line of log is incorrect")
        except IOError:
            self.fail()
        self.assertIsInstance(theFix, F.Fix, 
                              "Major:  log file failed to create")
        self.cleanup()  
        
    def test100_910_ShouldRaiseExceptionOnFileNameLength(self):
        expectedDiag = self.className + "__init__:"
        with self.assertRaises(ValueError) as context:
            F.Fix("")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)], 
                          "Minor:  failure to check for log file name length")  
        
    def test100_920_ShouldRaiseExceptionOnNonStringFile(self):
        expectedDiag = self.className + "__init__:"
        with self.assertRaises(ValueError) as context:
            F.Fix(42)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)], 
                          "Minor:  failure to check for non-string log file name")  
        
        
# 200 setSightingFile
#    Analysis
#        inputs:
#            sightingFile: string, mandatory, unvalidated, format = f.xml (len(f) >= 1)
#        outputs:
#            returns:  absolutePath of sighting file
#            also:    writes "Sighting file:" + absolutePath of sighting file to log file
#
#    Happy tests:
#        sightingFile:  
#            legal file name  -> setSightingFile("sightingFile.xml")  
#    Sad tests:
#        sightingFile:
#            nonstring -> setSightinghFile(42)
#            length error -> setSightingFile(".xml")
#            nonXML -> setSightingFile("sightingFile.txt")
#            missing -> setSightingFile()
#            nonexistent file -> setSightingFile("missing.xml")
    def test200_010_ShouldConstructWithKeywordParm(self):
        'Minor:  '
        theFix = F.Fix(logFile=self.RANDOM_LOG_FILE)
        try:
            result = theFix.setSightingFile("CA02_200_ValidStarSightingFile.xml")
            absolutePath = os.path.abspath("CA02_200_ValidStarSightingFile.xml")
            self.assertEquals(result, absolutePath)
        except:
            self.fail("Minor: incorrect keyword specified in setSighting parm")
        self.cleanup()   

    def test200_020_ShouldSetValidSightingFile(self):
        theFix = F.Fix()
        result = theFix.setSightingFile("CA02_200_ValidStarSightingFile.xml")
        absolutePath = os.path.abspath("CA02_200_ValidStarSightingFile.xml")
        self.assertEquals(result,absolutePath)
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        self.assertNotEquals(-1, logFileContents[-1].find(self.logSightingString), 
                             "Minor:  first setSighting logged entry is incorrect")
        theLogFile.close()
        
    def test200_910_ShouldRaiseExceptionOnNonStringFileName(self):
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile(42)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non-string sighting file name")  
        
    def test200_920_ShouldRaiseExceptionOnFileLengthError(self):
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile(".xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for .GE. 1 sighting file name") 
        
    def test200_930_ShouldRaiseExceptionOnNonXmlFile1(self):
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("sighting.")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non.xml sighting file extension")
        
    def test200_940_ShouldRaiseExceptionOnNonXmlFile2(self):
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to delineate between sighting file name and extension") 
        
    def test200_950_SholdRaiseExceptionOnMissingFileName(self):
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to check for missing sighting file")       
        
           
    def test200_960_SholdRaiseExceptionOnMissingFile(self):
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile(self.RANDOM_LOG_FILE+".xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to check for missing sighting file") 
 
 # 300 setAriesFile
#    Analysis
#        inputs:
#            ariesFile: string, mandatory, unvalidated, format = f.txt (len(f) >= 1)
#        outputs:
#            returns:  absolutePath of aries file
#
#    Happy tests:
#        ariesFile:  
#            legal file name  -> setAriesFile("aries.txt")  
#    Sad tests:
#        ariesFile:
#            nonstring -> setAriesFile(42)
#            length error -> setAriesFile(".txt")
#            nonTXT -> setAriesFile("aries.xml")
#            missing -> setAriesFile()
#            nonexistent file -> setAriesFile("missing.txt")
    def test300_010_ShouldConstructWithKeywordParm(self):
        'Minor:  '
        theFix = F.Fix(logFile=self.RANDOM_LOG_FILE)
        try:
            result = theFix.setAriesFile("aries.txt")
            absolutePath = os.path.abspath("aries.txt")
            self.assertEquals(result, absolutePath)
        except:
            self.fail("Minor: incorrect keyword specified in setSighting parm")
        self.cleanup()   
 
    def test300_020_ShouldSetValidAriesFile(self):
        theFix = F.Fix()
        result = theFix.setAriesFile("aries.txt")
        absolutePath = os.path.abspath("aries.txt")
        self.assertEquals(result,absolutePath)
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        self.assertNotEquals(-1, logFileContents[-1].find(self.logAriesString), 
                             "Minor:  first setSighting logged entry is incorrect")
        theLogFile.close()
               
    def test300_910_ShouldRaiseExceptionOnNonStringFileName(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile(42)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non-string sighting file name")  
        
    def test300_920_ShouldRaiseExceptionOnFileLengthError(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile(".txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for .GE. 1 sighting file name") 
        
    def test300_930_ShouldRaiseExceptionOnNonXmlFile1(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile("aries.xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non.xml sighting file extension")
        
    def test300_940_ShouldRaiseExceptionOnNonXmlFile2(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile("xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to delineate between sighting file name and extension") 
        
    def test300_950_SholdRaiseExceptionOnMissingFileName(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to check for missing sighting file")       
        
           
    def test300_960_SholdRaiseExceptionOnMissingFile(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile(self.RANDOM_LOG_FILE+".txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to check for missing sighting file") 

 # 400 setStarFile
#    Analysis
#        inputs:
#            starFile: string, mandatory, unvalidated, format = f.txt (len(f) >= 1)
#        outputs:
#            returns:  absolutePath of star file
#
#    Happy tests:
#        starFile:  
#            legal file name  -> setStarFile("stars.txt")  
#    Sad tests:
#        starFile:
#            nonstring -> setStarFile(42)
#            length error -> setStarFile(".txt")
#            nonTXT -> setStarFile("stars.xml")
#            missing -> setStarFile()
#            nonexistent file -> setStarFile("missing.txt")
    def test400_010_ShouldConstructWithKeywordParm(self):
        'Minor:  '
        theFix = F.Fix(logFile=self.RANDOM_LOG_FILE)
        try:
            result = theFix.setStarFile(self.STAR_FILE)
            absolutePath = os.path.abspath(self.STAR_FILE)
            self.assertEquals(result, absolutePath)
        except:
            self.fail("Minor: incorrect keyword specified in setSighting parm")
        self.cleanup()   
 
    def test400_020_ShouldSetValidStarFile(self):
        theFix = F.Fix()
        result = theFix.setStarFile(self.STAR_FILE)
        absolutePath = os.path.abspath(self.STAR_FILE)
        self.assertEquals(result,absolutePath)
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        self.assertNotEquals(-1, logFileContents[-1].find(self.logStarString), 
                             "Minor:  first setSighting logged entry is incorrect")
        theLogFile.close()
               
    def test400_910_ShouldRaiseExceptionOnNonStringFileName(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile(42)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non-string sighting file name")  
        
    def test400_920_ShouldRaiseExceptionOnFileLengthError(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile(".txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for .GE. 1 sighting file name") 
        
    def test400_930_ShouldRaiseExceptionOnNonXmlFile1(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile("starts.xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non.xml sighting file extension")
        
    def test400_940_ShouldRaiseExceptionOnNonXmlFile2(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile("xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to delineate between sighting file name and extension") 
        
    def test400_950_SholdRaiseExceptionOnMissingFileName(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to check for missing sighting file")       
        
           
    def test400_960_SholdRaiseExceptionOnMissingFile(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile(self.RANDOM_LOG_FILE+".txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to check for missing sighting file") 
        
# 500 getSightings
#    Analysis
#        inputs:
#            via parm:  none
#            via file:  xml description of sighting
#            via file:  txt description of stars
#            via file:  txt description of aries
#        outputs:
#            returns:    (latitude, longitude)
#            via file:    writes body /t date /t time /t adjusted altitude /t latitude /t longitude in sorted order
#        entry criterion:
#            setSightingsFile,setAriesFile and setStarFile must be called first
#
#    Happy tests:
#        sighting file 
#            valid file with single sightings1 (Pollus) -> should return ("27d59.1", "84d33.4")
#            valid file with single sightings2 (Sirius) -> should return ("-16d44.5", "239d13.1")
#            valid file with multiple sightings -> should log star bodies in sorted order
#            valid file with multiple sightings -> should log sighting error

#    Sad tests:
#        sightingFile:
#            sighting file not previously set
#            aries file not previously set
#            star file not previously set

    def test500_010_ShouldReturnCorrectLatitudeAndLongitude(self):
        testFile = "CA03_500_SampleSightingFile1.xml"
        expectedResult = ("27d59.1","84d33.4")
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ARIES_FILE)
        theFix.setStarFile(self.STAR_FILE)
        result = theFix.getSightings()
        self.assertTupleEqual(expectedResult, result, 
                              "Minor:  incorrect return value from getSightings")

    def test500_015_ShouldReturnCorrectLatitudeAndLongitude(self):
        testFile = "CA03_500_SampleSightingFile2.xml"
        expectedResult = ("-16d44.5","239d13.1")
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ARIES_FILE)
        theFix.setStarFile(self.STAR_FILE)
        result = theFix.getSightings()
        self.assertTupleEqual(expectedResult, result, 
                              "Minor:  incorrect return value from getSightings")

    def test500_020_ShouldLogMultipleSightingsInTimeOrder(self):       
        testFile = "CA03_500_sampleTest.xml"
        targetStringList = [
            ["Pollux", "2017-04-14", "23:50:14", "15d01.5","27d59.1","84d33.4"],
            ["Sirius", "2017-04-09", "09:30:30", "45d11.9","-16d44.5","239d13.1"]
            ]
        theFix = F.Fix(self.MYLOG)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ARIES_FILE)
        theFix.setStarFile(self.STAR_FILE)
        theFix.getSightings()
        
        theLogFile = open(self.MYLOG, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        # find entry with first star
        entryIndex = self.indexInList(targetStringList[0][0], logFileContents)
        self.assertLess(-1, entryIndex, 
                           "failure to find " + targetStringList[0][0] +  " in log")
        for index in range(entryIndex+1, len(targetStringList)):
            entryIndex += 1
            if(not(targetStringList[index][0] in logFileContents[entryIndex])):
                self.fail("failure to find star in log")
        self.cleanup()
        
    def test500_030_ShouldLogSightingError(self):       
        testFile = "CA03_500_sampleTest.xml"
        targetStringList = ["Sighting error", "1"]
        theFix = F.Fix(self.MYLOG)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ARIES_FILE)
        theFix.setStarFile(self.STAR_FILE)
        theFix.getSightings()
        
        theLogFile = open(self.MYLOG, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        # find entry with first star
        entryIndex = self.indexInList(targetStringList[0], logFileContents)
        self.assertLess(-1, entryIndex, 
                           "failure to write " + targetStringList[0] +  " in log")
        for index in range(entryIndex+1, len(targetStringList)):
            entryIndex += 1
            if(not(targetStringList[index] in logFileContents[entryIndex])):
                self.fail("failure to calculate sighting errors in log")
        self.cleanup()
        

#Sad Path

    def test500_910_ShouldRaiseExceptionOnNotSettingSightingsFile(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        theFix.setAriesFile(self.ARIES_FILE)
        theFix.setStarFile(self.STAR_FILE)
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to set sighting file before getSightings()") 

    def test500_920_ShouldRaiseExceptionOnNotSettingAriesFile(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        theFix.setSightingFile(self.SIGHTINGS_FILE)
        theFix.setStarFile(self.STAR_FILE)
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to set sighting file before getSightings()") 

    def test500_930_ShouldRaiseExceptionOnNotSettingStarsFile(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        theFix.setSightingFile(self.SIGHTINGS_FILE)
        theFix.setAriesFile(self.ARIES_FILE)
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to set sighting file before getSightings()") 

#     def test500_010_ShouldIgnoreMixedIndentation(self):
#         testFile = "CA02_300_GenericValidStarSightingFile.xml"
#         expectedResult = ("0d0.0", "0d0.0")
#         theFix = F.Fix()
#         theFix.setSightingFile(testFile)
#         result = theFix.getSightings()
#         self.assertTupleEqual(expectedResult, result, 
#                               "Minor:  incorrect return value from getSightings")
# 
#     def test500_020_ShouldIgnoreMixedIndentation(self):
#         testFile = "CA02_300_ValidWithMixedIndentation.xml"
#         theFix = F.Fix()
#         theFix.setSightingFile(testFile)
#         try:
#             theFix.getSightings()
#             self.assertTrue(True)
#         except:
#             self.fail("Major: getSightings failed on valid file with mixed indentation")  
# 
#     def test500_030_ShouldLogOneSighting(self):
#         testFile = "CA02_300_ValidOneStarSighting.xml"
#         targetStringList = ["Aldebaran", "2016-03-01", "23:40:01"]
#         theFix = F.Fix(self.RANDOM_LOG_FILE)
#         theFix.setSightingFile(testFile)
#         theFix.getSightings()
#         
#         theLogFile = open(self.RANDOM_LOG_FILE, "r")
#         logFileContents = theLogFile.readlines()
#         theLogFile.close()
#         
#         sightingCount = 0
#         for logEntryNumber in range(0, len(logFileContents)):
#             if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
#                 sightingCount += 1
#                 for target in targetStringList:
#                     self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
#                                          "Major:  Log entry is not correct for getSightings")
#         self.assertEquals(1, sightingCount)
#         self.cleanup()  
        
#     def test500_040_ShouldLogMultipleSightingsInTimeOrder(self):       
#         testFile = "CA02_300_ValidMultipleStarSighting.xml"
#         targetStringList = [
#             ["Sirius", "2016-03-01", "00:05:05"],
#             ["Canopus", "2016-03-02", "23:40:01"]
#             ]
#         theFix = F.Fix(self.RANDOM_LOG_FILE)
#         theFix.setSightingFile(testFile)
#         theFix.getSightings()
#         
#         theLogFile = open(self.RANDOM_LOG_FILE, "r")
#         logFileContents = theLogFile.readlines()
#         theLogFile.close()
#         
#         # find entry with first star
#         entryIndex = self.indexInList(targetStringList[0][0], logFileContents)
#         self.assertLess(-1, entryIndex, 
#                            "failure to find " + targetStringList[0][0] +  " in log")
#         for index in range(entryIndex+1, len(targetStringList)):
#             entryIndex += 1
#             if(not(targetStringList[index][0] in logFileContents[entryIndex])):
#                 self.fail("failure to find star in log")
#         self.cleanup()  

#     def test500_050_ShouldLogMultipleSightingsWithSameDateTime(self):       
#         testFile = "CA02_300_ValidMultipleStarSightingSameDateTime.xml"
#         targetStringList = [
#             ["Acrux", "2016-03-01", "00:05:05"],
#             ["Sirius", "2016-03-01", "00:05:05"],
#             ["Canopus", "2016-03-02", "23:40:01"]
#             ]
#         theFix = F.Fix(self.RANDOM_LOG_FILE)
#         theFix.setSightingFile(testFile)
#         theFix.getSightings()
#         
#         theLogFile = open(self.RANDOM_LOG_FILE, "r")
#         logFileContents = theLogFile.readlines()
#         theLogFile.close()
#         
#         # find entry with first star
#         entryIndex = self.indexInList(targetStringList[0][0], logFileContents)
#         self.assertLess(-1, entryIndex, 
#                            "failure to find " + targetStringList[0][0] +  " in log")
#         for index in range(entryIndex+1, len(targetStringList)):
#             entryIndex += 1
#             if(not(targetStringList[index][0] in logFileContents[entryIndex])):
#                 self.fail("failure to find star in log")
#         self.cleanup()   

#     def test500_060_ShouldHandleNoSightings(self):       
#         testFile = "CA02_300_ValidWithNoSightings.xml"
#         targetString1 = "Sighting errors"
#         targetString2 = "Sighting file"
#         
#         theFix = F.Fix(self.RANDOM_LOG_FILE)
#         theFix.setSightingFile(testFile)
#         theFix.getSightings()
#         
#         theLogFile = open(self.RANDOM_LOG_FILE, "r")
#         logFileContents = theLogFile.readlines()
#         theLogFile.close()
#         
#         endOfSightingFileIndex = self.indexInList(targetString1, logFileContents)
#         self.assertLess(-1,endOfSightingFileIndex,
#                            "log file does not contain 'end of sighting file' entry")
#         self.assertLess(1, endOfSightingFileIndex,
#                            "log file does not contain sufficient entries")
#         self.assertTrue((targetString2 in logFileContents[endOfSightingFileIndex - 1]))
#         self.cleanup()   
#         
#     def test500_070_ShouldIgnoreExtraneousTags(self):       
#         testFile = "CA02_300_ValidWithExtraneousTags.xml"
#         targetStringList = [
#             ["Sirius", "2016-03-01", "00:05:05"],
#             ]
#         theFix = F.Fix(self.RANDOM_LOG_FILE)
#         theFix.setSightingFile(testFile)
#         theFix.getSightings()
#         
#         theLogFile = open(self.RANDOM_LOG_FILE, "r")
#         logFileContents = theLogFile.readlines()
#         theLogFile.close()
#         
#         # find entry with first star
#         entryIndex = self.indexInList(targetStringList[0][0], logFileContents)
#         self.assertLess(-1, entryIndex, 
#                            "failure to find " + targetStringList[0][0] +  " in log")
#         for index in range(entryIndex+1, len(targetStringList)):
#             entryIndex += 1
#             if(not(targetStringList[index][0] in logFileContents[entryIndex])):
#                 self.fail("failure to find star in log")
#         self.cleanup()    
# 
# 
#     def test500_080_ShouldLogStarWithNaturalHorizon(self):
#         testFile = "CA02_300_ValidOneStarNaturalHorizon.xml"
#         targetStringList = ["Hadar", "2016-03-01", "23:40:01", "29d55.7"]
#         theFix = F.Fix(self.RANDOM_LOG_FILE)
#         theFix.setSightingFile(testFile)
#         theFix.getSightings()
#         
#         theLogFile = open(self.RANDOM_LOG_FILE, "r")
#         logFileContents = theLogFile.readlines()
#         theLogFile.close()
#         
#         sightingCount = 0
#         for logEntryNumber in range(0, len(logFileContents)):
#             if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
#                 sightingCount += 1
#                 for target in targetStringList:
#                     self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
#                                          "Major:  Log entry is not correct for getSightings")
#         self.assertEquals(1, sightingCount)
#         self.cleanup()  
# 
# 
#     def test500_080_ShouldLogStarWithArtificialHorizon(self):
#         testFile = "CA02_300_ValidOneStarArtificialHorizon.xml"
#         targetStringList = ["Hadar", "2016-03-01", "23:40:01", "29d55.7"]
#         theFix = F.Fix(self.RANDOM_LOG_FILE)
#         theFix.setSightingFile(testFile)
#         theFix.getSightings()
#         
#         theLogFile = open(self.RANDOM_LOG_FILE, "r")
#         logFileContents = theLogFile.readlines()
#         theLogFile.close()
#         
#         sightingCount = 0
#         for logEntryNumber in range(0, len(logFileContents)):
#             if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
#                 sightingCount += 1
#                 for target in targetStringList:
#                     self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
#                                          "Major:  Log entry is not correct for getSightings")
#         self.assertEquals(1, sightingCount)
#         self.cleanup()  
        
#         
#     def test500_090_ShouldLogStarWithDefaultSightingValues(self):
#         testFile = "CA02_300_ValidOneStarWithDefaultValues.xml"
#         targetStringList = ["Hadar", "2016-03-01", "23:40:01", "29d59.9"]
#         theFix = F.Fix(self.RANDOM_LOG_FILE)
#         theFix.setSightingFile(testFile)
#         theFix.getSightings()
#         
#         theLogFile = open(self.RANDOM_LOG_FILE, "r")
#         logFileContents = theLogFile.readlines()
#         theLogFile.close()
#         
#         sightingCount = 0
#         for logEntryNumber in range(0, len(logFileContents)):
#             if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
#                 sightingCount += 1
#                 for target in targetStringList:
#                     self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
#                                          "Major:  Log entry is not correct for getSightings")
#         self.assertEquals(1, sightingCount)
#         self.cleanup()  
# 
#     def test500_910_ShouldRaiseExceptionOnNotSettingSightingsFile(self):
#         expectedDiag = self.className + "getSightings:"
#         theFix = F.Fix()
#         with self.assertRaises(ValueError) as context:
#             theFix.getSightings()
#         self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
#                           "Major:  failure to set sighting file before getSightings()")   
#         
#     def test500_920_ShouldRaiseExceptionOnMissingMandatoryTag(self):
#         expectedDiag = self.className + "getSightings:"
#         theFix = F.Fix()
#         with self.assertRaises(ValueError) as context:
#             theFix.setSightingFile("CA02_300_InvalidWithMissingMandatoryTags.xml")
#             theFix.getSightings()
#         self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
#                           "Major:  failure to check for missing mandatory tag")   
#         
#     def test500_930_ShouldRaiseExceptionOnInvalidBody(self):
#         expectedDiag = self.className + "getSightings:"
#         theFix = F.Fix()
#         with self.assertRaises(ValueError) as context:
#             theFix.setSightingFile("CA02_300_InvalidBody.xml")
#             theFix.getSightings()
#         self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
#                           "Major:  failure to check for invalid body")    
#         
#     def test500_940_ShouldRaiseExceptionOnInvalidDate(self):
#         expectedDiag = self.className + "getSightings:"
#         theFix = F.Fix()
#         with self.assertRaises(ValueError) as context:
#             theFix.setSightingFile("CA02_300_InvalidDate.xml")
#             theFix.getSightings()
#         self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
#                           "Major:  failure to check for invalid body") 
#         
#     def test500_950_ShouldRaiseExceptionOnInvalidTime(self):
#         expectedDiag = self.className + "getSightings:"
#         theFix = F.Fix()
#         with self.assertRaises(ValueError) as context:
#             theFix.setSightingFile("CA02_300_InvalidTime.xml")
#             theFix.getSightings()
#         self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
#                           "Major:  failure to check for invalid body")    
#         
#     def test500_960_ShouldRaiseExceptionOnInvalidObservation(self):
#         expectedDiag = self.className + "getSightings:"
#         theFix = F.Fix()
#         with self.assertRaises(ValueError) as context:
#             theFix.setSightingFile("CA02_300_InvalidObservation.xml")
#             theFix.getSightings()
#         self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
#                           "Major:  failure to check for invalid body")       
#         
#     def test500_970_ShouldRaiseExceptionOnInvalidHeight(self):
#         expectedDiag = self.className + "getSightings:"
#         theFix = F.Fix()
#         with self.assertRaises(ValueError) as context:
#             theFix.setSightingFile("CA02_300_InvalidHeight.xml")
#             theFix.getSightings()
#         self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
#                           "Major:  failure to check for invalid body" )
#         
#     def test500_980_ShouldRaiseExceptionOnInvalidTemperature(self):
#         expectedDiag = self.className + "getSightings:"
#         theFix = F.Fix()
#         with self.assertRaises(ValueError) as context:
#             theFix.setSightingFile("CA02_300_InvalidTemperature.xml")
#             theFix.getSightings()
#         self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
#                           "Major:  failure to check for invalid body" )
#         
#     def test500_990_ShouldRaiseExceptionOnInvalidPressure(self):
#         expectedDiag = self.className + "getSightings:"
#         theFix = F.Fix()
#         with self.assertRaises(ValueError) as context:
#             theFix.setSightingFile("CA02_300_InvalidPressure.xml")
#             theFix.getSightings()
#         self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
#                           "Major:  failure to check for invalid body" )
#         
#     def test500_995_ShouldRaiseExceptionOnInvalidHorizon(self):
#         expectedDiag = self.className + "getSightings:"
#         theFix = F.Fix()
#         with self.assertRaises(ValueError) as context:
#             theFix.setSightingFile("CA02_300_InvalidHorizon.xml")
#             theFix.getSightings()
#         self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
#                           "Major:  failure to check for invalid body" )
        
               


        

#  helper methods
    def indexInList(self, target, searchList):
        for index in range(len(searchList)):
            if(target in searchList[index]):
                return index
        return -1
    
    def cleanup(self):
        if(os.path.isfile(self.RANDOM_LOG_FILE)):
            os.remove(self.RANDOM_LOG_FILE)  