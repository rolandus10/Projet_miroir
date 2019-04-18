from tkinter import *
import webbrowser
from PIL import ImageTk, Image


FONT_menu = ("Arial", 25)
Font_page = ("Courrier", 80)



class Interface(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        interface = Frame(self, bg="Green")
        self.state = False
        interface.pack(fill="both", expand=YES)
        self.toggle_fullscreen()
        self.bind("<Escape>", self.end_fullscreen)


        self.frames = {}

        for page in (Navigation, PAE):
            frame = page(interface, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PAE)


    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"


class Navigation(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="black")
        label = Label(self, text="Page de Navigation!", font=Font_page)
        label.pack(expand=YES)

        menu = Frame(self, bg="green")

        nav = Button(menu, text="Navigation", bg='#000000', fg='White', font=FONT_menu,
                     command=lambda: controller.show_frame(Navigation))
        nav.pack(side=LEFT, fill="both", expand=YES)

        Pae = Button(menu, text="PAE", bg='#000000', fg='White', font=FONT_menu,
                     command=lambda: controller.show_frame(PAE))
        Pae.pack(side=LEFT, fill="both", expand=YES)

        menu.pack(side=BOTTOM, fill="both", expand=YES)

class PAE(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="black")

        label = Label(self, text="Page de PAE!", font=Font_page)
        label.pack(expand=YES)

        menu =Frame(self, bg="green")

        nav = Button(menu, text="Navigation", bg='#000000', fg='White', font=FONT_menu,
                     command=lambda: controller.show_frame(Navigation))
        nav.pack(side=LEFT, fill="both", expand=YES)

        Pae = Button(menu, text="PAE", bg='#000000', fg='White', font=FONT_menu,
                     command=lambda: controller.show_frame(PAE))
        Pae.pack(side=LEFT, fill="both", expand=YES)

        menu.pack(side=BOTTOM, fill="both", expand=YES)



interfaceGraphique = Interface()
interfaceGraphique.mainloop()


# creer une fenetre
window = Tk()

# personnalisation de la fenetre

window.title("Test Menu")
window.geometry("1080x720")
window.config(background='Black')

# ouvrir plan

frame2 = Frame(window, bg='Black', bd=2, relief="groove")
def premier_etage():
    # frame
    img2 = Image.open("TR__Plans_de_houdain/Screen Shot 2019-03-19 at 4.49.02 PM.png")
    img2= img2.resize((800,600), Image.ANTIALIAS)
    photo2 = ImageTk.PhotoImage(img2)
    PAE2 = Label(frame2, image = photo2)
    PAE2.image = photo2
    PAE2.pack()
    frame2.pack()
    Activites = Button(menu, text="Activites", bg='#000000', fg='White', font=FONT_menu,
                       command=self.Print("eco"))
    Activites.grid(row=0, column=2, sticky=W, padx=25, pady=25)

    Planning = Button(menu, text="Planning", bg='#000000', fg='White', font=FONT_menu,
                      command=self.Print("eco"))
    Planning.grid(row=0, column=3, sticky=W, padx=25, pady=25)



# frame


# image

img = ImageTk.PhotoImage(Image.open("TR__Plans_de_houdain/Screen Shot 2019-03-19 at 4.49.02 PM.png"))  # PIL solution
#img.resize((10, 10), Image.ANTIALIAS)
# ajout d'elements







# lancement de la fentre
window.mainloop()
