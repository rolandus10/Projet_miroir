import tkinter as tk

from PIL import ImageTK, Image

LARGE_FONT=("verdana",12)

class SeaofBTCapp(tk.TK):
    def __init__(self,*arg,**kwargs):

        tk.TK._init_(self,*arg,**kwargs)
        container = tk.Frame(self)

        container.pack(side="top",fill="both", expand = True)
        container.grid_columnconfigure(0,weight=1)

        self.frames ={}

        for F in(StartPage, PageOne):

            frame = F(container,self)
            self.frames[F]=frame

            frame.grid(row=0, column=0,sticky="nsew")
        self.show_frame(StartPage)
    def show_frame(self,cont):
        frame= self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame._init_(self,parent)
        label = tk.Label(self,text="Start Page", font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self , text="visite p1",
                           command= lambda:controller.show_frame(PageOne))
        button.pack()

class PageOne(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame._init_(self,parent)
        label = tk.Label(self,text="Page one", font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self , text="Back to home",
                           command= lambda:controller.show_frame(PageOne))
        button.pack()

app= SeaofBTCapp
app.mainloop()
