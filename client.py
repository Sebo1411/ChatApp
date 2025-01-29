import customtkinter as ctk
import asyncio
from baza import Baza
from tkinter import END

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
    
    def provjeriZaNovePoruke(self):
        pass

    def button_callback(self):
        print("button pressed")

#glavni prozor
#imamo dvije klase za svaki razgovor, to bude popravljeno uskoro
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

##chat = Aplikacija()
##chat.mainloop()
class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacija")
        self.geometry("800x600")

        #odvojeni prikaz popisa razgovora i aktivnog razgovora
        self.grid_columnconfigure(0,weight=1,uniform="column")
        self.grid_columnconfigure(1,weight=3,uniform="column")
        self.grid_rowconfigure(0,weight=1)

        #dio sa svim razgovorima
        self.razgovori=ctk.CTkFrame(self,corner_radius=0)
        self.razgovori.grid(row=0,column=0,sticky="nsew")
        self.oznakar=ctk.CTkLabel(self.razgovori,text="Razgovori",font=("Arial",20)) #oznaka iznad "kutijice"
        self.oznakar.pack(pady=10)
        self.kutijar=ctk.CTkTextbox(self.razgovori,width=200,height=400)
        self.kutijar.pack(pady=5,padx=10,fill="both",expand=True)
        self.kutijar.bind("<<ListboxSelect>>",self.otvorirazgovor)

        #dio s pojedinačnim razgovorom
        self.razgovor=ctk.CTkFrame(self,corner_radius=0)
        self.razgovor.grid(row=0,column=1,sticky="nsew")
        self.trenutni=ctk.CTkLabel(self.razgovor,text="Odaberite razgovor",font=("Arial",20))
        self.trenutni.pack(pady=10)
        self.poruke=ctk.CTkTextbox(self.razgovor,height=400,state="disabled")
        self.poruke.pack(pady=5,padx=10,fill="both",expand=True)

        #pisanje poruka
        self.unosporuka=ctk.CTkFrame(self.razgovor)
        self.unosporuka.pack(fill="x", padx=10, pady=5)

        self.unos=ctk.CTkEntry(self.unosporuka, placeholder_text="Retard", width=500)
        self.unos.pack(side="left", padx=0)

        self.posalji=ctk.CTkButton(self.unosporuka,text="Pošalji",command=self.slanje)
        self.posalji.pack(side="right", padx=0)

 
    def otvorirazgovor():
        pass
    def slanje(args):
        pass

    #trebalo bude biti jos potprograma, za sad je to to

class LoginApp:
    def __init__(self):
        # Colors and settings
        self.plava = "#6495ED"
        self.plava1 = "#4169E1"
        self.pozadina = "#1F1F1E"
        self.bijela = "#FFFFFF"
        self.crna = "#000000"
        self.siva = "#323332"
        self.tekst = "#505050"

        # Main application window
        self.main = ctk.CTk()
        self.main.title("Login-stranica")
        self.main.config(bg=self.siva)
        self.main.geometry("800x600")
        self.main.resizable(False, False)

        # Build UI
        self.UI()

    def UI(self):
        # Frame
        frame1 = ctk.CTkFrame(self.main, fg_color=self.bijela, bg_color=self.siva, height=350, width=300, corner_radius=20)
        frame1.grid(row=0, column=0, padx=240, pady=115)

        # Title Label
        title = ctk.CTkLabel(frame1, text="Dobrodošli natrag! \nPrijavite se:",text_color=self.tekst, font=("", 35, "bold"))
        title.grid(row=0, column=0, sticky="nw", pady=30, padx=10)

        # Username Entry
        self.username_entry = ctk.CTkEntry(frame1, text_color=self.tekst, 
                                          placeholder_text="Korisničko ime", fg_color=self.plava, 
                                          placeholder_text_color=self.tekst, font=("", 16, "bold"), 
                                          width=200, corner_radius=15, height=45)
        self.username_entry.grid(row=1, column=0, sticky="nwe", padx=30)

        # Password Entry
        self.password_entry = ctk.CTkEntry(frame1, text_color=self.tekst, 
                                         placeholder_text="Lozinka", fg_color=self.plava, 
                                         placeholder_text_color=self.tekst, font=("", 16, "bold"), 
                                         width=200, corner_radius=15, height=45, show="*")
        self.password_entry.grid(row=2, column=0, sticky="nwe", padx=30, pady=20)

        # Register Label
        cr_acc = ctk.CTkLabel(frame1, text="Registriraj se", text_color=self.tekst, 
                              cursor="hand2", font=("", 15))
        cr_acc.grid(row=3, column=0, sticky="w", pady=20, padx=40)
        cr_acc.bind("<Button-1>", lambda e: self.registracija())

        # Login Button
        l_btn = ctk.CTkButton(frame1, text="Prijavi se", font=("", 15, "bold"), 
                              height=40, width=60, fg_color=self.plava1, cursor="hand2", 
                              corner_radius=15, command=self.prijava)
        l_btn.grid(row=3, column=0, sticky="ne", pady=20, padx=35)

    def prijava(self):
        # Placeholder for login logic
        prijava1(5)
   
    def registracija(self):
        # Placeholder for registration logic
        print("Registration window")

    def run(self):
        self.main.mainloop()
def prijava1(n):
    print("posrani sam")
a=LoginApp()
a.run()
