# -*-coding:UTF-8 -*
#need to install the pdfminer package
#sudo apt-get install python-pdfminer

import pdf_recuperation as rec
import os
from classes import *

def getDayName(day):

    if day==0:
        day="Lundi"
    elif day==1:
        day="Mardi"
    elif day==2:
        day="Mercredi"
    elif day==3:
        day="Jeudi"
    elif day==4:
        day="Vendredi"    #it's what we find at the end of the menu
    elif day==5:
        day="www"
    else:
        day=None     #no menu on the weekend
    return day


def getMenu(decal=0):
    #open the PDF file and convert it using PDF class of slate

    saveName,date=rec.recupPDF(decal)
    
    try:
        with open(saveName,'rb') as file :
            infos = PDF(file)
    except:
        print("Pas de menu trouvé")
        return None

    chaine = infos.text(False)    #text is a method of the class PDF, False because we keep the special characters like \n

    day1=getDayName(date.tm_wday)
    day2=getDayName(date.tm_wday+1)

    if day1 == None or day2 == None :
        menu = "Pas de menu disponible pour le weekend, désolé"
    else:
        pos1 = chaine.find(day1)
        pos2 = chaine.find(day2)
        
        content = chaine[pos1+len(day1):pos2]   #take just between the days without the names of days

        vec=content.split("\n\n")

        try:
            vec.remove(' ')
            vec.remove('')
        except ValueError:
            pass #do nothing (we don't care if there's nothing to remove from the vector

        menu=""
        for e in vec:
            menu+=e+"\n"

    return menu


