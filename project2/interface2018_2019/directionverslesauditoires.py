# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 02:21:00 2019

@author: djakd
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import time
import datetime
import random
# NOTE: this example requires PyAudio because it uses the Microphone class
import speech_recognition as sr
import subprocess

# text to speek function
#def execute_command(str):
#	""" For openning eSpeak module"""
#	subprocess.Popen(['C:\Program Files (x86)\eSpeak\command_line\espeak.exe', str])

# configuration
myName = "patrick"
snowWhite=False
misUnderstood = False
tl= 2 # for little sentences
tL= 5 # for long sentences
t = tl # default configuration
r = sr.Recognizer()

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
		
		
		try:
			message = r.recognize_google(audio, language = "fr-FR")
			#print("Vous : " + message )
			del audio
		except sr.UnknownValueError:
			answer("Je n'ai pas compris, pouvez-vous répéter ?", 3.5)
			message = ""
			misUnderstood = True
		except sr.RequestError as e:
			print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
			message =""
		# search if the answer exists
		if(re.search("auditoire 24 merci",message) or re.search("24 merci",message)):
			answer("ok 24")
			navigator="auditoire 24"
			print(navigator)
		elif(re.search("auditoire 11 merci",message) or re.search("11 merci",message)):
			answer("ok 11")
			navigator="auditoire 11"
			print(navigator)
		elif(re.search("auditoire 12 merci",message) or re.search("12 merci",message)): 
			answer("ok 12")
			navigator="auditoire 12"
			print(navigator)
		elif(re.search("auditoire 23 merci",message) or re.search("23 merci",message)):
			answer("ok 23")
			navigator="auditoire 23"
			print(navigator)
		elif(re.search("c'est gentil", message) or re.search("c'est ok", message)):
			answer("A bientôt {} !".format(myName))
			discuss = False
		elif(re.search("auditoire 25 merci",message) or re.search("25 merci",message)): 
			answer("ok 25")
			navigator="auditoire 25"
			print(navigator)
		elif(re.search("05 merci",message) or re.search("réfectoire please",message)):
			answer("ok 05")
			navigator="auditoire 05"
			print(navigator)
		elif(re.search("hall d'entrer merci",message) or re.search("secrétariat des étudiants merci",message)):
			answer("vous y êtes")
		elif(re.search("accueil merci", message)):
			answer("acceuil ok")
			navigator="accueil"
			print(navigator)
		elif(re.search("activité merci",message) or re.search("programme des études",message)):
			answer("ok")
			navigator="activité"
			print(navigator)
		else:
			if(misUnderstood==True):
				misUnderstood=False
			else:
				t=0
			
			
		# to avoid him listening to himself
		time.sleep(t) # stop execution 
		t=tl # reset stop time
			
os.system("pause")
