import customtkinter as ctk
from typing import Self
import asyncio
from baza import Baza
from tkinter import END
import hashlib
import random

baza = Baza(__file__)

plava = "#6495ED"
plava1 = "#4169E1"
b_pozadina = "#1F1F1E"
bijela = "#FFFFFF"
crna = "#000000"
siva = "#323332"
b_tekst = "#505050"

"""
Okvir za odabir/stvaranje razgovora

Pri pokretanju aplikacije vidljiv s lijeve strane
Zauzima 1/4 horizontalnog prostora
Ak se ude u razgovor, zatvori se, gumbom se opet otvara
"""
class OdabirRazgovora(ctk.CTkScrollableFrame):
    def __init__(self: Self, *args, **kwargs):#*args i **kwargs u slucaju da ih custom tkinter koristi sa strane (bez da znamo)
        super().__init__(*args, **kwargs)#custom tkinter postavi sam sebe
        
        #oznaka iznad "kutijice"
        chatsLabel=ctk.CTkLabel(self.master, text="Razgovori", font=("Arial", 20)) 
        chatsLabel.grid(row=0, column=0, pady=10, sticky="nsew")
        input=ctk.CTkTextbox(self.master, width=200, height=400)
        input.grid(row=1, column=0, pady=5, padx=10, sticky="nsew")
        input.bind("<<ListboxSelect>>", lambda: self.openChat())

    def openChat(self: Self):
        print("open Chat")
        pass

"""
Okvir za razgovor

Sadrzava prosle poruke, mjesto za pisanje(unost b_teksta),
slanje poruka i datoteka koje su automatski kriptirane i potpisane

"""
class Razgovor(ctk.CTkScrollableFrame):
    def __init__(self: Self, *args, **kwargs):#*args i **kwargs u slucaju da ih custom tkinter koristi sa strane (bez da znamo)
        super().__init__(*args, **kwargs)#custom tkinter postavi sam sebe

        

        self.trenutni=ctk.CTkLabel(razgovor, text="", font=("Arial", 20))
        self.trenutni.pack(pady=10)
        self.poruke=ctk.CTkTextbox(razgovor, height=400, state="disabled")
        self.poruke.pack(pady=5, padx=10, fill="both", expand=True)

    def openChat(self: Self):
        pass

class Login(ctk.CTkFrame):
    def __init__(self: Self, *args, **kwargs):
        super().__init__(*args, **kwargs)#custom tkinter postavi sam sebe

        

        self.trenutni=ctk.CTkLabel(razgovor, text="", font=("Arial", 20))
        self.trenutni.pack(pady=10)
        self.poruke=ctk.CTkTextbox(razgovor, height=400, state="disabled")
        self.poruke.pack(pady=5, padx=10, fill="both", expand=True)

    def openChat(self: Self):
        pass

class Login(ctk.CTkFrame):
    def __init__(self: Self, *args, **kwargs):
        super().__init__(*args, **kwargs)#custom tkinter postavi sam sebe
        self.UI()

    def UI(self: Self):
        # Frame
        innerFrame = ctk.CTkFrame(self.master, fg_color=bijela, bg_color=siva, height=350, width=300, corner_radius=20)
        innerFrame.grid(row=0, column=0, padx=240, pady=115)

        # Title Label
        title = ctk.CTkLabel(innerFrame, text="Dobrodošli natrag! \nPrijavite se:", text_color=b_tekst, font=("", 35, "bold"))
        title.grid(row=0, column=0, sticky="nw", pady=30, padx=10)

        # Username Entry
        self.usernameEntry = ctk.CTkEntry(innerFrame, text_color=b_tekst, 
                                          placeholder_text="Korisničko ime", fg_color=plava, 
                                          placeholder_text_color=b_tekst, font=("", 16, "bold"), 
                                          width=200, corner_radius=15, height=45)
        self.usernameEntry.grid(row=1, column=0, sticky="nwe", padx=30)

        # Password Entry
        self.passwordEntry = ctk.CTkEntry(innerFrame, text_color=b_tekst, 
                                           placeholder_text="Lozinka", fg_color=plava, 
                                           placeholder_text_color=b_tekst, font=("", 16, "bold"), 
                                           width=200, corner_radius=15, height=45, show="*")
        self.passwordEntry.grid(row=2, column=0, sticky="nwe", padx=30, pady=20)

        # Register Label
        registerLabel = ctk.CTkLabel(innerFrame, text="Registriraj se", text_color=b_tekst, 
                                     cursor="hand2", font=("", 15))
        registerLabel.grid(row=3, column=0, sticky="w", pady=20, padx=40)
        registerLabel.bind("<Button-1>", lambda e: self.registracija())

        # Login Button
        loginButton = ctk.CTkButton(innerFrame, text="Prijavi se", font=("", 15, "bold"), 
                                    height=40, width=60, fg_color=plava1, cursor="hand2", 
                                    corner_radius=15, command=self.prijava)
        loginButton.grid(row=3, column=0, sticky="ne", pady=20, padx=35)

    def prijava(self: Self):
        # Placeholder for login logic
        prijava1(5)
   
    def registracija(self: Self):
        # Placeholder for registration logic
        print("Registration window")

