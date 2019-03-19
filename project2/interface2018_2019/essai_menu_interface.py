from tkinter import *

from PIL import ImageTk, Image


# creer une fenetre
window = Tk()

# personnalisation de la fenetre
window.title("Test Menu")
window.geometry("1080x720")
window.config(background='Black')

# ouvrir plan
def premier_etage():
    # creer une fenetre
    window2 = Tk()
    # personnalisation de la fenetre
    window2.title("1er Etage")
    window2.geometry("1920x1080")
    window2.config(background='Black')
    # image
    #img = ImageTk.PhotoImage(Image.open("assets/iconfinder_navigation.png")) # PIL solution
    img = PhotoImage(file="assets/iconfinder_navigation.png") # PIL solution
    plan = Label(window2, image=img, text="Navigation", bg='#000000', fg='White', font=("Arial", 25))
    plan.pack()
    window2.mainloop()

# frame
frame = Frame(window, bg='Black', bd=2, relief="groove")

# image

#img = ImageTk.PhotoImage(Image.open("assets/iconfinder_navigation.png"))  # PIL solution
#img.__size((10, 10), Image.ANTIALIAS)
# ajout d'elements

Navigation = Button(frame, text="Navigation", bg='#000000', fg='White', font=("Arial", 25), command=premier_etage)
Navigation.grid(row=0, column=0, padx=25, pady=25)

#Navigation.config(image=img)

PAE = Button(frame, text="PAE",  bg='#000000', fg='White', font=("Courrier", 25))
PAE.grid(row=0, column=1, sticky=W, padx=25, pady=25)


Activites = Button(frame, text="Activites",  bg='#000000', fg='White', font=("Courrier", 25))
Activites.grid(row=0, column=2, sticky=W, padx=25, pady=25)

Planning = Button(frame, text="Planning",  bg='#000000', fg='White', font=("Courrier", 25))
Planning.grid(row=0, column=3, sticky=W, padx=25, pady=25)

frame.pack(side=BOTTOM)




# lancement de la fentre
window.mainloop()
