# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:29:20 2019

@author: djakd
"""

from gtts import gTTS# google teste to speech simple

import pyglet#permet de jouer les fichier audio depuis le programme

import time, os


#permet de recuperer le text et de le lire dans l'un des languages disponible dans le package pyglet
def tts(text, lang):

    file = gTTS(text = text, lang = lang)

    filename = 'sample.mp3'# chemin vers le document mp3

    file.save(filename)



    music = pyglet.media.load(filename, streaming = False)

    music.play()



    time.sleep(music.duration)

    os.remove(filename)