"""
Glavna aplikacija, nasljeduje klasu glavne aplikacije iz custom tkintera

U pocetku su vidljivi OdabirRazgovora i Razgovor (gore napravljene klase)
Ak se odabere/napravi razgovor, OdabirRazgovora se zatvori(ostaje gumb kojim se opet otvara)
"""
class Aplikacija(ctk.CTk):
    def __init__(self: Self, *args, **kwargs):#*args i **kwargs u slucaju da ih custom tkinter koristi sa strane (bez da znamo)
        super().__init__(*args, **kwargs)#custom tkinter postavi sam sebe

        self.title("WhatsApp")
        self.geometry("800x600")
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
        self.config(bg=siva)

    def initChat(self: Self):
        #glavni frame koji sadrzava 2 podframea
        self.frame=ctk.CTkFrame(self.master, corner_radius=0)
        self.frame.grid(row=0, column=0, sticky="nsew")

        #odvojeni prikaz popisa razgovora i aktivnog razgovora
        self.grid_columnconfigure(0, weight=1, uniform="column")
        self.grid_columnconfigure(1, weight=3, uniform="column")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        
        odabirRazgovora = OdabirRazgovora()
        odabirRazgovora.grid(row=0, column=0, sticky="nsew")

        razgovor=Razgovor(self.frame, corner_radius=0)
        razgovor.grid(row=0, column=1, sticky="nsew")

        #pisanje poruka
        self.unosporuka=ctk.CTkFrame(razgovor)
        self.unosporuka.pack(fill="x", padx=10, pady=5)

        self.unos=ctk.CTkEntry(self.unosporuka, placeholder_text="Retard", width=500)
        self.unos.pack(side="left", padx=0)

        self.posalji=ctk.CTkButton(self.unosporuka, text="Pošalji", command=lambda: self.slanje())
        self.posalji.pack(side="right", padx=0)

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
    def __init__(self,q=160,p=1024):
        self.q=self.generiraj1(q)
        self.p=self.generiraj1(p)
        while (self.p-1)%self.q!=0:
            self.p=self.generiraj(p)
        self.g=self.generiraj2()
        self.x=random.randint(1,self.q-1)
        self.y=pow(self.g,self.x,self.p)

    def generiraj1(self,b):
        while True:
            k=random.getrandbits(b)|1
            if self.prost(k):
                return k

    def prost(self,n):
        je=True
        for i in range(2,round(n**0.5)+1):
            if n%i==0:
                je=False
                break
        return je

    def generator2(self):
        h=2
        while True:
            g=pow(h,(self.p-1)//self.g,self.p)
            if g>1:
                return g
            h+=1
    def potpis(self,poruka):
        h=int(hashlib.sha1(message.encode()).hexdigest(),16)
        while True:
            k=random.randint(1,self.g-1)
            r=pow(self.g,k,self.p)%self.q
            if r==0:continue
            kinv=pow(k,1,self.q)
            s=(kinv*(h+self.x*r))%self.q
            if s!=0:break
        return (r,s)

    def verificiraj(self,poruka,potpis):
        r,s=potpis
        if not (0<r<self.q and 0<s<self.q):
            return False
        h=int(hashlib.sha1(message.encode()).hexdigest(),16)
        w=pow(s,-1,self.q)
        u1=(h*w)%self.q
        u2=(r*w)%self.q
        v=((pow(self.g,u1,self.p)*pow(self.y,u2,self.p))%self.p)%self.q
        dobro=v==r
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
