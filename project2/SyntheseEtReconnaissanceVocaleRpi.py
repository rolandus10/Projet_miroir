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
myName = "Santo"
snowWhite=False
misUnderstood = False
tl= 2 # for little sentences
tL= 5 # for long sentences
t = tl # default configuration
BING_KEY = "daf975c2970740f8b09c48d35b8926fd" # Microsoft Bing Voice Recognition API key
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
		
		
		# recognize speech using Google Speech Recognition
		# try:
			# for testing purposes, we're just using the default API key
			# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
			# instead of `r.recognize_google(audio)`
			# message = r.recognize_google(audio)
			# print("Vous : " + message)
			# del audio
		# except sr.UnknownValueError:
			# answer("Je n'ai pas compris, pouvez-vous répéter ?")
			# message = ""
		# except sr.RequestError as e:
			# print("Could not request results from Google Speech Recognition service; {0}".format(e))
			# message = ""
		
		try:
			message = r.recognize_bing(audio, key=BING_KEY, language = "fr-FR")
			print("Vous : " + message )
			del audio
		except sr.UnknownValueError:
			answer("Je n'ai pas compris, pouvez-vous répéter ?", 3.5)
			message = ""
			misUnderstood = True
		except sr.RequestError as e:
			print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
			message =""
		# search if the answer exists
		if(re.search("comment vas-tu",message) or re.search("comment ça va",message) ):
			answer("Je vais bien et vous ?")
		elif(re.search("que peux tu faire",message) or re.search("de quoi es-tu capable",message)):
			if(random.randint(1,2)==1):
				answer("Je peux faire de nombreuses choses comme vous donner votre horaire ou le menu de la cité", tL)
			else:
				answer("Je peux discuter avec vous {} et c'est un plaisir.".format(myName),3.5)
		elif(message == "bonjour" or message == "salut"): 
			answer("Bonjour {}".format(myName))
		elif(re.search("agenda", message) or re.search("planning", message) or re.search("horaire", message)): 
			answer("Voici votre horaire du jour, {} :".format(myName))
		# elif(re.search("météo",message)):
			# answer("Voilà la météo : ")
		elif(re.search("au revoir", message) or re.search("à bientôt", message)):
			answer("A bientôt {} !".format(myName))
			discuss = False
		elif(re.search("quel est ton nom", message) or re.search("tu appelles", message)): 
			print("Mon nom est Hi Reflect")
			#execute_command("Mon nom est aie riflect")	# to take into account the french accent
		elif((re.search("plus beau", message) or re.search("plus belle", message)) and snowWhite==False):
			answer("Um... J'hésite entre Blanche Neige et vous, voulez-vous vraiment que je réponde à cette question ?",6.0)
			snowWhite = True
		elif((re.search("bien sur", message) or re.search("oui", message)) and snowWhite== True):
			if(random.randint(1,2)==1):
				answer("C'est vous {}, comment cela aurait-il pu en être autrement ?".format(myName), tL)
			else:
				answer("Désolé, mon grand-père m'a appris que c'est Blanche Neige. Mais selon moi c'est vous {}".format(myName),6.0)
			snowWhite = False
		elif(re.search("^bien joué$", message)):
			answer("Oh, merci {} j'essaie de faire de mon mieux pour vous !".format(myName))
		# elif(re.search("what else$",message)):
			# answer("Sorry, I'm not already able to bring you a Nespresso coffee")
		elif(re.search("bonne blague", message)):
			answer("Merci {}, j'apprends beaucoup à vos côtés".format(myName), tL)
		elif(re.search("qui est le meilleur", message)):
			answer("{}, c'est vous ! Quelle question ...".format(myName))
		else:
			if(misUnderstood==True):
				misUnderstood=False
			else:
				t=0
			
			
		# to avoid him listening to himself
		time.sleep(t) # stop execution 
		t=tl # reset stop time
			
os.system("pause")
