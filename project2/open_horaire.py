# -*-coding:UTF-8 -*

from ics import Calendar
from ics import timeline as t
import datetime as d
from urllib.request import urlopen
from functionsHoraire import *
import os
import time #for cpu time measure
from operator import attrgetter
import mysql.connector


def giveSchedule(studentId,deltaT=0):

        db = mysql.connector.connect(host="localhost",user="HiReflect",password="pi=3.14", database="Students")
        cursor = db.cursor()
        req="""SELECT blocUrl
        FROM ((Student
        INNER JOIN TakeBloc
        ON TakeBloc.studentId=Student.studentId)
        INNER JOIN Bloc
        ON Bloc.blocId=TakeBloc.blocId)
        WHERE Student.studentId=%(studentId)s"""
        
        values={"studentId" : studentId}
        cursor.execute(req,values)
        rows=cursor.fetchall()

        if rows:
                urls=list()
                for row in rows:
                        urls.append(row[0])      #possible d'avoir plusieurs blocs suivis

        else:
                raise ValueError("Cet étudiant ne semble pas suivre de bloc !")
	
        #tmp1=time.clock()

        calendars=list()
        for url in urls:
                f=urlopen(url)
                calendars.append(Calendar(f.read().decode('utf8')))     #on met nos différents calendriers dans une liste

                f.close()

                #tmp2=time.clock()

                #print("TEMPS OUVERTURE DU FICHIER ET LECTURE : "+str(tmp2-tmp1))
	
        date=d.datetime.today() + d.timedelta(deltaT)
	
        #tmp1=time.clock()
        todayEvents=[]
        for c in calendars:  
                for e in c.events:
                        if date.year==e.begin.year and date.month==e.begin.month and date.day==e.begin.day:	#on recupere la date et on regarde si elle est contenue dans e.begin qui contient la date et l'heure
			
                                if not (("Annulation" or "annulation" or "ANNULATION") in str(e.description)):
                                        todayEvents.append(e)
    

        todayEvents.sort(key=attrgetter("begin"))       #sort using begin of the event

        pEvent,otherEventsList=printSchedule(todayEvents,date) 

        #tmp2=time.clock()
        #print("TEMPS LECTURE DES EVENTS ADEQUATS : "+str(tmp2-tmp1))

        return pEvent, otherEventsList



