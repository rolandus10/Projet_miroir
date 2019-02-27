# -*-coding:Utf-8 -*
import os
import time
import sys
PYTHON_3 = sys.version_info[0] == 3

if PYTHON_3:
    import urllib.request
else:
    import urllib

def recupPDF(decal=0):

    date=time.localtime(time.time()+24*60*60*decal)      #for now if we don't precise a timestamp in parametre
    #on récupère le timestamp dans 'decal' jours...
    
    beginDate=date.tm_mday - date.tm_wday  #take the current day and cut a number to be on monday
    endDate=beginDate+4

    if date.tm_mon == 1:
        month = "JANVIER"
    elif date.tm_mon == 2:
        month = "FEVRIER"
    elif date.tm_mon == 3:
        month = "MARS"
    elif date.tm_mon == 4:
        month = "AVRIL"
    elif date.tm_mon == 5:
        month = "MAI"
    elif date.tm_mon == 6:
        month = "JUIN"
    elif date.tm_mon == 7:
        month = "JUILLET"
    elif date.tm_mon == 8:
        month = "AOUT"
    elif date.tm_mon == 9:
        month = "SEPTEMBRE"
    elif date.tm_mon == 10:
        month = "OCTOBRE"
    elif date.tm_mon == 11:
        month = "NOVEMBRE"
    elif date.tm_mon == 12:
        month = "DECEMBRE"

    saveName="Menu du "+str(beginDate)+" au "+str(endDate)+" "+month+'.pdf'
    
    try:

        #download the file only if necessary (once a week)

        fileOrNot = os.path.isfile(saveName)

        if fileOrNot == False :    

            filesNames = os.listdir("./")   #on supprime l'ancien pdf
            for f in filesNames:
                if ".pdf" in f:
                    os.remove(f)   

            url='http://portail.umons.ac.be/FR/universite/admin/aff_etudiant/restaurants/MENU/MENU%20DU%20'+str(beginDate)+'%20AU%20'+str(endDate)+'%20'+month+'.pdf'

            if PYTHON_3:
                urllib.request.urlretrieve(url,saveName)
            else:
                urllib.urlretrieve(url,saveName)

        return saveName,date
    
    except:
        print("Désolé, aucun menu disponible")
        return None,date
    
             



