'''
Created on Oct 8, 2016

@author: yunfanrao
'''
import unittest
import Navigation.prod.Fix as Fix

class FixTest(unittest.TestCase):
    
    def setUp(self):
        self.myLogFile = "myLog.txt"
        self.missingTagSightingFile = "missingTagSightings.xml"
        self.InvalidedInfoSightingFile = "InvalidedInfoSightings.xml"
        self.InvalidedOAltitudeSightingFile = "InvalidedOAltitudeSightings.xml"
        
    def tearDown(self):
        pass

#-----------------------------------------------------------------
#-----Acceptance Tests:100
#       Analysis constructor
#          input:
#             logFile   string .GE.1 optional  
#          output:
#             instance of Fix
#          state change:
#             create a new file   or    write "Start of log"
#          Happy path:
#             empty input(missing logFile): logFile == None, create a new file
#             normal value: logFile = "a.txt"
#          Sad path:
#             non-string: logFile = 123
#             out of bound: logFile = ""
#
#Happy path

    def test100_010_ShouldCreateInstanceOfFix(self):
        self.assertIsInstance(Fix.Fix(), Fix.Fix)

    def test100_020_ShouldCreateInstanceOfFix(self):
        self.assertIsInstance(Fix.Fix("a.txt"), Fix.Fix)

#Sad path

    def test100_910_ShouldRaiseExceptionOnNonStringLogFile(self):
        expectedString = "Fix.__init__:  "
        with self.assertRaises(ValueError) as context:
            Fix.Fix(123)                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
             
    def test100_920_ShouldRaiseExceptionOnLengthOfLogFileLessthanOne(self):
        expectedString = "Fix.__init__:  "
        with self.assertRaises(ValueError) as context:
            Fix.Fix("")                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
            
#-----------------------------------------------------------------
#-----Acceptance Tests:200
#       Analysis setSightingFile
#          input:
#             sightingFile f.xml  f: string .GE.1 optional  Mandatory, unvalidated
#          output:
#             A string having the value passed as the "sightingFile".
#          state change:
#             write "Start of sighting file f.xml"
#          Happy path:
#             sightingFile = "a.xml"
#          Sad path:
#             missing sightingFile: setSightingFile()
#             non-string: sightingFile = 123
#             missing f: sightingFile = ".xml"
#             non-existent sightingFile: sightingFile = "inexistent.xml"
#Happy path
    def test200_010_ShouldReturntheNameOfSightingFile(self):
        fix = Fix.Fix(self.myLogFile)
        sFile = fix.setSightingFile("sightingFile.xml")
        self.assertEquals("sightingFile.xml", sFile)

#Sad path
    def test200_910_ShouldRaiseExceptionOnMissSightingFile(self):
        expectedString = "Fix.setSightingFile:  "
        with self.assertRaises(ValueError) as context:
            fix = Fix.Fix(self.myLogFile)
            fix.setSightingFile()                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
 
    def test200_920_ShouldRaiseExceptionOnNonStringSightingFile(self):
        expectedString = "Fix.setSightingFile:  "
        with self.assertRaises(ValueError) as context:
            fix = Fix.Fix(self.myLogFile)
            fix.setSightingFile(123)                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
                    
    def test200_930_ShouldRaiseExceptionOnMissF(self):
        expectedString = "Fix.setSightingFile:  "
        with self.assertRaises(ValueError) as context:
            fix = Fix.Fix(self.myLogFile)
            fix.setSightingFile(".xml")                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 

    def test200_940_ShouldRaiseExceptionOnInexistentSightingFile(self):
        expectedString = "Fix.setSightingFile:  "
        with self.assertRaises(ValueError) as context:
            fix = Fix.Fix(self.myLogFile)
            fix.setSightingFile("inexistent.xml")                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 

#-----------------------------------------------------------------
#-----Acceptance Tests:300
#       Analysis getSightings
#          input:
#             none
#          output:
#             A tuple consisting of the latitude and longitude
#          state change:
#             navigational calculations are written to log file
#          Happy path:
#             normal value: sightingFile.xml
#          Sad path:
#             no sighting file has been set 
#             missing a mandatory tag in sighting file
#             the info associated with a tag is invalid
#             the observed altitude are .LT. 0.1 arc-minutes
#Happy path

    def test300_010_ShouldReturnTuple(self):
        fix = Fix.Fix(self.myLogFile)
        sFile = fix.setSightingFile("sightingFile.xml")
        tuple = fix.getSightings()
        expectedTuple = "0d0.0","0d0.0"
#        self.assertEquals([["15d01.5"],["45d11.9"]], tuple)
        self.assertEquals(expectedTuple, tuple)

#Sad path

    def test300_910_ShouldRaiseExceptionOnNoSightingFileHasBeenSet(self):
        expectedString = "Fix.getSightings:  "
        fix = Fix.Fix(self.myLogFile)
        with self.assertRaises(ValueError) as context:
            tuple = fix.getSightings()                         
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])     

    def test300_920_ShouldRaiseExceptionOnMissingMandatoryTags(self):
        expectedString = "Fix.getSightings:  "
        fix = Fix.Fix(self.myLogFile)
        fix.setSightingFile("missingTagsSightings.xml")
        with self.assertRaises(ValueError) as context:
            tuple = fix.getSightings()                         
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])    

    def test300_930_ShouldRaiseExceptionOnInvalidedInforOfTags(self):
        expectedString = "Fix.getSightings:  "
        fix = Fix.Fix(self.myLogFile)
        fix.setSightingFile("InvalidedInfoSightings.xml")
        with self.assertRaises(ValueError) as context:
            tuple = fix.getSightings()                         
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 

    def test300_940_ShouldRaiseExceptionOnTooLessObservedAltitude(self):
        expectedString = "Fix.getSightings:  "
        fix = Fix.Fix(self.myLogFile)
        fix.setSightingFile("InvalidedOAltitudeSightings.xml")
        with self.assertRaises(ValueError) as context:
            tuple = fix.getSightings()                         
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
