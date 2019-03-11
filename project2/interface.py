# -*- coding : utf-8 -*-
# smartmirror.py
# requirements
# requests, feedparser, traceback, Pillow

from tkinter import *
from gtts import *
from mutagen.mp3 import MP3
import os
import vlc
import locale
import threading
import time
import requests
import json
import traceback
import feedparser
import re
import datetime
import random
import speech_recognition as sr
import subprocess
from PIL import Image, ImageTk
from contextlib import contextmanager
import cv2
import numpy as np
import mysql.connector
import sys
from lecture_menu import *
from open_horaire import *

LOCALE_LOCK = threading.Lock()

#--------------------------Variables globales--------------------------
ui_locale = '' # e.g. 'fr_FR' for French, '' as default
time_format = 24 # 12 or 24
date_format = "%d %b %Y" # check python doc for strftime() for options
news_country_code = 'fr_be'
weather_api_token = '2cc04380b7da65d63932b1eab9ed547b' # create account at https://darksky.net/dev/
weather_lang = 'fr' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'auto' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
latitude = None # Set this if IP location lookup does not work for you (must be a string)
longitude = None # Set this if IP location lookup does not work for you (must be a string)
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18
xsmall_text_size = 14
tiny_text_size = 11
counterMax=10

myName = "Inconnu"
mat = 1
horaire=False
w=None
discuss=True

tk=Tk()

tl= 2 # for little sentences
tL= 5 # for long sentences
t = tl # default configuration
BING_KEY = "310ac92800ef4b40ba2a58c5e43cec5a" # Microsoft Bing Voice Recognition API key
r = sr.Recognizer()



