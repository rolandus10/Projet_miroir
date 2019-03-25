from tkinter import *
import webbrowser
from PIL import ImageTk, Image


# creer une fenetre
window = Tk()

# personnalisation de la fenetre

window.title("Test Menu")
window.geometry("1080x720")
window.config(background='Black')

# ouvrir plan
def premier_etage():
    # frame
    frame2 = Frame(window, bg='Black', bd=2, relief="groove")
    img2 = Image.open("TR__Plans_de_houdain/Screen Shot 2019-03-19 at 4.49.02 PM.png")
    img2= img2.resize((800,600), Image.ANTIALIAS)
    photo2 = ImageTk.PhotoImage(img2)
    PAE2 = Label(frame2, image = photo2)
    PAE2.image = photo2
    PAE2.pack()
    frame2.pack()

# frame
frame = Frame(window, bg='Black', bd=2, relief="groove")

# image

img = ImageTk.PhotoImage(Image.open("TR__Plans_de_houdain/Screen Shot 2019-03-19 at 4.49.02 PM.png"))  # PIL solution
#img.resize((10, 10), Image.ANTIALIAS)
# ajout d'elements

Navigation = Button(frame, text="Navigation", bg='#000000', fg='White', font=("Arial", 25), command=premier_etage)
Navigation.grid(row=0, column=0, padx=25, pady=25)

# Navigation.config(image=img)

PAE = Button(frame, text="PAE",  bg='#000000', fg='White', font=("Courrier", 25))
PAE.grid(row=0, column=1, sticky=W, padx=25, pady=25)


Activites = Button(frame, text="Activites",  bg='#000000', fg='White', font=("Courrier", 25))
Activites.grid(row=0, column=2, sticky=W, padx=25, pady=25)

Planning = Button(frame, text="Planning",  bg='#000000', fg='White', font=("Courrier", 25))
Planning.grid(row=0, column=3, sticky=W, padx=25, pady=25)

frame.pack(side=BOTTOM)




# lancement de la fentre
window.mainloop()
