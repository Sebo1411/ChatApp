import customtkinter
import asyncio
from baza import Baza

baza = Baza(__file__)

"""
Okvir za odabir/stvaranje razgovora

Pri pokretanju aplikacije vidljiv s lijeve strane
Zauzima 1/4 horizontalnog prostora
Ak se ude u razgovor, zatvori se, gumbom se opet otvara
"""
class OdabirRazgovora(customtkinter.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):#*args i **kwargs u slucaju da ih custom tkinter koristi sa strane (bez da znamo)
        super().__init__(*args, **kwargs)#custom tkinter postavi sam sebe
        #...

"""
Okvir za razgovor

Sadrzava prosle poruke, mjesto za pisanje(unost teksta),
slanje poruka i datoteka koje su automatski kriptirane i potpisane

"""
class Razgovor(customtkinter.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):#*args i **kwargs u slucaju da ih custom tkinter koristi sa strane (bez da znamo)
        super().__init__(*args, **kwargs)#custom tkinter postavi sam sebe
        #...

"""
Glavna aplikacija, nasljeduje klasu glavne aplikacije iz custom tkintera

U pocetku su vidljivi OdabirRazgovora i Razgovor (gore napravljene klase)
Ak se odabere/napravi razgovor, OdabirRazgovora se zatvori(ostaje gumb kojim se opet otvara)
"""
class Aplikacija(customtkinter.CTk):
    def __init__(self, *args, **kwargs):#*args i **kwargs u slucaju da ih custom tkinter koristi sa strane (bez da znamo)
        super().__init__(*args, **kwargs)#custom tkinter postavi sam sebe

        #default kod, treba pomijeniti...
        self.title("my app")
        self.geometry("400x150")
        self.grid_columnconfigure((0, 1), weight=1)

        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        self.checkbox_1.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
        self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
        self.checkbox_2.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="w")
        
    def button_callback(self):
        print("button pressed")

chat = Aplikacija()
chat.mainloop()