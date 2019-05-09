"---------------------------------------------------------------------------------------------------------------"
"---------------------------------------------------------------------------------------------------------------"
"-------------------------------- Interface Miroir Intelligent 2018-2019 ---------------------------------------"
"---------------------------------------------------------------------------------------------------------------"
"---------------------------------------------------------------------------------------------------------------"

" Colaborateurs:  @GUY_ROLAND_KUE  @PATRICK_DJAKOU @ROSABELLE_LEKEMO  "

" Ce projet à été developpé dans le cadre du projet informatique de BA3 IG de l'école polytechnique de l'Umons "


from tkinter import *
from PIL import Image, ImageTk
import locale
import speech_recognition as sr
import re
import cv2
import time
import threading
from contextlib import contextmanager
import traceback
import requests
import json
import os
import feedparser
from threading import Thread
import speak



LOCALE_LOCK = threading.Lock()

ui_locale = ''  # e.g. 'fr_FR' for French, '' as default
time_format = 24  # 12 or 24
date_format = "%d %b %Y"  # check python doc for strftime() for options
news_country_code = 'fr_be'
weather_api_token = 'a748079ee05ff724dc7b60cd11e0e0dd'  # create account at https://darksky.net/dev/
weather_lang = 'fr'  # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'auto'  # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
latitude = '50.4541'  # Set this if IP location lookup does not work for you (must be a string)
longitude = '3.9523'  # Set this if IP location lookup does not work for you (must be a string)
xlarge_text_size = 94
large_text_size = 50
medium_text_size = 30
small_text_size = 20
xsmall_text_size = 15
tiny_text_size = 13
counterMax=10
lang ="fr-FR"
font_menu = ("Arial", 25)

tl = 2  # for little sentences
tL = 5  # for long sentences
t = tl  # default configuration

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# -------------------------------- WEATHER -----------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# classe qui permet d'afficher la météo dans une fenetre de type Frame

