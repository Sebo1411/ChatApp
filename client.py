import customtkinter as ctk
from typing import Self
import asyncio
from baza import Baza
from tkinter import END
import random
from hashlib import sha1
import os

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
    def __init__(self):
        self.p, self.q, self.g = self.parameter_generation()
        self.x, self.y = self.per_user_key()

    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def get_prime(self, bits):
        while True:
            num = random.getrandbits(bits) | 1  # Ensure it's an odd number
            if self.is_prime(num):
                return num

    def hash_function(self, message):
        return sha1(message.encode("UTF-8")).hexdigest()

    def hash_function1(self,file_path):
        name=os.path.basename(file_path)
        with open(name,"r") as file:
            text=file.read()
        return self.hash_function(text)

    def mod_inverse(self, a, m):
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return 1

    def parameter_generation(self):
        q = self.get_prime(5)
        p = self.get_prime(10)
        while (p - 1) % q != 0:
            p = self.get_prime(10)
            q = self.get_prime(5)

        
        while True:
            h = random.randint(1, p - 1)
            g = pow(h,int((p-1)/q))%p
            if g > 1:
                break
        print(p,q,g)
        return p,q,g

    def per_user_key(self):
        x = random.randint(1, self.q - 1)
        y = pow(self.g, x, self.p)%self.p
        return x, y

    def sign(self, file_path):
        ime=os.path.basename(file_path)
        with open(ime, "r") as file:
            text = file.read()
        hash_component = self.hash_function(text) #primljeni hash od dokumenta

        r, s = 0, 0
        while r == 0 or s == 0:
            k = random.randint(1, self.q - 1)
            r = ((pow(self.g,k))%self.p)%self.q
            i = self.mod_inverse(k, self.q)
            hashed = int(hash_component, 16)
            s = (i * (hashed + (self.x * r))) % self.q
        
        return r, s, k

    def verify(self, file_path, r, s):
        ime=os.path.basename(file_path)
        with open(ime, "r") as file:
            text = file.read()
        hash_component = self.hash_function(text)

        w = self.mod_inverse(s, self.q)
        
        hashed = int(hash_component, 16)
        u1 = (hashed * w) % self.q
        u2 = (r * w) % self.q
        v = ((pow(self.g,u1)*pow(self.y,u2))%self.p)%self.q
        if v == r:
            return True
        else:
            return False

# Example usage:
dsa = DSA()
file_path = input("Put: ") #rC:\Users\DOMINIK-LPT\Desktop\Tujesjedio.txt 
signature = dsa.sign(file_path)
print("Signature (r, s, k):", signature)
hash1=dsa.hash_function1(file_path)
print("Hash: ",hash1)
print()

file_path = input("Put: ")
print(dsa.verify(file_path, signature[0], signature[1])) #True ako je valjan False ako nije
if __name__ == "__main__":
    whatsApp=Aplikacija()
    whatsApp.mainloop()
