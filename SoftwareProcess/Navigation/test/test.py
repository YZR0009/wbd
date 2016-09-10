'''
Created on Sep 8, 2016

@author: yunfanrao
'''
from Navigation.prod import Angle 
from logging import raiseExceptions


angle1 = Angle.Angle()
angle2 = Angle.Angle()
angle3 = Angle.Angle()
angle4 = Angle.Angle()

degrees = 10


print("\n**********now testing the set method****************")
try:
    angle1Degree = angle1.setDegreesAndMinutes("45d0.0")
    angle2Degree = angle2.setDegrees(degrees = -19.5)                     #Y
    angle3Degree = angle3.setDegreesAndMinutes("0d30.0")
    angle2.setDegrees("")
except ValueError as raiseExceptions:
    diagnosticString = raiseExceptions.args[0]
    print(diagnosticString)

#the angleString in this list all must be legal
angleRightList = ["45d10.1","45d10","0d0","0d0.1","700d1","700d61","-10d0","-10d1"]

for angle in angleRightList:
    try:
        angle4Degree = angle4.setDegreesAndMinutes(angle)
        print(angle4.degree)
        print(angle4.minute)
    except ValueError as raiseExceptions:
        diagnosticString = raiseExceptions.args[0]
        print(diagnosticString)

#the angleString in this list all must be illegal 
angleFalseList = ["d10.0","10d","10","0.1d0","0d-10","0d5.44","xd10","10dy","10:30","","6d8."]
for angle in angleFalseList:
    try:
        angle4Degree = angle4.setDegreesAndMinutes(angle)
        print(angle4.degree)
        print(angle4.minute)
    except ValueError as raiseExceptions:
        diagnosticString = raiseExceptions.args[0]
        print(diagnosticString)

print("\n**********now testing the add method***************")
try:
    addedDegree1=angle1.add(angle2)
    addedDegree2=angle2.add(angle3)
    print(addedDegree1)
    print(addedDegree2)
except ValueError as raiseExceptions:
    diagnosticString = raiseExceptions.args[0]
    print(diagnosticString)
try:
    angle1.add("42d0")
except ValueError as raiseExceptions:
    diagnosticString = raiseExceptions.args[0]
    print(diagnosticString)

print("\n**********now testing the subtract method***************")
try:
    subtractDegree=angle4.subtract(angle1)
    print(subtractDegree)
except ValueError as raiseExceptions:
    diagnosticString = raiseExceptions.args[0]
    print(diagnosticString)
try:
    angle1.subtract(0)
except ValueError as raiseExceptions:
    diagnosticString = raiseExceptions.args[0]
    print(diagnosticString)
   
print("\n**********now testing the compare method***************")
try:
    angle1.setDegrees(45.0)
    angle2.setDegrees(45.1)
    result1 = angle1.compare(angle2)
    result2 = angle2.compare(angle1)
    print(result1)
    print(result2)
except ValueError as raiseExceptions:
    diagnosticString = raiseExceptions.args[0]
    print(diagnosticString)

try:
    angle1.compare(42.5)
except ValueError as raiseExceptions:
    diagnosticString = raiseExceptions.args[0]
    print(diagnosticString)
   
print("\n**********now testing the getString method***************")
try:
    angle1String=angle1.getString()
    angle2String=angle2.getString()
    angle3.setDegrees(45.123)
    angle3String=angle3.getString()
    print(angle1String)
    print(angle2String)
    print(angle3String)
except ValueError as raiseExceptions:
    diagnosticString = raiseExceptions.args[0]
    print(diagnosticString)

print("\n**********now testing the getDegree method***************")
try:
    angle1Degree = angle1.getDegrees()
    angle2Degree = angle2.getDegrees()
    angle3Degree = angle3.getDegrees()
    print(angle1Degree)
    print(angle2Degree)
    print(angle3Degree)
except ValueError as raiseExceptions:
    diagnosticString = raiseExceptions.args[0]
    print(diagnosticString)