class Weather(Frame):

    def __init__(self, parent, *args, **kwargs):

        # maps open weather icons to
        # icon reading is not impacted by the 'lang' parameter
        # dictionnaire des chemins d'acces d'icon de météo
        self.icon_lookup = {
            'clear-day': "assets/Sun.png",  # clear sky day
            'wind': "assets/Wind.png",  # wind
            'cloudy': "assets/Cloud.png",  # cloudy day
            'partly-cloudy-day': "assets/PartlySunny.png",  # partly cloudy day
            'rain': "assets/Rain.png",  # rain day
            'snow': "assets/Snow.png",  # snow day
            'snow-thin': "assets/Snow.png",  # sleet day
            'fog': "assets/Haze.png",  # fog day
            'clear-night': "assets/Moon.png",  # clear sky night
            'partly-cloudy-night': "assets/PartlyMoon.png",  # scattered clouds night
            'thunderstorm': "assets/Storm.png",  # thunderstorm
            'tornado': "assests/Tornado.png",  # tornado
            'hail': "assests/Hail.png"  # hail
        }
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''

        # on initialise la frame d'affichage des données météos
        Frame.__init__(self, parent, bg='black')
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=N, padx=10)
        self.currentlyLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=W)
        self.forecastLbl = Label(self, font=('Helvetica', xsmall_text_size), fg="white", bg="black")
        # self.forecastLbl.pack(side=TOP, anchor=W)
        self.locationLbl = Label(self, font=('Helvetica', xsmall_text_size), fg="white", bg="black")
        # self.locationLbl.pack(side=TOP, anchor=W)
        self.get_weather()


    # permet de récuperer un json en ligne et extraire l'ip pour récuperer les données méteos
    def get_ip(self):
        try:
            ip_url = "http://jsonip.com/"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
        except Exception as e:
            traceback.print_exc()
            return "Error: %s. Cannot get ip." % e

    #récupère les données météos de l'API sous forme de fichier json et les formate pour l'affichage
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
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (
                weather_api_token, lat, lon, weather_lang, weather_unit)
            else:
                location2 = ""
                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (
                weather_api_token, latitude, longitude, weather_lang, weather_unit)

            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)

            degree_sign = u'\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
            currently2 = weather_obj['currently']['summary']
            forecast2 = weather_obj["hourly"]["summary"]

            icon_id = weather_obj['currently']['icon']
            icon2 = None

            if icon_id in self.icon_lookup:
                icon2 = self.icon_lookup[icon_id]

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

        # self.after(600000, self.get_weather)

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# -------------------------------- TEXT --------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# classe permettant d'afficher des textes dans une frame en petit carractère
class Text(Frame):
    def __init__(self, parent, text, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.contentText = text
        self.contentTextLbl = Label(self, text=self.contentText, font=('Helvetica', tiny_text_size), fg="white",
                                    bg="black")
        self.contentTextLbl.pack(side=LEFT, anchor=N)

    # modifie le texte affiché
    def updateText(self, newText):
        self.contentTextLbl.config(text=newText)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# -------------------------------- TEXT BIG ----------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# classe permettant d'afficher des textes dans une frame en grand carractère

class TextBig(Frame):
    def __init__(self, parent, text, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.contentText = text
        self.contentTextLbl = Label(self, text=self.contentText, font=('Helvetica', xsmall_text_size), fg="white",
                                    bg="black")
        self.contentTextLbl.pack(side=LEFT, anchor=N)

    # modifie le texte affiché
    def updateText(self, newText):
        self.contentTextLbl.config(text=newText)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# -------------------------------- ClOCK -------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# frame d'affichage de l'heure et de la date
class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', xsmall_text_size), fg="white",
                              bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', xsmall_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    # renvoie la localité
    @contextmanager
    def setlocale(self,name):  # thread proof function to work with locale
        with LOCALE_LOCK:
            saved = locale.setlocale(locale.LC_ALL)
            try:
                yield locale.setlocale(locale.LC_ALL, name)
            finally:
                locale.setlocale(locale.LC_ALL, saved)

    # récupere l'heure et la date locale et met à jour l'affichage tous les 3 secondes
    def tick(self):
        with self.setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p')  # hour in 12h format
            else:
                time2 = time.strftime('%H:%M')  # hour in 24h format

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
# ------------------------------- NEWS ---------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# frame d'affichage des news
class News(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'News'  # 'News' is more internationally generic
        self.newsLbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=W)
        self.headlinesContainer = Frame(self, bg="black")
        self.headlinesContainer.pack(side=TOP)
        self.get_headlines()

    # recupère les infos sous forme de json et affiche les grands titres
    # met à jour les infos tous les 600s
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

            for post in feed.entries[0:5]:
                headline = NewsHeadline(self.headlinesContainer, post.title)
                headline.pack(side=TOP, anchor=W, fill=X)

        except Exception as e:
            traceback.print_exc()

        self.after(600000, self.get_headlines)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------- NEWS HEADLINE ------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# classe qui récupere et formate les infos pour l'affichage dans une frame
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

        if ((re.search("image", event_name) or re.search("vidéo", event_name) or re.search("cliché",
                                                                                           event_name) or re.search(
                "photo", event_name))):
            self.toPrint = False
        if self.toPrint == True:
            self.iconLbl.pack(side=LEFT, anchor=N)
            self.eventName = event_name
            self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', tiny_text_size), fg="white",
                                      bg="black")
            self.eventNameLbl.pack(side=LEFT, anchor=N)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------- FULLSCREEN WINDOW --------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# classe qui gere l'affichage de l'interface ainsi que les interations avec l'utiliateur
class FullscreenWindow():
    def __init__(self):
        self.fenetre_principale_tk = Tk()   # initialisation de la frame principale
        self.fenetre_principale_tk.configure(background='black')
        self.state = False   # bouleen pour le toggle du fullscreen
        self.toggle_fullscreen()

        # sortir du fullscreen par le clic sur la touche escape du clavier
        self.fenetre_principale_tk.bind("<Escape>", self.end_fullscreen)

        self.welcome()


    # affichage de la page de bienvenue
    def welcome(self):
        welcome = Welcome(self.fenetre_principale_tk)
        welcome.pack(pady=300)

        # lancement de la détection de visage
        detection = FaceDetect(self.fenetre_principale_tk)
        detection.start()

    # affichage de la page de accueil
    def accueil(self):
        pageAccueil = Accueil(self.fenetre_principale_tk)
        pageAccueil.pack(side=TOP, anchor=N, fill=BOTH, expand=YES)

    # affichage de la page d'acceuil
    def navigation(self):

        nav = Navigation(self.fenetre_principale_tk)
        nav.pack(side=TOP)

    # affichage de la page du PAE
    def pae(self):
        pagePae = Pae(self.fenetre_principale_tk)
        pagePae.pack(side=TOP)

    # affichage de la vue des activitées
    def activite(self):
        pageActivite = Activite(self.fenetre_principale_tk)
        pageActivite.pack(side=TOP)

    # toggle du fullscreen
    def toggle_fullscreen(self):
        self.state = not self.state  # Just toggling the boolean
        self.fenetre_principale_tk.attributes("-fullscreen", self.state)
        return "break"

    # sortir du fullscreen
    def end_fullscreen(self):
        self.state = False
        self.fenetre_principale_tk.attributes("-fullscreen", False)
        return "break"

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------- FACE DETECTION -----------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# class qui fait la détection de visages pour afficher la page d'accueil, elle hérite de la classe Thread pour
# permettre l'enregistrement vidéo en parallèle pendant que l'interface tourne
class FaceDetect(Thread):
    def __init__(self,Frame):
        Thread.__init__(self)
        self.frame = Frame

    # détection de visage pour le lancement de la page l'accueil et la reconnaissance vocale
    def run(self):
        # le fichier haarcascade_frontalface_default.xml doit être dans le dossier où est sauvegardé le code
        faceDetec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # lancement de la caméra "0" correspond en général à la webcam si ça ne marche pas il faut tester d'autres numéros
        cam = cv2.VideoCapture(0)

        i = False
        while (i == False):
            ret, img = cam.read()
            # img est une image en couleur
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # détection de visage
            faces = faceDetec.detectMultiScale(gray, 1.3, 10)

            nombre_face = len(faces)

            if nombre_face > 0:
                i = True
                cam.release()   # stop la camera

        speak.tts("bienvenue", lang)

        accueil = Accueil(self.frame)
        accueil.pack(side=TOP, anchor=N, fill=BOTH, expand=YES)

        speech = SpeechReconignition(self.frame)
        speech.start()

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------- P A E --------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# classe qui crée la page les information du pae
class Pae(Frame):
    def __init__(self, parent):

        # executé avant le init de la frame car l'objet self.menuFrame vide la fenetre placée en paramètre (parent)
        # avant d'afficher le menu
        self.menuFrame = Menu(parent)
        self.menuFrame.pack(side=BOTTOM)

        Frame.__init__(self, parent, bg="black")


        cheminImage = "plans/pae.png"
        img2 = Image.open(cheminImage)
        img2 = img2.resize((1000, 600), Image.ANTIALIAS)
        photo2 = ImageTk.PhotoImage(img2)
        affiche = Label(self, image=photo2)
        affiche.image = photo2
        affiche.pack(pady=30)
        speak.tts("P A E", lang)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------- ACTIVITE -----------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# classe qui crée la vue des les activités
class Activite(Frame):
    def __init__(self, parent):

        # executé avant le init de la frame car l'objet self.menuFrame vide la fenetre placée en paramètre (parent)
        # avant d'afficher le menu
        self.menuFrame = Menu(parent)
        self.menuFrame.pack(side=BOTTOM)

        Frame.__init__(self, parent, bg="black")


        topFrame = Frame(self, bg='black')
        topFrame.pack(side=TOP, anchor=N, fill=BOTH, expand=YES)

        cheminImage = "plans/activites2.png"
        img2 = Image.open(cheminImage)
        img2 = img2.resize((1000, 600), Image.ANTIALIAS)
        photo2 = ImageTk.PhotoImage(img2)
        affiche = Label(topFrame, image=photo2)
        affiche.image = photo2
        affiche.pack(pady=30)
        speak.tts("Activité", lang)





# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------- ACCUEIL ------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# classe qui crée la vue de l'accueil
class Accueil(Frame):
    def __init__(self, parent):

        # executé avant le init de la frame car l'objet self.menuFrame vide la fenetre placée en paramètre (parent)
        # avant d'afficher le menu
        self.menuFrame = Menu(parent)
        self.menuFrame.pack(side=BOTTOM)

        # initialisation de la frame
        Frame.__init__(self, parent, bg="black")
        self.parent = parent

        # clock
        self.clock = Clock(self)
        self.clock.pack(side=RIGHT, anchor=N, padx=50, pady=30)

        # weather
        self.weather = Weather(self)
        self.weather.pack(side=LEFT, anchor=N, padx=50, pady=30)

        # news
        self.news = News(self)
        self.news.pack(side=BOTTOM, fill=BOTH, anchor=S, padx=50, pady=30)

        speak.tts("Accueil", lang)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------- MENU ---------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# class qui crée le menu
class Menu(Frame):
    def __init__(self, parent):

        # vide la fenetre parent placée en paramètre
        for frame in parent.winfo_children():
            frame.destroy()

        Frame.__init__(self, parent, bg="black")
        self.parent = parent
        buttonNavigation = Button(self, text="Navigation", font=font_menu, command=self.navigation)
        buttonNavigation.grid(row=0, column=1, sticky="nsew", pady=30)
        buttonAcceuil = Button(self, text="Accueil", font=font_menu, command=self.accueil)
        buttonAcceuil.grid(row=0, column=0, sticky="nsew", pady=30)
        activite = Button(self, text="Activite", font=font_menu, command=self.activite)
        activite.grid(row=0, column=2, sticky="nsew", pady=30)
        buttonPae = Button(self, text="Pae", font=font_menu, command=self.pae)
        buttonPae.grid(row=0, column=3, sticky="nsew", pady=30)

    #affichage de la vue de navigation
    def navigation(self):
        nav = Navigation(self.parent)
        nav.pack(side=TOP)

    # affichage de la vue de accueil
    def accueil(self):
        pageNavigation = Accueil(self.parent)
        pageNavigation.pack(side=TOP, anchor=N, fill=BOTH, expand=YES)

    # affichage de la vue de activite
    def activite(self):
        pageActivite = Activite(self.parent)
        pageActivite.pack(side=TOP)

    # affichage de la vue de pae
    def pae(self):
        pagePae = Pae(self.parent)
        pagePae.pack(side=TOP)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------- NAVIGATION ---------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# class qui gere l'affichage des plans
class Navigation(Frame):
    def __init__(self, parent):

        # executé avant le init de la frame car l'objet self.menuFrame vide la fenetre placée en paramètre (parent)
        # avant d'afficher le menu
        self.menuFrame = Menu(parent)
        self.menuFrame.pack(side=BOTTOM)

        Frame.__init__(self, parent, bg="black")



        self.topFrame = Frame(self, background='black')
        self.topFrame.pack(side=TOP)
        self.inputRecherche = Entry(self.topFrame, bd=1)
        self.inputRecherche.grid(row=0, column=0, sticky=E)
        self.recherche = Button(self.topFrame, text="Recherche", font=font_menu, command=self.recherche)
        self.recherche.grid(row=0, column=1, sticky=W)

        self.dictionnaireDesPlans = {'auditoire 05': "plans/aud05.png",
                                     'auditoire 11': "plans/aud11.1.PNG",
                                     'auditoire 25': "plans/aud25.1.PNG",
                                     'auditoire 23': "plans/aud23.1.PNG",
                                     'auditoire 12': "plans/aud12.1.PNG"}

        cheminImage = "plans/aud12.0.PNG"
        img2 = Image.open(cheminImage)
        img2 = img2.resize((800, 600), Image.ANTIALIAS)
        photo2 = ImageTk.PhotoImage(img2)
        affiche = Label(self.topFrame, image=photo2)
        affiche.image = photo2
        affiche.grid(row=1, columnspan=2, pady=30)
        speak.tts("Navigation", lang)

    # on recupère les informations du champ imput de recherche (inputRecherche) et on recherche le local dans
    # dictionnaireDesPlans puis on affiche
    def recherche(self):
        local = self.inputRecherche.get()
        self.recherche_vocale(local)

    # on recherche auditoire dans dictionnaireDesPlans
    # puis on affiche
    def recherche_vocale(self, auditoire):
        local = auditoire
        plans = self.dictionnaireDesPlans

        if local in plans:
            cheminImage = plans[local]
            img2 = Image.open(cheminImage)
            img2 = img2.resize((800, 600), Image.ANTIALIAS)
            photo2 = ImageTk.PhotoImage(img2)
            affiche = Label(self.topFrame, image=photo2)
            affiche.image = photo2
            affiche.grid(row=1, columnspan=2, pady=30)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------- WELCOME ------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# classe qui crée la page Bienvenue
class Welcome(Frame):
    def __init__(self, parent):
        self.menuFrame = Menu(parent)

        Frame.__init__(self, parent, bg="black")

        topFrame = Frame(self, background='black')
        topFrame.pack(side=TOP, anchor=N, fill=BOTH, expand=YES)

        message="BIENVENUE A POLYTECH UMONS"

        messageLabel = Label(topFrame, text=message, font=('Helvetica', large_text_size),  fg="white",
                              bg="black")
        messageLabel.pack()

        speak.tts("Bienvenu au miroir intelligent de l'école polytechnique de l'université de  Mons", lang)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ------------------------------- SPEECH RECONGNITION ------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# classe qui gère la navigation vocale dans l'interface, elle hérite de la classe thread pour permettre l'enregistrement
# vocale en parallèle pendant que l'interface tourne
class SpeechReconignition(Thread):
    def __init__(self, Frame):
        Thread.__init__(self)
        self.frame = Frame
        self.discuss = True

        self.navigator = ""

        tl = 2  # for little sentences
        tL = 5  # for long sentences
        t = tl  # default configuration
        self.r = sr.Recognizer()

    # answer function
    def answer(self, toSay, t_stop=tl):
        # print and say the 'toSay' variable and can modify time pause
        print(toSay)
        # execute_command(toSay)
        global t
        t = t_stop

    #  utilisé pour arreter le thread et afficher la page de bienvenu
    def welcome(self):

        self.discuss = False

        welcome = Welcome(self.frame)
        welcome.pack(pady=300)

        detection = FaceDetect(self.frame)
        detection.start()

    # lance le micro et gère les commandes vocales pour naviguer dans l'interface
    def run(self):

        with sr.Microphone(sample_rate=32000) as source:

            while (self.discuss == True):
                try:
                    # obtain audio from the microphone
                    print("...")  # to show he wait something from you
                    audio = self.r.listen(source, 4, 6)  # slowwwww
                    print("..")  # to show he has recorded your demande
                    message = self.r.recognize_google(audio, language="fr-FR")
                    # print("Vous : " + message )
                    del audio

                except sr.WaitTimeoutError as ve:
                    message = ""
                    print(ve)

                except sr.UnknownValueError:
                    self.answer("Je n'ai pas compris, pouvez-vous répéter ?", 3.5)
                    message = ""
                    # misUnderstood = True
                except sr.RequestError as e:
                    print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
                    message = ""
                    # search if the answer exists
                if re.search("auditoire 24 merci", message) or re.search("24 merci", message):
                    self.answer("ok 24")
                    self.navigator = "auditoire 24"
                    print(self.navigator)
                    nav = Navigation(self.frame)
                    nav.recherche_vocale(self.navigator)
                    nav.pack(side=TOP)


                elif re.search("auditoire 11 merci", message) or re.search("11 merci", message):
                    self.answer("ok 11")
                    self.navigator = "auditoire 11"
                    print(self.navigator)
                    nav = Navigation(self.frame)
                    nav.recherche_vocale(self.navigator)
                    nav.pack(side=TOP)
                    direction = "prenez à votre droite ensuite montez jusqu'au premier étage, l'auditoire est " \
                                "sur votre gauche"
                    speak.tts(direction, lang)

                elif re.search("auditoire 12 merci", message) or re.search("12 merci", message):
                    self.answer("ok 12")
                    self.navigator = "auditoire 12"
                    print(self.navigator)
                    nav = Navigation(self.frame)
                    nav.recherche_vocale(self.navigator)
                    nav.pack(side=TOP)
                    direction = "prenez à votre droite ensuite montez jusqu'au premier étage puis tournez à droite," \
                                " vous êtes arrivez"
                    speak.tts(direction, lang)

                elif re.search("auditoire 23 merci", message) or re.search("23 merci", message):
                    self.answer("ok 23")
                    self.navigator = "auditoire 23"
                    print(self.navigator)
                    nav = Navigation(self.frame)
                    nav.recherche_vocale(self.navigator)
                    nav.pack(side=TOP)
                    direction = "Prenez à votre droite jusqu'à l'escalier, montez jusqu'au deuxième étage puis " \
                                "faite quelques pas sur votre gauche l'auditoire se trouve à droite"
                    speak.tts(direction, lang)


                elif re.search("auditoire 25 merci", message) or re.search("25 merci", message):
                    self.answer("ok 25")
                    self.navigator = "auditoire 25"
                    print(self.navigator)
                    nav = Navigation(self.frame)
                    nav.recherche_vocale(self.navigator)
                    nav.pack(side=TOP)
                    direction = "comme indiquez sur le plan, prenez à votre droite ensuite montez jusqu'au deuxième" \
                                " étage l'auditoire est face à vous légèrement à droite"
                    speak.tts(direction, lang)


                elif (re.search("auditoire 05 merci", message)
                      or re.search("5 merci", message)
                      or re.search("05 merci", message)):
                    self.answer("ok 05")
                    self.navigator = "auditoire 05"
                    print(self.navigator)
                    nav = Navigation(self.frame)
                    nav.recherche_vocale(self.navigator)
                    nav.pack(side=TOP)
                    direction = "comme indiquer sur le plan prenez à votre droite jusqu'au IGLAB puis tournez à " \
                                "droite, la destination est à votre droite"
                    speak.tts(direction, lang)

                elif (re.search("hall d'entrer merci", message) or re.search("secrétariat des étudiants merci",
                                                                             message)):
                    self.answer("vous y êtes")

                elif (re.search("accueil merci", message)):
                    self.answer("acceuil ok")
                    self.navigator = "accueil"
                    accueil = Accueil(self.frame)
                    accueil.pack(side=TOP, anchor=N, fill=BOTH, expand=YES)


                    print(self.navigator)

                elif re.search("activité merci", message):
                    self.answer("activité ok")
                    self.navigator = "activite"

                    activitePage = Activite(self.frame)
                    activitePage.pack(side=TOP)

                    print(self.navigator)


                elif re.search("navigation merci", message):
                    self.answer("ok")
                    self.navigator = "navigation"
                    print(self.navigator)
                    nav = Navigation(self.frame)
                    nav.pack(side=TOP)



                elif re.search("programme des études merci", message) or re.search("P A E merci",
                                                                             message):


                    paePage = Pae(self.frame)
                    paePage.pack(side=TOP)

                    self.answer("pae ok")
                    self.navigator = "pae"
                    print(self.navigator)

                elif re.search("miroir merci", message):
                    self.welcome()

        os.system("pause")

# ------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------ #
# ---------------------------- lancement de l'interface ------------------------------------------ #
# ------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------ #


interface = FullscreenWindow()
interface.fenetre_principale_tk.mainloop()



