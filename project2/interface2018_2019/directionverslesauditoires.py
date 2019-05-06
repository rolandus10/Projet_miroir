# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 02:21:00 2019

@author: djakd
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re# permet de faire des recherches très précises dans une chaîne de caractère
import time
import datetime
import random
# NOTE: this example requires PyAudio because it uses the Microphone class
import speech_recognition as sr #librairie de reconnaisssance vocal
import subprocess
import speak # permet de faire resortire la voix

# text to speek function
#def execute_command(str):
#	""" For openning eSpeak module"""
#	subprocess.Popen(['C:\Program Files (x86)\eSpeak\command_line\espeak.exe', str])

# configuration
my_Name = "patrick"
tl= 2 # for little sentences
tL= 5 # for long sentences
t = tl # default configuration
r = sr.Recognizer()
lang ="fr-FR"
recherche_direction=False

# answer function 
def answer(toSay, t_stop=tl):
	"""" print and say the 'toSay' variable and can modify time pause"""
	print(toSay)
	#execute_command(toSay)
	global t
	t=t_stop

# start to discuss 
discuss = True
with sr.Microphone(sample_rate = 32000) as source:
	while (discuss == True):
	
		# obtain audio from the microphone
		print("...") # to show he wait something from you
		audio = r.listen(source, 4, 6) # slowwwww
		print("..")	# to show he has recorded your demande
		
		#recuperer de l'enregistrement audio et reconnaissance vocal grace au package de google
		
		
		try:
			message = r.recognize_google(audio, language = "fr-FR")
			#print("Vous : " + message )
			del audio# permet de supprimer le message enregistré à chaque fois pour attendre le message suivant
		except sr.UnknownValueError:
			print("Je n'ai pas compris, pouvez-vous répéter ?")
			message = ""
			misUnderstood = True
		except sr.RequestError as e:
			print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
			message =""
		# search if the answer exists
		if(re.search("accueil merci", message)):
			answer("acceuil ok")
			navigator="accueil"
			recherche_direction=False
		elif(re.search("activité merci",message) or re.search("programme des études",message)):
			answer("ok")
			navigator="activité"
			recherche_direction=False
		elif(re.search("direction merci", message)):
			answer("direction ok")
			navigator="direction"
			recherche_direction=True
		elif(re.search("auditoire 25 merci",message) or re.search("25 merci",message) and recherche_direction==True):
			#answer("ok 25")
			direction="comme indiquez sur le plan, prenez à votre gauche ensuite montez jusqu'au deuxième étage l'auditoire est face à vous légèrement à droite"
			navigator="auditoire 25"
			speak.tts(direction, lang)
		elif(re.search("auditoire 11 merci",message) or re.search("11 merci",message) and recherche_direction==True):
			#answer("ok 11")
			direction="prenez à votre droite ensuite montez jusqu'au premier étage, l'auditoire est sur votre gauche"
			navigator="auditoire 11"
			speak.tts(direction, lang)
		elif(re.search("auditoire 12 merci",message) or re.search("12 merci",message) and recherche_direction==True): 
			#answer("ok 12")
			direction="prenez à votre droite ensuite montez jusqu'au premier étage puis tournez à droite, vous êtes arrivez"
			navigator="auditoire 12"
			speak.tts(direction, lang)
		elif(re.search("auditoire 23 merci",message) or re.search("23 merci",message) and recherche_direction==True):
			#answer("ok 23")
			direction="Prenez à votre droite jusqu'à l'escalier, montez jusqu'au deuxième étage puis faite quelques pas sur votre gauche l'auditoire se trouve à droite"
			navigator="auditoire 23"
			speak.tts(direction, lang)
		elif(re.search("c'est gentil", message) or re.search("merci miroir", message)):
			direction="non, ne me remerciez pas"
			speak.tts(direction, lang)
			navigator="accueil"
			discuss = False
		elif(re.search("auditoire 04 merci",message) or re.search("réfectoire merci",message) and recherche_direction==True):
			#answer("ok 05")
			direction="comme indiquer sur le plan prenez à votre droite jusqu'au IGLAB puis tournez à droite, la destination est à votre droite"
			speak.tts(direction, lang)
		elif(re.search("hall d'entrer merci",message) or re.search("secrétariat des étudiants merci",message)and recherche_direction==True):
		
			navigator="auditoire 23"
			speak.tts("vous y êtes",lang)
		
		else:
			if(misUnderstood==True):
				misUnderstood=False
			else:
				t=0
			
			
		# to avoid him listening to himself
		time.sleep(t) # stop execution 
		t=tl # reset stop time
			
os.system("pause")
