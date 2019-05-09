
from gtts import gTTS   # google teste to speech simple
from pygame import mixer
import os

# permet de recuperer le text et de le lire dans l'un des languages disponible dans gTTS
def tts(text, lang):
    filename = 'sample.mp3'  # chemin vers le document mp3
    file = gTTS(text=text, lang=lang)   # transcription du texte en fichier audio mp3
    file.save(filename)
    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()
    os.remove(filename)