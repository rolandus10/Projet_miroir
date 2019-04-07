import tkinter

def top():
  fenetre0=tkinter.Toplevel()
  fenetre0.title("Seconde")

racine0=tkinter.Tk()
racine0.title("Principale")
bouton0=tkinter.Button(text="Autre", command=top)
bouton0.pack()
racine0.mainloop()