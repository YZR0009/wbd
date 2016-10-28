'''
Created on Oct 9, 2016

@author: yunfanrao
'''
'''
functionName = "Fix.__init__:  "
defaultName = "log.txt"
logFormatString = "LOG:\t" 
startString = "Start of log\n"
logfile = open(defaultName,"a")
logfile.write(logFormatString + startString)  
'''
import Navigation.prod.SightingsList as S
import math
import Navigation.prod.Fix as F


sightingsList = S.SightingsList("sightingFile.xml")
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
xml_List.sort( key = lambda l: (l[1], l[2]) )    
print(xml_List)

if "3" > 2:
    print("y")
if "72" < -2:
    print("yy")
if "72" > 120:
    print("yyy")

from datetime import datetime
try:
    datetime.strptime("2011-03-31","%Y-%m-%d")
    datetime.strptime("23:12:59","%H:%M:%S")
except:
    print("F")
    
print(math.degrees(0.1/60))
print(math.radians(0.095))

#log = open("log.txt",'r')
log = open("log.txt",'a')
log.write("Start of log1\n")
log = open("log.txt",'a')
log.write("Start of log2")
log = open("log.txt",'r')
content = log.readlines()
print(content)
print(content[-1].find("Start of log"))
print(content[-1])
print(content[0])

