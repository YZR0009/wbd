import re
from math import floor

class Angle():
    def __init__(self):
        self.degree = 0
        self.minute = 0
        pass
    
    def setDegrees(self, degrees):
        if degrees == None:
            degrees = 0
        if isinstance(degrees, int) or isinstance(degrees, float):    
            self.degree = degrees%360
            self.minute = 0
        else:
            raise ValueError("Angle.setDegree:  Degree must be a number!")
        pass
    
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
            if self.minute > 60:
                self.degree += self.minute/60
            self.degree %= 360
            self.minute %= 60
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
        pass
    
    def add(self, angle):
        if not isinstance(angle, Angle):
            raise ValueError("Angle.add:  only the instance of Angle can use add()")  
        tDegree1 = self.getDegrees()
        tDegree2 = angle.getDegrees()
        self.degree = round(tDegree1 + tDegree2,1)
        self.degree %= 360
        self.minute = 0
        return self.degree
        pass
    
    def subtract(self, angle):
        if not isinstance(angle, Angle):
            raise ValueError("Angle.substract:  only the instance of Angle can use subtract()")  
        tDegree1 = self.getDegrees()
        tDegree2 = angle.getDegrees()
        self.degree = round(tDegree1 - tDegree2,1)
        self.degree %=360
        self.minute = 0
        return self.degree
        pass
    
    def compare(self, angle):
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
        pass
    
    def getString(self):
        string = ""
        if isinstance(self.degree, float):
            self.minute = round((self.degree - floor(self.degree))*60,1)
            self.degree = floor(self.degree)
            self.degree = int(self.degree)
        string += str(self.degree)
        string += "d"
        string += str(self.minute)
        return string
        pass  
    
    def getDegrees(self):
        tDegree = self.degree
        self.minute = float(self.minute)
        tDegree += round(self.minute/60,1)
        tDegree %= 360
        return tDegree
        pass
    

            
    
    
    
    