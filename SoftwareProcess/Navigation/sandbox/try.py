'''
Created on Oct 9, 2016

@author: yunfanrao
'''
from test.test_readline import readline
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
import datetime as d


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
#xml_List.sort( key = lambda l: (l[1], l[2]) )    
xml_list2 = sorted(xml_List, key = lambda l: (l[1], l[2]) ) 
print(xml_List)
print(xml_list2)
sortChange = [i for i in range(numberOfSighting)]
for i in range(numberOfSighting):
    for j in range(numberOfSighting):
        if xml_List[i] == xml_list2[j]:
            sortChange[i] = j
            print(sortChange[i])
    

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


log = open("log.txt",'r')
result = log.readline()
print(1)
print(result.find("Start"))
result = log.readline()
print(2)
print(result.find("of"))
result = log.readline()
print(3)
print(result)
result = log.readline()
print(4)
print(result)
if result == None:
    print("result equals None")
if result == "\n":
    print("result equals \n")
if result == "":
    print("result equals ")
    
sumString  = "Alpheratz\t01/01/17\t357d41.7\t29d10.9"
a = "Alpheratz" + "\t" + "01/01/17"
print(sumString.find(a))
strlist = sumString.split("\t")
print(strlist[0])
print(strlist[1])
print(strlist[2])
print(strlist[3])

for str in strlist:
    print(str)
#print(strlist[0])
# print(strlist[1])
# print(strlist[2])
# print(strlist[3])

d1 = d.datetime.strptime("10/15/16",'%m/%d/%y')
d3 = d1 + d.timedelta(days = -1)
print(d3.strftime('%m/%d/%y'))

str1 = "absfw\n"
str2 = str1.rstrip()
print(str2)
