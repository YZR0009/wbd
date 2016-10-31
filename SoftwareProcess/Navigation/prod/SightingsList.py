'''
Created on Oct 11, 2016

@author: yunfanrao
'''
#from xml.dom.minidom import parse 
import xml.dom.minidom 
import re
from datetime import datetime

class SightingsList(object):


    def __init__(self, sightingFile = None):
        if sightingFile == None:
            raise ValueError("SightingsLish.__inint__:  must f.xml as a paramount")
        self.DOMTree = xml.dom.minidom.parse(sightingFile) 
        self.Data = self.DOMTree.documentElement 
        self.fix = None
        self.sightings = None
        self.body = []
        self.date = []
        self.time = []
        self.observation = []
        self.height = []
        self.temperature = []
        self.pressure = []
        self.horizon = []
        self.count = 0

    def get_fix(self):
        self.fix = self.Data.getElementsByTagName("fix")

    def get_sightings(self):
        self.sightings = self.Data.getElementsByTagName("sighting")
        for sighting in self.sightings:
            self.count += 1

    def get_body(self):
        for sighting in self.sightings:
            self.body.append(str(sighting.getElementsByTagName("body")[0].childNodes[0].data))
        return self.body

    def get_date(self):
        for sighting in self.sightings:
            self.date.append(str(sighting.getElementsByTagName("date")[0].childNodes[0].data))
        return self.date

    def get_time(self):
        for sighting in self.sightings:
            self.time.append(str(sighting.getElementsByTagName("time")[0].childNodes[0].data))
        return self.time

    def get_observation(self):
        for sighting in self.sightings:
            self.observation.append(str(sighting.getElementsByTagName("observation")[0].childNodes[0].data))
        return self.observation

    def get_height(self):
        for sighting in self.sightings:
            try:
                self.height.append(str(sighting.getElementsByTagName("height")[0].childNodes[0].data))
            except:
                self.height.append("0")
        return self.height

    def get_temperature(self):
        for sighting in self.sightings:
            try:
                self.temperature.append(str(sighting.getElementsByTagName("temperature")[0].childNodes[0].data))
            except:
                self.temperature.append("72")
        return self.temperature

    def get_pressure(self):
        for sighting in self.sightings:
            try:
                self.pressure.append(str(sighting.getElementsByTagName("pressure")[0].childNodes[0].data))
            except:
                self.pressure.append("1010")
        return self.pressure

    def get_horizon(self):
        for sighting in self.sightings:
            try:
                self.horizon.append(str(sighting.getElementsByTagName("horizon")[0].childNodes[0].data))
            except:
                self.horizon.append("natural")
        return self.horizon

    def get_count(self):
        return self.count
    
    def checkError(self):
        if self.fix == None or self.sightings == None:
            return True
        for i in range(self.count):
            if not self.body[i].isalpha():
                return True
            try:
                datetime.strptime(self.date[i],"%Y-%m-%d")
                datetime.strptime(self.time[i],"%H:%M:%S")
            except:
                return True
            isObservationWrong = self.isObservationError(self.observation[i])
            if isObservationWrong:
                return True
            try:
                float(self.height[i])
                int(self.temperature[i])
                int(self.pressure[i])
            except:
                return True
            if float(self.height[i]) < 0:
                return True
            if (int(self.temperature[i]) < -2) or (int(self.temperature[i]) > 120):
                return True
            if (int(self.pressure[i]) < 100) or (int(self.pressure[i]) > 1100):
                return True
            natural = "natural"
            artificial = "artificial"
            if not ((self.horizon[i].lower() == natural.lower()) 
                                   or (self.horizon[i].lower() == artificial.lower())):
                return True
        return False
                
    def isObservationError(self,observation):     
        matchAngle = re.match( r'^(\-?\d+) d ((\d+)$ | (\d+\.{1}\d{1})$)',observation,re.X)
        if matchAngle:
            degree = int(matchAngle.group(1))
            if '.' in matchAngle.group(2):
                minute = float(matchAngle.group(2))
                minute = round(minute,1)
            else:
                minute = int(matchAngle.group(2))
            if (degree < 0) or (degree >= 90):
                return True
            if (minute < 0 ) or (minute >= 60): 
                return True
            return False