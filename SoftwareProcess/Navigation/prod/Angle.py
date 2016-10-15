import re
from math import floor

class Angle():
    def __init__(self):
        self.degree = 0
        self.minute = 0
    
    def setDegrees(self, degrees = 0):
        if not (isinstance(degrees, int) or isinstance(degrees, float)):    
            raise ValueError("Angle.setDegrees:  Degree must be a number!")           
        else:
            if isinstance(degrees, int):
                degrees = float(degrees)
            self.degree = degrees%360
            self.minute = 0
            return self.degree
    
    def setDegreesAndMinutes(self, angleString):
        if not isinstance(angleString, str):
            raise ValueError("Angle.setDegreesAndMinutes:  The parameter must be a string!")
        matchAngle = re.match( r'^(\-?\d+) d ((\d+)$ | (\d+\.{1}\d{1})$)',angleString,re.X)
        if matchAngle:
            self.degree = int(matchAngle.group(1))
            if '.' in matchAngle.group(2):
                self.minute = float(matchAngle.group(2))
                self.minute = round(self.minute,1)
            else:
                self.minute = int(matchAngle.group(2))
            if self.degree < 0:
                self.minute = 0 - self.minute
            if self.minute > 60:
                self.degree += self.minute/60
                self.minute %= 60
            self.degree %= 360
            self.minute = round(self.minute, 1)
            return self.getDegrees()
        else:         
            if angleString == "":
                raise ValueError("Angle.setDegreesAndMinutes:  null string") 
            if angleString[0] == 'd':
                raise ValueError("Angle.setDegreesAndMinutes:  Missing degree")
            if angleString[-1] == 'd':
                raise ValueError("Angle.setDegreesAndMinutes:  Missing minute")
            matchAngle = re.match( r'^(.*) d (.*)$',angleString,re.X)
            if matchAngle:
                if not matchAngle.group(1).isdigit():
                    raise ValueError("Angle.setDegreesAndMinutes:  degree must be an integer")
                if not matchAngle.group(2).isdigit():
                    if '-' in matchAngle.group(2):
                        raise ValueError("Angle.setDegreesAndMinutes:  minute must be positive")
                    if re.match(r'^\d+\.\d{2,}$',matchAngle.group(2)):
                        raise ValueError("Angle.setDegreesAndMinutes:  minute must have only one decimal place")
                    if re.match(r'^\d+\.$',matchAngle.group(2)):
                        raise ValueError("Angle.setDegreesAndMinutes:  minute must have digit to the right of decimal point")
                    raise ValueError("Angle.setDegreesAndMinutes:  minute must be a number")
            else:
                raise ValueError("Angle.setDegreesAndMinutes:  Missing separator")
    
    def add(self, angle = None):
        if not isinstance(angle, Angle):
            raise ValueError("Angle.add:  only the instance of Angle can use add()")  
        tDegree1 = self.getDegrees()
        tDegree2 = angle.getDegrees()
        self.degree = round(tDegree1 + tDegree2,1)
        self.degree %= 360
        self.minute = 0
        return self.degree
    
    def subtract(self, angle = None):
        if not isinstance(angle, Angle):
            raise ValueError("Angle.subtract:  only the instance of Angle can use subtract()")  
        tDegree1 = self.getDegrees()
        tDegree2 = angle.getDegrees()
        self.degree = round(tDegree1 - tDegree2,1)
        self.degree %=360
        self.minute = 0
        return self.degree
    
    def compare(self, angle = None):
        if not isinstance(angle, Angle):
            raise ValueError("Angle.compare:  only the instance of Angle can use compare()")  
        tDegree1 = self.getDegrees()
        tDegree2 = angle.getDegrees()
        if tDegree1 > tDegree2 :
            return 1
        elif tDegree1 == tDegree2:
            return 0
        else:
            return -1
    
    def getString(self):
        string = ""
        if isinstance(self.degree, float):
            self.minute = round((self.degree - floor(self.degree))*60,1)
            self.degree = floor(self.degree)
            self.degree = int(self.degree)
        string += str(self.degree)
        string += "d"
        if self.minute < 10:
            string += "0"
        string += str(self.minute)
        return string
 
    def getDegrees(self):
        tDegree = self.degree
        tMinute = self.minute + tDegree * 60
        tMinute = round(tMinute,1)
        tDegree = tMinute / 60.0
        tDegree %= 360
        return tDegree

    

            
    
    
    
    