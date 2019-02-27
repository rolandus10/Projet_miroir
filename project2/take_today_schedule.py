# -*-coding:UTF-8 -*

from open_horaire import *

studentId=151771 #come from facial and vocal recognitions
pEvent, otherEvents = giveSchedule(studentId)
#deltaT si on veut l'horaire d'un autre jour --> possibilité d'amélioration du code pour étendre les fonctionnalités

print(pEvent)
print("\n")
print(otherEvents)