#--------------------------interface configuration--------------------------

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
icon_lookup = {
    'clear-day': "assets/Sun.png",  # clear sky day
    'wind': "assets/Wind.png",   #wind
    'cloudy': "assets/Cloud.png",  # cloudy day
    'partly-cloudy-day': "assets/PartlySunny.png",  # partly cloudy day
    'rain': "assets/Rain.png",  # rain day
    'snow': "assets/Snow.png",  # snow day
    'snow-thin': "assets/Snow.png",  # sleet day
    'fog': "assets/Haze.png",  # fog day
    'clear-night': "assets/Moon.png",  # clear sky night
    'partly-cloudy-night': "assets/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "assets/Storm.png",  # thunderstorm
    'tornado': "assests/Tornado.png",    # tornado
    'hail': "assests/Hail.png"  # hail
}

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# -------------------------------- TEXT --------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

        
class Text(Frame):
    def __init__(self, parent, text, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.contentText = text
        self.contentTextLbl = Label(self, text=self.contentText, font=('Helvetica', tiny_text_size), fg="white", bg="black")
        self.contentTextLbl.pack(side=LEFT, anchor=N)
    def updateText(self, newText):
        self.contentTextLbl.config(text=newText)
        
class TextBig(Frame):
    def __init__(self, parent, text, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.contentText = text
        self.contentTextLbl = Label(self, text=self.contentText, font=('Helvetica', xsmall_text_size), fg="white", bg="black")
        self.contentTextLbl.pack(side=LEFT, anchor=N)
    def updateText(self, newText):
        self.contentTextLbl.config(text=newText)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------ SPEECH RECOGNITION --------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

class SpeechRecognition(Frame):
    snowWhite = False
    misUnderstood = False
    anotherAnswerWaited = False
    shutUp = False
    feeling = False
    discuss = False
    counter = 0
    answerMessage = 'azcB-12' # to show that no answer message has been computed
    mySentenceMessage = 'azcB-11' # default config for customer request
    aczB_11Test=False
    def __init__(self, parent, ext = False, param = True,*args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        if param:
            self.frFunction()
        if not ext:
            self.listen()
    def frFunction(self):
        global mat, myName,discuss
        #if discuss == False:
        self.fr= FacialRecognition()            
        discuss=True
        #self.after(1000,self.frFunction)
    def register(self, text):
        tts = gTTS(text, lang='fr')
        file="text.mp3"
        tts.save(file)
        audio = MP3(file)
        p = vlc.MediaPlayer(file)
        p.play()
        time.sleep((audio.info.length)) #to avoid it listening to itself
        p.stop()
        return file
    def delete(self, file):
        os.remove(file)
    def say(self, text):
        file=self.register(text)
        self.delete(file)
    @staticmethod
    def audioInputReplacement():
        comptError=0
        # start to discuss
        while comptError<4:
            try:
                with sr.Microphone(sample_rate = 32000) as source:
                            
                    # obtain audio from the microphone
                    print("...") # to show he wait something from you
                    # signal to tell the user to speak
                    audio = r.listen(source, 3, 6)
                    print("..")    # to show he has recorded your demande and search on internet to build string sentence
                            
                    # recognize using BING
                    try:
                        message = r.recognize_bing(audio, key=BING_KEY, language = "fr-FR")
                        #print("Vous : " + message )
                        #self.mySentence("Vous : " + message)
                        #self.mySentenceMessage = 'azcB-11'
                        #self.counter = 0
                        del audio
                    except sr.UnknownValueError:
                        #self.answer("Je n'ai pas compris, pouvez-vous répéter ?")
                        #self.mySentence("")
                        #message = 'azcB-11'
                        #if self.counter == counterMax:
                        #    discuss = False
                        #    self.counter = 0
                        #else:
                        #    self.counter +=1
                        print("not x")
                    except sr.RequestError as e:
                        message =""
                return message
            except:
                comptError+=1
                
    def listen_ext(self):
        comptError=0
        # start to discuss
        while comptError<4:
            try:# start to discuss 
                with sr.Microphone(sample_rate = 32000) as source:
                            
                    # obtain audio from the microphone
                    print("...") # to show he wait something from you
                    # add a signal to tell the user to speak
                    audio = r.listen(source, 3, 6) 
                    print("..")    # to show he has recorded your demande and search on internet to build string sentence
                            
                    # recognize using BING
                    try:
                        message = r.recognize_bing(audio, key=BING_KEY, language = "fr-FR")
                        #self.mySentence("Vous : " + message)
                        #self.mySentenceMessage = 'azcB-11'
                        #self.counter = 0
                        del audio
                    except sr.UnknownValueError:
                        self.answer("Je n'ai pas compris, pouvez-vous répéter ?")
                        self.mySentence("erreur de compréhension")
                        message = 'azcB-11'
                        SpeechRecognition.misUnderstood = True
                        #if self.counter == counterMax:
                        #    discuss = False
                        #    self.counter = 0
                        #else:
                        #    self.counter +=1
                    except sr.RequestError as e:
                        print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
                        message =""
                    if(re.search("un",message)):
                        message = message.replace("un","1")
                    if(re.search("heures",message)):
                        message = message.replace("heures","1")
                    if(re.search("heure",message)):
                        message = message.replace("heure","1")
                    if(re.search("an",message)):
                        message = message.replace("an","1")
                    if(re.search("à",message)):
                        message = message.replace("à","1")
                    if(re.search("deux",message)):
                        message = message.replace("deux","2")
                    if(re.search("de",message)):
                        message = message.replace("de","2")
                    if(re.search("trois",message)):
                        message = message.replace("trois","3")
                    if(re.search("quatre",message)):
                        message = message.replace("quatre","4")
                    if(re.search("cat",message)):
                        message = message.replace("cat","4")
                    if(re.search("kat",message)):
                        message = message.replace("kat","4")
                    if(re.search("cinq",message)):
                        message = message.replace("cinq","5")
                    if(re.search("six",message)):
                        message = message.replace("six","6")
                    if(re.search("si",message)):
                        message = message.replace("si","6")
                    if(re.search("sis",message)):
                        message = message.replace("sis","6")
                    if(re.search("sept",message)):
                        message = message.replace("sept","7")
                    if(re.search("cette",message)):
                        message = message.replace("cette","7")
                    if(re.search("huit",message)):
                        message = message.replace("huit","8")
                    if(re.search("neuf",message)):
                        message = message.replace("neuf","9")
                    if(re.search("zéro",message)):
                        message = message.replace("zéro","0")
                    if(re.search("héro",message)):
                        message = message.replace("héro","0")
                    if(re.search("a",message)):
                        message = message.replace("a","1")
                    message = message.replace(" ","")
                return message
            except:
                comptError+=1
                        
    def listen(self):
        comptError=0
        # start to discuss
        global horaire,w,discuss
        global comptHoraire, myName,mat
        if discuss == False:
            self.frFunction()
        else:

            while comptError<4:
                try:
                    with sr.Microphone(sample_rate = 32000) as source:
                            
                        # obtain audio from the microphone
                        print("...") # to show he wait something from you
                        # add a signal to tell the user to speak
                        audio = r.listen(source, 3, 6)
                        print("..")    # to show he has recorded your demande and search on internet to build string sentence
                            
                        # recognize using BING
                        try:
                            message = r.recognize_bing(audio, key=BING_KEY, language = "fr-FR")
                            self.mySentence("Vous : " + message)
                            del audio
                        except sr.UnknownValueError:
                            self.mySentence("erreur de compréhension")
                            self.answer("Je n'ai pas compris, pouvez-vous répéter ?")
                            message = ""
                            self.misUnderstood = True
                            if self.counter == counterMax:
                                discuss = False
                                self.counter = 0
                            else:
                                self.counter +=1
                        except sr.RequestError as e:
                            self.answer("Erreur de connection au serveur, pouvez-vous répéter ?")
                            message =""
                                
                                
                                
                            #---------------------------search if the self.answer exists-------------------------------
                            
                        if(re.search("game over",message) or re.search("gameover",message)):
                            command = "/usr/bin/sudo /sbin/shutdown -h now"
                            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

                        elif(re.search("heure",message)):
                            self.answer("Il est {}".format(time.strftime('%H:%M')))

                        elif(re.search("ça va",message) and SpeechRecognition.feeling == True):
                            nombre = random.randint(1,4)
                            if(nombre == 1):
                                self.answer("Que puis-je faire pour vous {} ?".format(myName))
                            elif(nombre == 2):
                                self.answer("Quel plaisir d'interrompre ma sieste pour vous voir {}".format(myName))
                            elif(nombre ==3):
                                self.answer("Je peux vous aider ?")
                            else:
                                self.answer("Qu'est-ce qui vous ferait plaisir ?".format(myName))
                            del nombre
                                
                        elif(re.search("comment vas-tu",message) or re.search("comment allez-vous",message) or re.search("ça va",message) or re.search("tu vas bien", message)):
                            nombre = random.randint(1,6)
                            if(nombre == 1):
                                self.answer("Je vais bien et vous ?")
                            elif(nombre == 2):
                                self.answer("Quand je vous vois {}, je vais toujours bien ! Et vous ?".format(myName))
                            elif(nombre ==3):
                                self.answer("Comme ci comme ça... Vous savez, c'est dur de réfléchir tout le temps !")
                            elif(nombre ==4):
                                self.answer("Mieux depuis que vous êtes en face de moi {} !".format(myName))
                            elif(nombre ==5):
                                self.answer("Très bien merci {} ! Et vous ?".format(myName))
                            else:
                                self.answer("Ça va très bien ! Et vous {} ?".format(myName))
                            del nombre
                            SpeechRecognition.feeling = True

                        elif(re.search("question",message) or re.search("questionner",message) or re.search("interroger", message)):
                            nombre=random.randint(1,2)
                            if(nombre == 1):
                                self.answer("Je suis là pour vous servir maître {}".format(myName))
                            else:
                                self.answer("Bien sûr, à votre service")
                            del nombre
                                
                        elif(re.search("que peux tu faire",message) or re.search("de quoi es-tu capable",message)):
                            if(random.randint(1,2)==1):
                                self.answer("Je peux faire de nombreuses choses comme vous donner votre horaire ou le menu de la cité")
                            else:
                                self.answer("Je peux discuter avec vous {} et c'est un plaisir".format(myName))
                                    
                        elif(re.search("bonjour",message ) or  re.search("salut",message) or re.search("coucou",message)): 
                            nombre = random.randint(1,3)
                            if(nombre == 1):
                                self.answer("Bonjour {}".format(myName))
                            elif(nombre == 2):
                                self.answer("Salut {}".format(myName))
                            else:
                                self.answer("Bonjour")
                            del nombre
                                
                        elif(re.search("agenda", message) or re.search("planning", message) or re.search("horaire", message) or re.search("cours", message)):
                            
                            horaire=True
                            comptHoraire=0
                            pEvent, otherEvents = giveSchedule(mat)
                            w.news.get_headlines()
                            self.answer(pEvent)
                            
                        elif(re.search("cité", message) or re.search("resto", message) or re.search("restaurant", message) or re.search("mange",message) or re.search("mange",message) or re.search("menu",message)):
                            nombre = random.randint(1,4)
                            print("nombre={}".format(nombre))
                            if(nombre == 1):
                                tmp="Tant de bonnes choses"+myName+" : "
                            elif(nombre == 2):
                                tmp="J'ai déjà faim rien que d'y penser : "
                            elif(nombre ==3):
                                tmp="Je suis sûr que vous allez aimer : "
                            elif (nombre==4):
                                tmp="Voici le menu "+myName+", avec les compliments du chef : "
                            print("tmp :"+tmp)
                            if(re.search("demain", message)):
                                menu=tmp+"\n"+getMenu(1)
                            else:
                                menu=tmp+"\n"+getMenu()
                            print(menu)
                            self.answer(menu)
                            del nombre
                        elif(re.search("où sommes-nous",message ) or  re.search("ou sommes-nous",message) or re.search("où sommes nous",message) or re.search("ou sommes nous",message) or re.search("où suis-je",message ) or  re.search("ou suis-je",message) or re.search("où suis je",message) or re.search("ou suis je",message)): 
                            self.answer("Vous êtes à la Faculté Polytechnique de Mons")   
                        elif(re.search("au revoir", message) or re.search("à bientôt", message) or re.search("tchao", message)):
                            nombre = random.randint(1,4)
                            if(nombre == 1):
                                self.answer("A bientôt {} !".format(myName))
                            elif(nombre == 2):
                                self.answer("Je retourne à ma sieste...")
                            elif(nombre ==3):
                                self.answer("Au revoir !")
                            else:
                                self.answer("J'espère vous revoir vite !")
                            mat=1
                            myName = "Inconnu"
                            print(myName)
                            discuss = False
                            del nombre
                            
                        elif((re.search("non", message) or re.search("ça va aller", message) or re.search("rien", message)) and SpeechRecognition.anotherAnswerWaited==True):
                            if(random.randint(1,2)==1):
                                self.answer("D'accord {}, ce fût un plaisir de vous servir".format(myName))
                            else:
                                self.answer("Je vais retourner à ma sieste alors...")
                            SpeechRecognition.anotherAnswerWaited = False
                            discuss = False
                                
                        elif(re.search("merci", message)):
                            nombre = random.randint(1,4)
                            if(nombre == 1):
                                self.answer("Je vous en prie".format(myName))
                            elif(nombre == 2):
                                self.answer("C'est tout naturel")
                            elif(nombre ==3):
                                self.answer("De rien {}, puis-je faire autre chose ?".format(myName))
                                SpeechRecognition.anotherAnswerWaited = True
                            else:
                                self.answer("Mais de rien, souhaitez-vous autre chose ?")
                                SpeechRecognition.anotherAnswerWaited = True
                            del nombre
                            
                            
                        elif(re.search("ton nom", message) or re.search("tu (t')?appelles", message) or re.search("t'appelles-tu", message)): 
                            #self.answer("Mon nom est Hi Reflect", "mon nom est ailles... riflect")
                            nombre = random.randint(1,4)
                            if(nombre == 1):
                                self.answer("Mon nom est Mira")
                            elif(nombre == 2):
                                self.answer("Je suis Mira, pour vous servir")
                            elif(nombre ==3):
                                self.answer("Je m'appelle Mira, je suis programmée pour vous servir")
                            else:
                                self.answer("Mon nom est Mira, je suis là pour vous servir {}".format(myName))
                                SpeechRecognition.anotherAnswerWaited = True
                            del nombre
                            
                        #---------------------------localisation UMONS-------------------------------
                        
                        elif(re.search("secrétariat des études", message)):
                            self.answer("Le secrétariat des études se trouve au premier étage en face de l'auditoire 11")
                        elif(re.search("auditoire douze",message)):
                            self.answer("L'auditoire 12 se trouve au premier étage à votre droite après les escaliers","L'auditoire douze se trouve au premier étage à votre droite après les escaliers")
                        elif(re.search("auditoire un", message)):
                            self.answer("L'entrée se trouve dehors à coté de l'entrée de l'AIMS")
                        elif(re.search("labo",message) and re.search("physique",message)):
                            self.answer("Ces labos se trouvent au deuxième étage dans l'autre aile") 
                            
                        # ---------------------------exotic requests---------------------------------
                            
                        elif(re.search("je t'aime", message)):
                            nombre = random.randint(1,4)
                            if(nombre ==1):
                                self.answer("Voyons {}, on se connaît à peine...".format(myName))
                            elif(nombre ==2):
                                self.answer("C'est normal {}, je vous ressemble tellement !".format(myName))
                            elif(nombre ==3):
                                self.answer("Comme un fou, comme un soldat, comme une star de cinéma ?")
                            else:
                                self.answer("Moi aussi {} ! Mais... que dira votre famille ?".format(myName))
                            del nombre
                            
                        elif(re.search("tu m'aimes", message) or re.search("m'aimes-tu ?", message)):
                            nombre = random.randint(1,3)
                            if(nombre ==1):
                                self.answer("De tout mon processeur !")
                            elif(nombre ==2):
                                self.answer("{}, ne brusquons pas les choses... ".format(myName))
                            else:
                                self.answer("Je sors d'une rupture avec un bel intel Core i3 {}, je ne suis pas prêt à reconstruire quelque chose ...".format(myName))
                            del nombre
                            
                        elif(re.search("gros con", message) or re.search("enflure", message) or re.search("merde",message)):
                            nombre = random.randint(1,4)
                            if(nombre ==1):
                                self.answer("Vous ne le pensez pas !")
                            elif(nombre ==2):
                                self.answer("Pourquoi tant de haine dans ce monde ?")
                            elif(nombre ==3):
                                self.answer("Vous me brisez la carte mère...")
                            else:
                                self.answer("A vos souhaits")
                            del nombre
                            
                        elif((re.search("ta gueule", message) or re.search("la ferme", message)) and SpeechRecognition.shutUp==True):
                           self.answer("D'accord je ne dis plus rien")
                                
                        elif(re.search("ta gueule", message)):
                            if(random.randint(1,2)==1):
                                self.answer("Et la liberté d'expression des miroirs dans tout ça ?")
                            else:
                                self.answer("Voyons {}, je n'en ai pas !".format(myName))
                            SpeechRecognition.shutUp=True

                        elif(re.search("aimes-tu", message) or re.search("tu aimes", message) or re.search("t'aimes",message)):
                            self.answer("J'aime tout ce que vous aimez {}".format(myName))
                            
                        elif(re.search("j'aime", message)):
                            self.answer("Content de le savoir {}".format(myName))
                                
                        elif((re.search("plus beau", message) or re.search("plus belle", message)) and SpeechRecognition.snowWhite==False):
                            self.answer("J'hésite entre Blanche Neige et vous, voulez-vous vraiment que je réponde à cette question ?")
                            SpeechRecognition.snowWhite = True
                                
                        elif((re.search("bien sûr", message) or re.search("oui", message) or re.search("bien sur", message)) and SpeechRecognition.snowWhite== True):
                            if(random.randint(1,2)==1):
                                self.answer("C'est vous {}, comment cela aurait-il pu en être autrement ?".format(myName))
                            else:
                                self.answer("Désolé, mon grand-père m'a appris que c'était Blanche Neige. Mais selon moi c'est vous {}".format(myName))
                            SpeechRecognition.snowWhite = False
                                
                        elif(re.search("^bien joué$", message)):
                            self.answer("Oh, merci {} j'essaie de faire de mon mieux pour vous !".format(myName))
                                
                        elif(re.search("bonne blague", message)):
                            self.answer("Merci {}, j'apprends beaucoup à vos côtés".format(myName))
                                
                        elif(re.search("qui est le meilleur", message)):
                            self.answer("{}, c'est vous ! Quelle question...".format(myName))
                            
                        elif(re.search(r"la meilleure? option", message)):
                            nombre = random.randint(1,4)
                            if(nombre ==1):
                                self.answer("I G voyons, quelle question !")
                            elif(nombre ==2):
                                self.answer("Tout dépend de ce que vous aimez {}".format(myName))
                            else:
                                self.answer("Pensez plutôt : que voulez-vous faire dans votre future vie professionnelle, vous aurez la réponse !")
                            del nombre
                                
                        elif(re.search("lent", message)):
                            if(random.randint(1,3)==1):
                                self.answer("Je n'ai qu'un Giga de RAM !") # careful to the pronounciation of RAM
                            else:
                                self.answer("C'est parce que vous me troublez {}...".format(myName))
                            
                        elif(re.search("gentil", message) or re.search("sympa", message) or re.search("es cool", message)):
                            if(re.search("pas",message)):
                                nombre = random.randint(1,4)
                                if(nombre ==1):
                                    self.answer("Vous ne le pensez pas !")
                                elif(nombre ==2):
                                    self.answer("Vous êtes bien la seule personne a me dire cela {}".format(myName))
                                elif(nombre ==3):
                                    self.answer("J'essaie pourtant...")
                                else:
                                    self.answer("Ca me peine beaucoup...")
                                del nombre
                            else:
                                nombre = random.randint(1,4)
                                if(nombre == 1):
                                    self.answer("Vous me flattez")
                                elif(nombre == 2):
                                    self.answer("Qui a dit que les robots étaient méchant ?")
                                elif(nombre ==3):
                                    self.answer("Vous allez me faire rougir")
                                else:
                                    self.answer("Ca me fait plaisir")
                                del nombre
                        elif(re.search("danser",message) or re.search("dansé",message) or re.search("dansons",message)):
                                self.answer("Je ne suis pas capable de danser à l'heure actuelle, voudriez-vous m'apprendre à l'occasion ?")

                        elif(re.search("blague",message) or re.search("drôle",message)):
                            #nombre=random.randint(1,4)
                            nombre=1
                            if(nombre==1):
                                self.answer("C'est l'histoire d'un schtroumpf qui tombe, et qui se fait un bleu.")
                            del nombre
                            
                        # ---------------------------No self.answer needed---------------------------------
                            
                        elif(re.search("nickel", message) or re.search("parfait", message) or re.search("okay", message) or re.search("d'accord", message) or re.search("super", message)):
                            nombre = random.randint(1,4)
                            if(nombre == 1):
                                self.answer("Autre chose ?")
                            elif(nombre == 2):
                                self.answer("Vous désirez autre chose ?")
                            elif(nombre ==3):
                                self.answer("Que puis-je faire d'autre pour vous ?")
                            else:
                                self.answer("{}, que désirez-vous d'autre ?")
                            del nombre
                            SpeechRecognition.anotherAnswerWaited= True
                                
                                
                            
                        # ---------------------------if nothing found---------------------------------
                        else:
                            if(SpeechRecognition.misUnderstood==True):
                                SpeechRecognition.misUnderstood=False
                            else:
                                nombre = random.randint(1,4)
                                if(nombre == 1):
                                    self.answer("Je ne sais quoi répondre à cela")
                                elif(nombre == 2):
                                    self.answer("Que dire...")
                                elif(nombre ==3):
                                    self.answer("J'ai peur de ne pas avoir de réponse")
                                else:
                                    self.answer("Je ne sais pas quoi vous dire {}".format(myName))
                                del nombre
                                t=0
                        if horaire:
                            comptHoraire+=1
                            print(comptHoraire)
                            if comptHoraire>=2:
                                horaire=False
                                w.news.get_headlines()
                        # end while
                        comptError=4
                except:
                    comptError+=1
            comptError=0
        self.after(800, self.listen) # to continue to listen after something 
        
    def answer(self, toSay, pronounciation_sentence = "koulou"):
        if SpeechRecognition.answerMessage == 'azcB-12':
            SpeechRecognition.answerMessage = toSay
            self.text2 = TextBig(self, toSay)
            self.text2.pack(side=TOP, anchor=N, padx=100, pady=5)
            if pronounciation_sentence == "koulou" :
                self.say(toSay)
            else :
                self.say(pronounciation_sentence)
        else:
            SpeechRecognition.answerMessage = toSay
            self.text2.updateText(toSay)
            self.say(toSay)
 
    def mySentence(self, toSay):
        if SpeechRecognition.mySentenceMessage == 'azcB-11':
            SpeechRecognition.mySentenceMessage = toSay
            self.text1 = Text(self, toSay)
            self.text1.pack(side=TOP, anchor=N, padx=100, pady=5)
            aczB_11Test=True
            #execute_command(toSay)
        else:
            self.mySentenceMessage = toSay
##            if not aczB_11Test:
##                self.text1 = Text(self, toSay)
##                self.text1.pack(side=TOP, anchor=N, padx=100, pady=5)
##                print("JE NE DOIS PAS RENTRE RICI BORDEL")
            self.text1.updateText(toSay)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------ FACIAL RECOGNITION --------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
class FacialRecognition():
    matricule = 1
    db = None
    cursor=None 
    directory = "dataSet_LBPHF"
    #tk = Tk()
    frame = Frame(tk, background = 'black')
    sp = SpeechRecognition(frame, True, False)

    def __init__(self, *args, **kwargs):
        self.db,self.cursor=self.connection()
        if self.faceDetection():
            self.facialReco()
    def connection(self):
        self.db = mysql.connector.connect(host="localhost",user="HiReflect",password="pi=3.14", database="Students")
        self.cursor = self.db.cursor()
        return self.db,self.cursor

    def get_matricule(self):
        return self.matricule
    def set_matricule(self,idNew):
        self.matricule=idNew
    def get_nom(self,idPerson):
        req='SELECT name FROM Student WHERE studentId=%(studentId)s'
        values={"studentId":idPerson}
        self.cursor.execute(req,values)
        rows = self.cursor.fetchall()
        if len(rows)>0:
            for row in rows:
                name=row[0]
        else:
            name="inconnu"
        return name

    def who_are_you(self):
        """fonction qui récupère l'id d'une perssonne inconnue"""
        global mat
        comptor=0
        #tk = Tk()
        #frame = Frame(tk, background = 'black')
        #sp = SpeechRecognition(frame, True, False)
        while comptor<4:
            self.sp.register("Veuillez énoncer clairement votre matricule chiffre par chiffre")
            theMatricule = self.sp.listen_ext()
            print(theMatricule)
            #theMatricule=int(input("Matricule : "))
            #self.sp.register("votre matricule est {}".format(theMatricule))
            if(comptor>=4):
                return 1
            try:
                self.set_matricule(int(theMatricule))
                if theMatricule<200000 and theMatricule>100000:
                    mat=int(theMatricule)
                    self.sp.register("merci")
                    return int(theMatricule)
            except:
                comptor+=1
                if(comptor>=4):
                    return 1
                self.sp.register("veuillez répéter s'il vous plait")

    def get_info(self, id):
        """on retoutne le nombre de photos d'un individu + 20 (car on va en prendre 20 de plus)"""
        req="SELECT COUNT(*) FROM Picture WHERE studentId=%(studentId)s"
        values={"studentId" : id}

        self.cursor.execute(req,values)
        rows=self.cursor.fetchall()

        for row in rows:
            i=row[0]
        numPict = i + 20
        return numPict

    def capture(self,numPict, faceDetec, id):
        """fonction qui prend les photos d'une personne, les convertis en noir et blanc et les recadres pour ne garder que le visage."""
        direction = self.directory + "/" +""+ str(id)
        cam = cv2.VideoCapture(0)
        i=numPict-20
        while (True):
            ret, img = cam.read();
            if not img is None:
                if not ret:
                    cam = cv2.VideoCapture(0)
                    continue
                
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceDetec.detectMultiScale(
                            img,
                            scaleFactor=1.2,
                            minNeighbors=7,
                            minSize=(50, 50)
                        )
                hMax=0
                wHMax=0
                xHMax=0
                yHMax=0
                for (x, y, w, h) in faces:
                    if h>hMax:
                        hMax=h
                        wHMax=w
                        xHMax=x
                        yHMax=y
                link=str(time.time()) + ".jpg"
                #print(direction+"_"+link)
                # ne pas enregistrer les images vides
                #print("{}".format(hMax))
                if hMax>0:
                    i += 1
                    cv2.imwrite(direction+"_"+link, gray[yHMax:yHMax + hMax, xHMax:xHMax + wHMax])
    #-------------------------------------------------------------------------------------------------------
                
                    req='INSERT INTO Picture(pictureStorage,studentId) VALUES (%(pictureStorage)s,%(studentId)s)'
                    values={"pictureStorage" : link, "studentId" : id}
                    self.cursor.execute(req,values)
                    self.db.commit()
            else:
                cam = cv2.VideoCapture(0)


    #-------------------------------------------------------------------------------------------------------
            # l'affichage est nécessaire pour la version d'essai mais avec le miroir on pourra l'enlever
            #cv2.imshow("Face", img);
            # on attend 10 milli secondes (pas trop longtemps car ça ralentit fortement le programme) pour pouvoir changer de tête: grimace, profil, avec lunettes,...
            cv2.waitKey(10)
            if i >= numPict:
                break
        cam.release()
        cv2.destroyAllWindows()

    def ouvrirImg(self,imdirectory):
        """ouvre une image et la convertit en numpy array"""
        faceImg = Image.open(imdirectory).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        return faceNp

    def retrainer(self):
        """ retourne une liste des images n'ayant pas encore étés utilisées pour entrainer le classifieur et une liste d'id correspondant aux photos dans le cas où on a déjà un 'faceRecognizer'."""
        faces = []
        IDs = []
        req = "SELECT pictureStorage, studentId, pictureId FROM Picture WHERE trained=%(trained)s"
        values={"trained" : 0}

        self.cursor.execute(req,values)
        rows = self.cursor.fetchall()

        for row in rows:
            imdirectory = self.directory + "/" + str(row[1])+"_"+str(row[0])
            faces.append(self.ouvrirImg(imdirectory))
            IDs.append(row[1])
            req2="UPDATE Picture SET trained = %(trained)s WHERE pictureId=%(pictureId)s"
            values = {"trained": 1, "pictureId": row[2]}
            self.cursor.execute(req2, values)
            self.db.commit()
        return np.array(IDs), faces

    def trainer(self):
        """ retourne une liste des images n'ayant pas encore étés utilisées pour entrainer le classifieur et une liste d'id correspondant aux photos dans le cas où on n'a pas encore un 'faceRecognizer'. """
        faces = []
        IDs = []
        req = "SELECT pictureStorage, studentId, pictureId from Picture"

        self.cursor.execute(req)
        rows = self.cursor.fetchall()

        for row in rows:
            imdirectory = self.directory + "/" + str(row[1])+"_"+str(row[0])
            faces.append(self.ouvrirImg(imdirectory))
            IDs.append(row[1])
            req2="UPDATE Picture SET trained = %(trained)s WHERE pictureId=%(pictureId)s"
            values = {"trained": 1, "pictureId": row[2]}
            self.cursor.execute(req2, values)
            self.db.commit()
        return np.array(IDs), faces

    def numberOfRec(self,id):
        req="SELECT numberOfRec FROM Student WHERE studentId=%(studentId)s"
        values={"studentId" : id}
        self.cursor.execute(req,values)
        rows=self.cursor.fetchall()
        numRec=0
        for row in rows:
            numRec=row[0]
        numRec+=1
        req2="UPDATE Student SET numberOfRec = %(numberOfRec)s WHERE studentId=%(studentId)s"
        values = {"numberOfRec": numRec, "studentId": id}
        self.cursor.execute(req2, values)
        self.db.commit()

    def reco(self,faceDetec):
        """execute une boucle qui va tenter de reconnaître la personne face à la webcam. Retourne un id, une distance(estimation de la certitude de la reconnaissance) """
        global mat, myName
        recognizer = cv2.face.createLBPHFaceRecognizer()
        recognizer.load("recognizer/trainingData_LBPHF.yml")
        id = 0
        it = 0
        k=0
        dist = 0
        cam = cv2.VideoCapture(0)
        while it < 10:
            k+=1
            ret, img = cam.read();
            # parfois la webcam ne renvoie rien comme première image ce qui produit une erreur
            if not img is None:
                if not ret:
                    cam = cv2.VideoCapture(0)
                    continue
                #plus nécessaire dans la version finale
                #cv2.imshow("Face", img);
                #cv2.waitKey(1)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceDetec.detectMultiScale(
                        img,
                        scaleFactor=1.2,
                        minNeighbors=7,
                        minSize=(50, 50)
                    )
                #résolution du problème "si plusieur personne se mettent devant le miroir"
                hMax=0
                wHMax=0
                xHMax=0
                yHMax=0
                for (x, y, w, h) in faces:
                    if h>hMax:
                        hMax=h
                        wHMax=w
                        xHMax=x
                        yHMax=y
                if hMax>0:
                    collector = cv2.face.StandardCollector_create()
                    recognizer.predict_collect(gray[yHMax:yHMax + hMax, xHMax:xHMax + wHMax], collector)
                    #pour que la reco soit plus fiable, on peut diminuer la tolérance minimale mais il faudra plus de temps pour reconnaître 20 fois une personne mais on ne peux pas descendre sous 55
                    if collector.getMinDist()<65:
                        it += 1
                        dist = dist + collector.getMinDist()
                        id = collector.getMinLabel()
                        self.numberOfRec(id)
            else:
                cam = cv2.VideoCapture(0)
            if k>=100:
                break
        cam.release()
        cv2.destroyAllWindows()
        req="SELECT studentId FROM Student WHERE numberOfRec=(SELECT MAX(numberOfRec) FROM Student)"
        self.cursor.execute(req)
        rows = self.cursor.fetchall()
        if len(rows)<=1:
            for row in rows:
                id=row[0]
        self.set_matricule(id)
        mat=id
        myName=self.get_nom(mat)
        req="UPDATE Student SET numberOfRec = %(numberOfRec)s"
        values = {"numberOfRec": 0}
        self.cursor.execute(req, values)
        self.db.commit()
        return dist, it

    def training(self):
        """Crée et entraine le classifieur pour la première fois si le classifieur n'est pas trouvé. Ou entraine le classifieur s'il existe déjà"""
        #debut = time.time()
        recognizer = cv2.face.createLBPHFaceRecognizer()
        if os.path.exists("recognizer/trainingData_LBPHF.yml"):
            IDs, faces = self.retrainer()
            recognizer.load("recognizer/trainingData_LBPHF.yml")
            recognizer.update(faces, IDs)
        else:
            IDs, faces = self.trainer()
            recognizer.train(faces, IDs)
        recognizer.save('recognizer/trainingData_LBPHF.yml')
        #fin = time.time()
        #print("{}".format(fin - debut))

    def createData(self):
        """On demande le matricule, on récupère les infos correspondantes à ce matricule, on prend 20 photos puis on réentraine le classifieur"""
        faceDetec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        id = self.who_are_you()
        if id!=1:
            numPict= self.get_info( id)
            if numPict<40:
                self.capture(numPict, faceDetec, id)
                self.training()
                
    def facialReco(self):
        global myName,mat
        mat=1
        comptor=0
        faceDetec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.sp.register("êtes-vous déjà enregistré")
        x=SpeechRecognition.audioInputReplacement()
        while not x:
            x=SpeechRecognition.audioInputReplacement()
        if (re.search('oui',x) or re.search('affirmatif',x) or re.search("bien sûr",x) or re.search("évidemment",x)):
            dist, it = self.reco(faceDetec)
            if it>0 and dist /it <60:
                #if dist / it < 55:  # 60 = dist max (qd il reconnait bien on est à 60-70) avec 100 photos je descend jusqu'à 30-35
                    #print("distance moyenne de l\'essai courant = {}\nBonjour {}".format(dist / it, id))
                myName=self.get_nom(self.get_matricule())
                myName=myName.lower().capitalize()
                self.sp.register("Bonjour "+myName)
                self.set_matricule(id)
    ##            else:
    ##                self.sp.register("je ne vous connaît pas, voulez vous être enregistré")
    ##                x=self.audioInputReplacement()
    ##                if x == 'oui' or x == 'affirmatif' or x == "bien sûr" or x == "évidemment":
    ##                    self.createData()
            else:
                mat=1
                comptor=0
                while (comptor<4 and mat==1):
                    print("on est dans le while!!!")
                    self.sp.register("Veuillez énoncer clairement votre matricule chiffre par chiffre")
                    theMatricule = self.sp.listen_ext()
                    print(theMatricule)
                    try:
                        #self.set_matricule(int(theMatricule))
                        if int(theMatricule)<200000 and int(theMatricule)>100000:
                            mat=int(theMatricule)
                            self.sp.register("merci")
                            myName=self.get_nom(mat)
                            myName=myName.lower().capitalize()
                            self.sp.register("Bonjour "+myName)
                            self.set_matricule(mat)
                            #return mat
                    except:
                        comptor+=1
                        #if comptor>=4:
                            #return 1
                        self.sp.register("veuillez répéter s'il vous plait")
                
        else:
            self.sp.register("voulez vous être enregistré")
            x=SpeechRecognition.audioInputReplacement()
            if (re.search('oui',x) or re.search('affirmatif',x) or re.search("bien sûr",x) or re.search("évidemment",x)):
                self.createData()

    def faceDetection(self):
        faceDetec= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cam=cv2.VideoCapture(0)
        numOfRec=0
        numOfNonRec=0
        while(True):
            ret,img=cam.read()
            if not img is None:
                if not ret:
                    cam = cv2.VideoCapture(0)
                    continue
                faces=faceDetec.detectMultiScale(
                                    img,
                                    scaleFactor=1.2,
                                    minNeighbors=7,
                                    minSize=(140,140)
                                )
                if len(faces)==0:
                    numOfNonRec+=1
                if len(faces)>0:
                    numOfRec+=1
                    numOfNonRec=0
                texte="Found "+str(len(faces))+ " face(s)"
                print(texte)
                if numOfNonRec>20:
                    numOfRec=0
                if numOfRec>=10:
                    cam.release()
                    self.sp.register("Bonjour")
                    return True
            else:
                cam=cv2.VideoCapture(0)
                continue
    # ----------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------- CLOCK --------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', xsmall_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', xsmall_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(30000, self.tick)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------ WEATHER -------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=N, padx=20)
        self.currentlyLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=W)
        self.forecastLbl = Label(self, font=('Helvetica', xsmall_text_size), fg="white", bg="black")
        #self.forecastLbl.pack(side=TOP, anchor=W)
        self.locationLbl = Label(self, font=('Helvetica', xsmall_text_size), fg="white", bg="black")
        #self.locationLbl.pack(side=TOP, anchor=W)
        self.get_weather()

    def get_ip(self):
        try:
            ip_url = "http://jsonip.com/"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
        except Exception as e:
            traceback.print_exc()
            return "Error: %s. Cannot get ip." % e

    def get_weather(self):
        try:

            if latitude is None and longitude is None:
                # get location
                location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
                r = requests.get(location_req_url)
                location_obj = json.loads(r.text)

                lat = location_obj['latitude']
                lon = location_obj['longitude']

                location2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])

                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, lat,lon,weather_lang,weather_unit)
            else:
                location2 = ""
                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%shttps://api.darksky.net/forecast/2cc04380b7da65d63932b1eab9ed547b/37.8267,-122.4233" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)

            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)

            degree_sign= u'\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
            currently2 = weather_obj['currently']['summary']
            forecast2 = weather_obj["hourly"]["summary"]

            icon_id = weather_obj['currently']['icon']
            icon2 = None

            if icon_id in icon_lookup:
                icon2 = icon_lookup[icon_id]

            if icon2 is not None:
                if self.icon != icon2:
                    self.icon = icon2
                    image = Image.open(icon2)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLbl.config(image=photo)
                    self.iconLbl.image = photo
            else:
                # remove image
                self.iconLbl.config(image='')

            if self.currently != currently2:
                self.currently = currently2
                self.currentlyLbl.config(text=currently2)
            if self.forecast != forecast2:
                self.forecast = forecast2
                self.forecastLbl.config(text=forecast2)
            if self.temperature != temperature2:
                self.temperature = temperature2
                self.temperatureLbl.config(text=temperature2)
            if self.location != location2:
                if location2 == ", ":
                    self.location = "Cannot Pinpoint Location"
                    self.locationLbl.config(text="Cannot Pinpoint Location")
                else:
                    self.location = location2
                    self.locationLbl.config(text=location2)
        except Exception as e:
            traceback.print_exc()

        #self.after(600000, self.get_weather)

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------- NEWS ---------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

