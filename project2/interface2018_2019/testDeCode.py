from tkinter import *

liste_j = ["FT", "WSJ", "CNN"]


class App(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         **kwargs)  # super() renvoie les class dont hérite App, c-a-d Tk ici. En utilisant super() , le paramètre self est passé automatiquement
        self.begin()

    def begin(self):
        startpage = StartPage(self)  # on crée la startpage
        startpage.pack()
        startpage.bind('<<NEXT>>',
                       lambda e: self.next_page(startpage))  # on attend l'evenement '<<NEXT>>' pour continuer

    def next_page(self, startpage):
        values = [intvar.get() for intvar in
                  startpage.intvars]  # on récupère les valeurs dans une liste du type [1, 0, 1]
        startpage.pack_forget()  # ou grid_remove si grid()
        display = Display(self, values)
        display.pack()


class StartPage(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.intvars = []  # les IntVar seront stockés dans cette liste pour y acceder facilement<br>                          # depuis le controleur. les valeurs des Checkbutton sont conservées dans les IntVar
        self.checkbuttons()

    def checkbuttons(self):
        for i, s in enumerate(liste_j):
            intvar = IntVar()  # L'Intvar d'un bouton coché vaut 1 sinon 0
            self.intvars.append(intvar)  # pour acceder aux IntVar en les différenciant (par leur index dans la liste)
            c = Checkbutton(self, text=s, variable=intvar)  # étant dans une boucle for, chaque CB a son IntVar
            c.pack()
        Button(self, text='NEXT', command=lambda: self.event_generate('<<NEXT>>')).pack()


class Display(Frame):
    def __init__(self, master, values, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [liste_j[i] for i, value in enumerate(values) if
                   value]  # on crée une liste des mots correspondants aux cases cochées
        print(choices)  # print pour vérifier
        Label(self, text="Vous avez choisi {}".format(choices)).pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()