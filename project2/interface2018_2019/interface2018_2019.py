"*********INTERFACE MIROIRE********"

from tkinter import *
import locale
import datetime
import time
import threading
from contextlib import contextmanager
import traceback
import requests
import json
import sys
import os
import feedparser
from PIL import Image, ImageTk

from PIL import Image, ImageTk

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
xlarge_text_size = 84
large_text_size = 38
medium_text_size = 18
small_text_size = 38
xsmall_text_size = 38
tiny_text_size = 1
counterMax = 10

myName = "Inconnu"
mat = 1
horaire = False
w = None
discuss = True

tk = Tk()

tl = 2  # for little sentences
tL = 5  # for long sentences
t = tl  # default configuration


@contextmanager
def setlocale(name):  # thread proof function to work with locale
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

        # self.after(600000, self.get_weather)

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# -------------------------------- TEXT --------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


class Text(Frame):
    def __init__(self, parent, text, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.contentText = text
        self.contentTextLbl = Label(self, text=self.contentText, font=('Helvetica', tiny_text_size), fg="white",
                                    bg="black")
        self.contentTextLbl.pack(side=LEFT, anchor=N)

    def updateText(self, newText):
        self.contentTextLbl.config(text=newText)


class TextBig(Frame):
    def __init__(self, parent, text, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.contentText = text
        self.contentTextLbl = Label(self, text=self.contentText, font=('Helvetica', xsmall_text_size), fg="white",
                                    bg="black")
        self.contentTextLbl.pack(side=LEFT, anchor=N)

    def updateText(self, newText):
        self.contentTextLbl.config(text=newText)


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

    def tick(self):
        with setlocale(ui_locale):
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

class News(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'News'  # 'News' is more internationally generic
        self.newsLbl = Label(self, text=self.title, font=('Helvetica', large_text_size), fg="white", bg="black")
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
                    headline = NewsHeadline(self.headlinesContainer, event)
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

        if ((re.search("image", event_name) or re.search("vidéo", event_name) or re.search("cliché",
                                                                                           event_name) or re.search(
                "photo", event_name))):
            self.toPrint = False
        if self.toPrint == True:
            self.iconLbl.pack(side=LEFT, anchor=N)
            self.eventName = event_name
            self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', xsmall_text_size), fg="white",
                                      bg="black")
            self.eventNameLbl.pack(side=LEFT, anchor=N)

FONT_menu = ("Arial", 25)

class FullscreenWindow:
    def __init__(self,tk):

        global myName
        nbr = 0
        if nbr == 0:
            # self.tk = Tk()
            self.tk = tk
            self.tk.configure(background='black')

            self.state = False
            self.toggle_fullscreen()
            # self.end_fullscreen()
            # self.tk.bind("<Return>", self.toggle_fullscreen)
            self.tk.bind("<Escape>", self.end_fullscreen)

            # self.fr= FacialRecognition()
            # mat = self.fr.get_matricule()
            # myName=self.fr.get_nom(mat)
            # myName=myName.lower().capitalize()

            self.acceuil()
            nbr += 1


    def menuFrame(self):# affichage du menu

        # effacer tout dans la fenetre avant l'affichage
        for frame in self.tk.winfo_children():
            frame.destroy()

        menu = Frame(self.tk, bg="black")
        menu.pack(side=BOTTOM)
        navigation = Button(menu, text="Navigation", font=FONT_menu, command=self.navigation)
        navigation.grid(row=0, column=0, sticky="nsew")
        buttonAcceuil = Button(menu, text="Acceuil", font=FONT_menu, command=self.acceuil)
        buttonAcceuil.grid(row=0, column=1, sticky="nsew")
        activite = Button(menu, text="activite", font=FONT_menu, command=self.toggle_fullscreen)
        activite.grid(row=0, column=2, sticky="nsew")
        pae = Button(menu, text="Pae", font=FONT_menu)
        pae.grid(row=0, column=3, sticky="nsew")


    def acceuil(self):

        self.menuFrame()


        self.topFrame = Frame(self.tk, background='black')
        self.topFrame.pack(side=TOP, anchor=N, fill=BOTH, expand=YES)

         # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=50, pady=30)

        # self.text = SpeechRecognition(self.bottomFrame)
        # self.text.pack(side=TOP, anchor=N, padx=100, pady=5)
        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=10)

         # news
        self.news = News(self.topFrame)
        self.news.pack(side=BOTTOM, anchor=N, padx=100, pady=60)
        # calender
        # self.fr.get_matricule()
        # self.calender = Calendar(self.bottomFrame)
        # self.calender.pack(side = RIGHT, anchor=S, padx=100, pady=60)

        # self.facialRecognition()
        # self.speechRecognition()


    def navigation(self):

        self.menuFrame()

        nav = Navigation(self.tk)
        nav.pack(side=TOP)







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
        self.fr = FacialRecognition()
        mat = self.fr.get_matricule()
        myName = self.fr.get_nom(mat)
        myName = myName.lower().capitalize()

    def speechRecognition(self):
        self.text = SpeechRecognition(self.bottomFrame)
        self.text.pack(side=TOP, anchor=N, padx=100, pady=5)

#class qui gere l'affichage des plans
class Navigation(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg="black")
        self.topFrame = Frame(self, background='black')
        self.topFrame.pack(side=TOP)
        self.inputRecherche = Entry(self.topFrame, bd=1)
        self.inputRecherche.grid(row=0, column=0, sticky=E)
        self.recherche = Button(self.topFrame, text="Recherche", font=FONT_menu, command=self.recherche)
        self.recherche.grid(row=0, column=1, sticky=W)

        self.dictionnaireDesPlans = {'auditoire 05': "plans/aud05.png",
                                     'auditoire 11': "plans/aud11.1.PNG"}

        cheminImage = "plans/etage0.PNG"
        img2 = Image.open(cheminImage)
        img2 = img2.resize((800, 600), Image.ANTIALIAS)
        photo2 = ImageTk.PhotoImage(img2)
        affiche = Label(self.topFrame, image=photo2)
        affiche.image = photo2
        affiche.grid(row=1, columnspan=2, pady=10)


    def recherche(self):
        # on recupère les informations du inputRecherche et on recherche le local dans dictionnaireDesPlans
        # puis on affiche
        local = self.inputRecherche.get()
        plans = self.dictionnaireDesPlans

        if local in plans:
            cheminImage = plans[local]
            img2 = Image.open(cheminImage)
            img2 = img2.resize((800, 600), Image.ANTIALIAS)
            photo2 = ImageTk.PhotoImage(img2)
            affiche = Label(self.topFrame, image=photo2)
            affiche.image = photo2
            affiche.grid(row=1, columnspan=2, pady=10)




##if __name__ == '__main__':
##    global w
##    w = FullscreenWindow()
##    w.tk.mainloop()

w = FullscreenWindow(tk)
w.tk.mainloop()



