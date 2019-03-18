from tkinter import *



# creer une fenetre
window = Tk()

# personnalisation de la fenetre
window.title("Test Menu")
window.geometry("1080x720")
window.config(background='Black')

# frame
frame = Frame(window, bg='Black', bd=2, relief=SUNKEN)

# ajout d'elements

Navigation = Button(frame, text="Navigation",  bg='#000000', fg='White', font=("Arial", 25))
Navigation.grid(row=0, column=0, padx=25, pady=25)

PAE = Button(frame, text="PAE",  bg='#000000', fg='White', font=("Courrier", 25))
PAE.grid(row=0, column=1, sticky=W, padx=25, pady=25)


Activites = Button(frame, text="Activites",  bg='#000000', fg='White', font=("Courrier", 25))
Activites.grid(row=0, column=2, sticky=W, padx=25, pady=25)

frame.pack(side=BOTTOM)

# lancement de la fentre
window.mainloop()
