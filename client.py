import customtkinter as ctk
from typing import Any, Self
import asyncio
from baza import Baza
from tkinter import END
import hashlib
import random
from time import time

baza = Baza(__file__)

b_plava = "#6495ED"
b_plava1 = "#4169E1"
b_pozadina = "#1F1F1E"
b_bijela = "#FFFFFF"
b_crna = "#000000"
b_siva = "#323332"
b_tekst = "#505050"

sql_posaljiPoruku = \
"""
INSERT INTO KORISNICI VALUES()
"""

"""
Okvir za odabir/stvaranje razgovora

Pri pokretanju aplikacije vidljiv s lijeve strane
Zauzima 1/4 horizontalnog prostora
"""
class OdabirRazgovora(ctk.CTkScrollableFrame):
    def __init__(self: Self, *args, **kwargs):#*args i **kwargs u slucaju da ih custom tkinter koristi sa strane (bez da znamo)
        super().__init__(*args, **kwargs)#custom tkinter postavi sam sebe

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.razgovori: list[list[ctk.CTkFrame | ctk.CTkLabel | ctk.CTkCanvas]] = []

        #test
        for i in range(20):
            self.addRazgovor()
            
        

    def addRazgovor(self: Self):
        self.rowconfigure(len(self.razgovori), weight=1)
        #self.columnconfigure(1, weight=1)

        visina = 30
        sirina = 30

        frame = ctk.CTkFrame(self, fg_color=b_crna, height=visina)
        frame.grid(row=len(self.razgovori), column=0, sticky="nsew", pady=2)
        frame.columnconfigure(0, weight=1)


        self.razgovori.append([frame,
                               ctk.CTkLabel(frame, text="neki tekst"),
                               ctk.CTkCanvas(frame, height=visina, width=sirina),
                               ])
        #u frameu
        self.razgovori[-1][1].grid(row=0, column=0, sticky="nsew", pady=2)
        self.razgovori[-1][2].grid(row=0, column=1, sticky="ns", pady=2)

        diameter = round(min(visina, sirina)*0.7)//2*2
        self.razgovori[-1][2].create_oval(((sirina-diameter)//2, (visina-diameter)//2), ((sirina+diameter)//2, (visina+diameter)//2), fill=b_bijela)

    def openChat(self: Self):
        print("open Chat")
        pass

"""
Okvir za razgovor

Sadrzava prosle poruke, mjesto za pisanje(unost b_teksta),
slanje poruka i datoteka koje su automatski kriptirane i potpisane

"""
class Razgovor(ctk.CTkFrame):
    def __init__(self: Self, *args, **kwargs):#*args i **kwargs u slucaju da ih custom tkinter koristi sa strane (bez da znamo)
        super().__init__(*args, **kwargs)#custom tkinter postavi sam sebe
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.initPoruke()
        self.initPisanjePoruka()

    def initPoruke(self: Self):
        self.okvirZaPoruke = ctk.CTkScrollableFrame(self)
        self.okvirZaPoruke.grid(row=0, column=0, sticky="nsew")

        self._poruke: list[ctk.CTkLabel] = []
        self._timestamp: list[float] = []

    def initPisanjePoruka(self: Self):
        #pisanje poruka
        self.unosPoruka=ctk.CTkFrame(self)
        self.unosPoruka.grid(row=1, column=0, padx=10, pady=5, sticky="sew")
        self.unosPoruka.rowconfigure(0, weight=1)
        self.unosPoruka.columnconfigure(0, weight=1)

        self.unos=ctk.CTkEntry(self.unosPoruka, placeholder_text="Napišite poruku")
        self.unos.grid(row=0, column=0, sticky="nsew")

        self.posalji=ctk.CTkButton(self.unosPoruka, text="Pošalji", command=lambda: self.slanje(self.unos.get()))
        self.posalji.grid(row=0, column=1)

    def slanje(self: Self, poruka):
        if poruka == "": return
        print("Poslana poruka:", poruka)

    #todo
    def dodajPoruku(self: Self, poruka: dict[str, Any]):
        self._poruke.append(poruka["message"])
        self._timestamp.append(poruka["timestamp"])


class Login(ctk.CTkFrame):
    def __init__(self: Self, *args, **kwargs):
        super().__init__(*args, **kwargs)#custom tkinter postavi sam sebe
        self.initUI()

    def initUI(self: Self):
        # Frame
        innerFrame = ctk.CTkFrame(self.master, fg_color=b_bijela, bg_color=b_siva, height=350, width=300, corner_radius=20)
        innerFrame.grid(row=0, column=0, padx=240, pady=115)

        # Title Label
        title = ctk.CTkLabel(innerFrame, text="Dobrodošli natrag! \nPrijavite se:", text_color=b_tekst, font=("", 35, "bold"))
        title.grid(row=0, column=0, sticky="nsew", pady=30, padx=10)

        # Username Entry
        self.usernameEntry = ctk.CTkEntry(innerFrame, text_color=b_tekst, 
                                          placeholder_text="Korisničko ime", fg_color=b_plava, 
                                          placeholder_text_color=b_tekst, font=("", 16, "bold"), 
                                          width=200, corner_radius=15, height=45)
        self.usernameEntry.grid(row=1, column=0, sticky="nsew", padx=30)

        # Password Entry
        self.passwordEntry = ctk.CTkEntry(innerFrame, text_color=b_tekst, 
                                           placeholder_text="Lozinka", fg_color=b_plava, 
                                           placeholder_text_color=b_tekst, font=("", 16, "bold"), 
                                           width=200, corner_radius=15, height=45, show="*")
        self.passwordEntry.grid(row=2, column=0, sticky="nsew", padx=30, pady=20)

        # Register Label
        registerLabel = ctk.CTkLabel(innerFrame, text="Registriraj se", text_color=b_tekst, 
                                     cursor="hand2", font=("", 15))
        registerLabel.grid(row=3, column=0, sticky="nsew", pady=20, padx=40)
        registerLabel.bind("<Button-1>", lambda: self.registracija())

        # Login Button
        loginButton = ctk.CTkButton(innerFrame, text="Prijavi se", font=("", 15, "bold"), 
                                    height=40, width=60, fg_color=b_plava1, cursor="hand2", 
                                    corner_radius=15, command=lambda: self.prijava(self.usernameEntry.get(), self.passwordEntry.get()))
        loginButton.grid(row=3, column=0, sticky="nsew", pady=20, padx=35)

    def prijava(self: Self, username, password):
        pass
        
   
    def registracija(self: Self, username, password):
        pass

"""
Glavna aplikacija, nasljeduje klasu glavne aplikacije iz custom tkintera

U pocetku su vidljivi OdabirRazgovora i Razgovor (gore napravljene klase)
Ak se odabere/napravi razgovor, OdabirRazgovora se zatvori(ostaje gumb kojim se opet otvara)
"""
class Aplikacija(ctk.CTk):
    def __init__(self: Self, *args, **kwargs):#*args i **kwargs u slucaju da ih custom tkinter koristi sa strane (bez da znamo)
        super().__init__(*args, **kwargs)#custom tkinter postavi sam sebe

        self.title("WhatsApp")
        self.resizable(True, True)
        self.minsize(800, 600)

        if not self.loggedIn():
            self.initLogin()
        
        else:
            self.initChat()

    def loggedIn(self: Self):
        return True
    
    def initLogin(self: Self):
        self.frame = Login(self)
        self.config(bg=b_siva)

    def initChat(self: Self):
        selfID = baza.cur.execute("SELECT korisnikID FROM Korisnici WHERE korisnickoIme=?", ()).fetchone()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        #glavni frame koji sadrzava 2 podframea
        self.frame=ctk.CTkFrame(master=self, corner_radius=0)
        self.frame.grid(row=0, column=0, sticky="nsew")

        #odvojeni prikaz popisa razgovora i aktivnog razgovora
        self.frame.columnconfigure(0, weight=1, uniform="column")
        self.frame.columnconfigure(1, weight=3, uniform="column")
        
        #self.frame.rowconfigure(0, weight=1) #doesnt expand vertically
        self.frame.rowconfigure(1, weight=1)
        
        #lijeva strana, razgovori
        self.chatsLabel=ctk.CTkLabel(self.frame, text="Razgovori", font=("Arial", 20)) 
        self.chatsLabel.grid(row=0, column=0, pady=10, sticky="new")
        self.odabirRazgovora = OdabirRazgovora(self.frame, fg_color=b_plava1)
        self.odabirRazgovora.grid(row=1, column=0, sticky="nsew")

        #desna strana, ime razgovora, poruke i slanje
        self.imeRazgovora=ctk.CTkLabel(self.frame, text="", font=("Arial", 20))
        self.imeRazgovora.grid(row=0, column=1, sticky="nsew")
        self.razgovor = Razgovor(self.frame)
        self.razgovor.grid(row=1, column=1, sticky="nsew")

    def provjeriZaNovePoruke(self: Self):
        pass

    def button_callback(self: Self):
        print("button pressed")

    def otvorirazgovor(self: Self):
        pass

    def slanje(self: Self, *args):
        pass

def prijava1(n: int):
    print("posrani sam")

class DSA:
    def __init__(self: Self, q=160, p=1024):
        self.q=self.generiraj1(q)
        self.p=self.generiraj1(p)
        while (self.p-1)%self.q!=0:
            self.p=self.generiraj1(p)
        self.g=self.generator2()
        self.x=random.randint(1,self.q-1)
        self.y=pow(self.g,self.x,self.p)

    def generiraj1(self: Self, b):
        while True:
            k=random.getrandbits(b)|1
            if self.prost(k):
                return k

    def prost(self: Self, n):
        je=True
        for i in range(2,round(n**0.5)+1):
            if n%i==0:
                je=False
                break
        return je

    def generator2(self: Self):
        h=2
        while True:
            g=pow(h, (self.p-1)//self.g, self.p)
            if g>1:
                return g
            h+=1

    def potpis(self: Self, message):
        h=int(hashlib.sha1(message.encode()).hexdigest(),16)
        while True:
            k=random.randint(1,self.g-1)
            r=pow(self.g,k,self.p)%self.q
            if r==0:continue
            kinv=pow(k,1,self.q)
            s=(kinv*(h+self.x*r))%self.q
            if s!=0:break
        return (r,s)

    def verificiraj(self: Self, message, sig):
        r,s=sig
        if not (0<r<self.q and 0<s<self.q):
            return False
        h=int(hashlib.sha1(message.encode()).hexdigest(),16)
        w=pow(s,-1,self.q)
        u1=(h*w)%self.q
        u2=(r*w)%self.q
        v=((pow(self.g,u1,self.p)*pow(self.y,u2,self.p))%self.p)%self.q
        dobro= (v==r)
        return dobro

#korištenje:
##dsa=DSA()
##poruka="Dobar dan"
##potpis=dsa.potpis(poruka)
##verificiraj=dsa.verificiraj(poruka,potpis)
##print(verificiraj)

if __name__ == "__main__":
    whatsApp=Aplikacija()
    whatsApp.mainloop()
