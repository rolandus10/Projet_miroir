# -*-coding:UTF-8 -*

import pytz
from tzlocal import get_localzone
import datetime as d

local_tz = get_localzone()      #take same zone that in PC configuration !

def utcToLocal(utc_dt):       #found on stack
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


def findString(begin,end,event):
	
	pos1=event.find(begin)
	
	event=event[pos1:] #we delete the beginning to search correct end

	pos1=event.find(begin)+len(begin)
	
	pos2=event.find(end)

	return event[pos1:pos2]


def takeMatiere(event):
	
	matiere=findString("Matière","\n",str(event))	#we need a string to make searches
	
	matiere=matiere[::-1]	#reverse the string
	
	
	end=" -"
	pos2=matiere.find(end)
	matiere=matiere[0:pos2]

	matiere=matiere[::-1] #reverse the string

	return matiere

def takeSalle(event):
	
	return findString("Salle : ","\n",str(event))

def takeType(event):
	
	return findString("Type : ","\n",str(event))

def takeGroupe(event):

        return findString("TD : ","\n",str(event))

def takeEnseignant(event):

        enseignant=findString("Enseignant : ","\n",str(event))
        if(enseignant): #no string if more than one teacher
                return enseignant
        else:
                return findString("Enseignants : ","\n",str(event))

def takeTime(time):
        #time=utcToLocal(time)
        timeForm=str(time.hour)+":"+str(time.minute)
        return timeForm

def printSchedule(events,date):

        printed=False
        otherEvents=""
        otherEventsList=[]
        
        for e in events:
                
                matiere=takeMatiere(e.description)
                salle=takeSalle(e.description)
                typeEns=takeType(e.description)
                ens=takeEnseignant(e.description)
                groupe=takeGroupe(e.description)
                e.begin=utcToLocal(e.begin)
                e.end=utcToLocal(e.end)
                beginTime=takeTime(e.begin)
                endTime=takeTime(e.end)
                mtn=d.datetime.today()
                
                if not printed:

                    if ens:
                        wiv=" avec "+ens
                    else:
                        wiv=""
                    if salle:
                        loc=" au local "+salle
                    else:
                        loc=""
                    if typeEns:
                        tE=typeEns+" de "
                    else:
                        tE=""

                    if(((e.begin.hour*60+e.begin.minute)<=(mtn.hour*60+mtn.minute)) and ((mtn.hour*60+mtn.minute)<(e.end.hour*60+e.end.minute))):
                        
                        pEvent="Vous avez "+tE+matiere+wiv+loc+" actuellement. Dépéchez-vous, vous êtes en retard !"
                        printed=True
                        
                    elif((e.begin.hour*60+e.begin.minute)>(mtn.hour*60+mtn.minute)):
                        
                        pEvent="Vous avez "+tE+matiere+wiv+loc+" à "+beginTime 
                        printed=True

                    if " " in groupe:
                        pEvent="Votre horaire est affiché en bas de l'écran"    #car on sait pas dans quel groupe est l'étudiant
                        printed=True

                tmp=True   #magouille pour pas tenir compte du if de la ligne en-dessous
                if((e.begin.hour*60+e.begin.minute)>(mtn.hour*60+mtn.minute)) or tmp==True:  #on affiche que les événements restants de la journée

                    if ens:
                        wiv="  ["+ens+"]"
                    else:
                        wiv=""
                    if typeEns:
                        tE=" ("+typeEns+") "
                    else:
                        tE=""
                    if salle:
                        loc="   "+salle
                    else:
                        loc=""
                    if " " in groupe:   #plusieurs groupes suivent le cours
                        gr=" {"+groupe+"}"
                    else:
                        gr=""
                            
                    otherE=beginTime+"-"+endTime+" : "+matiere+tE+salle+wiv+gr

                    otherEvents+=otherE+"\n"    #on met tout dans un string plutot qu'une liste pour faciliter la procédure d'affichage dans l'interface

                    otherEventsList.append(otherE)


##                print("--------------------------------")
##                print(matiere)
##                print(salle)
##                print(typeEns)
##                print(ens)
##                print(beginTime)
##                print(endTime)
##                print("--------------------------------")
        if not printed:
            pEvent="Vous n'avez plus cours aujourd'hui, bonne fin de journée"

        return pEvent, otherEventsList