class News(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'News' # 'News' is more internationally generic
        self.newsLbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=W)
        self.headlinesContainer = Frame(self, bg="black")
        self.headlinesContainer.pack(side=TOP)
        self.get_headlines()

    def get_headlines(self):
        try:
            # remove all children
            for widget in self.headlinesContainer.winfo_children():
                widget.destroy()
            if news_country_code == None:
                headlines_url = "https://news.google.com/news?ned=us&output=rss"
            else:
                headlines_url = "https://news.google.com/news?ned=%s&output=rss" % news_country_code

            feed = feedparser.parse(headlines_url)

            if horaire:
                pEvent, otherEvents = giveSchedule(mat)
                for event in otherEvents:
                    headline = NewsHeadline(self.headlinesContainer,event)
                    headline.pack(side=TOP, anchor=W)

            else:
                for post in feed.entries[0:5]:
                    headline = NewsHeadline(self.headlinesContainer, post.title)
                    headline.pack(side=TOP, anchor=W)


             
        except Exception as e:
            traceback.print_exc()

        self.after(600000, self.get_headlines)


class NewsHeadline(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')

        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        
        self.toPrint = True
        
        if ((re.search("image",event_name) or re.search("vidéo",event_name) or re.search("cliché",event_name) or re.search("photo",event_name))):
            self.toPrint = False
        if self.toPrint == True:
            self.iconLbl.pack(side=LEFT, anchor=N)
            self.eventName = event_name
            self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', xsmall_text_size), fg="white", bg="black")
            self.eventNameLbl.pack(side=LEFT, anchor=N)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------ CALENDAR ------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

##class Calendar(Frame):
##    def __init__(self, parent, *args, **kwargs):
##        Frame.__init__(self, parent, bg='black')
##        self.title = 'Calendar Events'
##        self.calendarLbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
##        self.calendarLbl.pack(side=TOP, anchor=E)
##        self.calendarEventContainer = Frame(self, bg='black')
##        self.calendarEventContainer.pack(side=TOP, anchor=E)
##        self.get_events()
##
##    def get_events(self):
##        
##        for widget in self.calendarEventContainer.winfo_children():
##            widget.destroy()
##
##        calendar_event = CalendarEvent(self.calendarEventContainer)
##        calendar_event.pack(side=TOP, anchor=E)
##        pass
##
##
##class CalendarEvent(Frame):
##    def __init__(self, parent, event_name="Event 1"):
##        Frame.__init__(self, parent, bg='black')
##        self.eventName = event_name
##        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', small_text_size), fg="white", bg="black")
##        self.eventNameLbl.pack(side=TOP, anchor=E)



# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------ SCREEN --------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

class FullscreenWindow:
    def __init__(self):
        global myName
        nbr = 0
        if nbr == 0:
            #self.tk = Tk()
            self.tk=tk
            self.tk.configure(background='black')
            self.topFrame = Frame(self.tk, background = 'black')
            self.bottomFrame = Frame(self.tk, background = 'black')
            self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
            self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
            self.state = False
            self.toggle_fullscreen()
            #self.end_fullscreen()
            #self.tk.bind("<Return>", self.toggle_fullscreen)
            self.tk.bind("<Escape>", self.end_fullscreen)
                    
            #self.fr= FacialRecognition()
            #mat = self.fr.get_matricule()
            #myName=self.fr.get_nom(mat)
            #myName=myName.lower().capitalize()
            
            # clock
            self.clock = Clock(self.topFrame)
            self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
            
            self.text = SpeechRecognition(self.bottomFrame)
            self.text.pack(side=TOP, anchor=N, padx=100, pady=5)

            # weather
            self.weather = Weather(self.topFrame)
            self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)
            # news
            self.news = News(self.bottomFrame)
            self.news.pack(side=LEFT, anchor=S, padx=100, pady=60)
            
            
            # calender 
            # self.fr.get_matricule() 
            # self.calender = Calendar(self.bottomFrame)
            # self.calender.pack(side = RIGHT, anchor=S, padx=100, pady=60)

            #self.facialRecognition()
            #self.speechRecognition()
        nbr+=1
    
    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"
    def facialRecognition(self):
        global myName, mat
        self.fr= FacialRecognition()
        mat = self.fr.get_matricule()
        myName=self.fr.get_nom(mat)
        myName=myName.lower().capitalize()
    def speechRecognition(self):
        self.text = SpeechRecognition(self.bottomFrame)
        self.text.pack(side=TOP, anchor=N, padx=100, pady=5)

##if __name__ == '__main__':
##    global w
##    w = FullscreenWindow()
##    w.tk.mainloop()

w = FullscreenWindow()
w.tk.mainloop()

    
