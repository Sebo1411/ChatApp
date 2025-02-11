from threading import Thread
import customtkinter as ctk
from typing import Any, Self, Optional
import asyncio
from baza import Baza
from tkinter import END
import random
from hashlib import sha1
import os
import time
import socket
import gc
import asyncio
import ast
import traceback
import tracemalloc

class RequestParser:
    def __init__(self: Self):
        self.data: list[bytes] = []

    def append(self: Self, data: bytes):
        self.data.append(data)
    
    def parse(self: Self) -> dict[str, Any]:
        return ast.literal_eval("".join(data.decode("utf-8") for data in self.data)) #ocekuje dict, dekodira, spaja u jedan string i pretvara u dict
    
    def isEmpty(self: Self):
        return len(self.data) == 0

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
        #for i in range(20):
        #    self.addRazgovor()
            
        

    def addRazgovor(self: Self, username):
        print(f"dodana razgovor s {username}")

        self.rowconfigure(len(self.razgovori), weight=1)
        #self.columnconfigure(1, weight=1)

        visina = 30
        sirina = 30

        frame = ctk.CTkFrame(self, fg_color=b_crna, height=visina)
        frame.grid(row=len(self.razgovori), column=0, sticky="nsew", pady=2)
        frame.columnconfigure(0, weight=1)


        self.razgovori.append([frame,
                               ctk.CTkLabel(frame, text=username),
                               ctk.CTkCanvas(frame, height=visina, width=sirina),
                               ])
        #u frameu
        self.razgovori[-1][1].grid(row=0, column=0, sticky="nsew", pady=2)
        self.razgovori[-1][2].grid(row=0, column=1, sticky="ns", pady=2)
        
        assert type(self.razgovori[-1][2]) is ctk.CTkCanvas, "nije canvas"
        self.razgovori[-1][2].create_aa_circle(x_pos=round(sirina/2), y_pos=round(visina/2), radius=round(min(sirina/2, visina/2)*0.7), fill=b_bijela)

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
        app: Aplikacija = self.master.master #type: ignore

        #pisanje poruka
        self.unosPoruka=ctk.CTkFrame(self)
        self.unosPoruka.grid(row=1, column=0, padx=10, pady=5, sticky="sew")
        self.unosPoruka.rowconfigure(0, weight=1)
        self.unosPoruka.columnconfigure(0, weight=1)

        self.unos=ctk.CTkEntry(self.unosPoruka, placeholder_text="Napišite poruku")
        self.unos.grid(row=0, column=0, sticky="nsew")

        self.posalji=ctk.CTkButton(self.unosPoruka, text="Pošalji", command=lambda: app.slanje(self.unos.get()))
        self.posalji.grid(row=0, column=1)


class Login(ctk.CTkFrame):
    def __init__(self: Self, *args, **kwargs):
        super().__init__(*args, **kwargs)#custom tkinter postavi sam sebe
        self.initUI()

        #aplikacija i njezine metode, npr. Aplikacija.successfulLoginCallback() su metode na self.master

    def initUI(self: Self):
        # Frame
        innerFrame = ctk.CTkFrame(self.master, fg_color=b_bijela, height=350, width=300, corner_radius=20)
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

        inner2Frame = ctk.CTkFrame(innerFrame, fg_color=b_bijela, corner_radius=20)
        inner2Frame.rowconfigure(0, weight=1)
        inner2Frame.columnconfigure(0, weight=1)
        inner2Frame.columnconfigure(1, weight=1)
        inner2Frame.grid(row=3, column=0, sticky="nsew")



        # Register Label
        registerLabel = ctk.CTkLabel(inner2Frame, text="Registriraj se", text_color=b_tekst, 
                                     cursor="hand2", font=("", 15))
        registerLabel.grid(row=0, column=0, sticky="nsew", pady=20, padx=40)
        registerLabel.bind("<Button-1>", lambda e: self.registracija(self.usernameEntry.get(), self.passwordEntry.get()))

        # Login Button
        loginLabel = ctk.CTkLabel(inner2Frame, text="Prijavi se", font=("", 15, "bold"),
                                    height=40, width=60, fg_color=b_plava1, cursor="hand2", 
                                    corner_radius=15)
        loginLabel.grid(row=0, column=1, sticky="nsew", pady=20, padx=35)
        loginLabel.bind("<Button-1>", lambda e: self.prijava(self.usernameEntry.get(), self.passwordEntry.get()))

    def configureUsernamePasswordInput(self: Self, *args, **kwargs):
        self.after(0, self.usernameEntry.configure(*args, **kwargs))
        self.after(0, self.passwordEntry.configure(*args, **kwargs))

    def passwordRestrictionsSat(self: Self, password: str) -> bool:
        return True
        if len(password)<8 or len(password)>40: return False
        containsUpper, containsLower, containsSpecial, cointainsNumber = False, False, False, False
        allLetters = "qwertzuiopšđžćčlkjhgfdsayxcvbnm"
        allLettersU = allLetters.upper()
        for c in password:
            if cointainsNumber or c in "1234567890":
                cointainsNumber = True
            if containsUpper or c in allLettersU:
                containsUpper = True
            if containsLower or c in allLetters:
                containsLower = True
            if containsSpecial or c in "!?,;.-+*/_<>~#$%&()=@[]{}$€|\\":
                containsSpecial = True
            if containsLower and containsSpecial and containsUpper and cointainsNumber:
                return True
        return False

    def prijava(self: Self, username, password):
        #zadovoljava uvjete za lozinku
        if not self.passwordRestrictionsSat(password):
            return
        app: Aplikacija = self.master.master#type: ignore
        app.prijava(username, password)

    def registracija(self: Self, username, password):
        #zadovoljava uvjete za lozinku
        if not self.passwordRestrictionsSat(password):
            return
        app: Aplikacija = self.master.master#type: ignore
        app.registracija(username, password)



"""
Glavna aplikacija, nasljeduje klasu glavne aplikacije iz custom tkintera

U pocetku su vidljivi OdabirRazgovora i Razgovor (gore napravljene klase)
Ak se odabere/napravi razgovor, OdabirRazgovora se zatvori(ostaje gumb kojim se opet otvara)
"""
class Aplikacija(ctk.CTk):
    def __init__(self: Self, *args, **kwargs):#*args i **kwargs u slucaju da ih custom tkinter koristi sa strane (bez da znamo)
        super().__init__(*args, **kwargs)#custom tkinter postavi sam sebe

        self.login = None
        self.odabirRazgovora = None
        self.razgovor = None

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.mainFrame = ctk.CTkFrame(self)

        self.title("WhatsApp")
        self.resizable(True, True)
        self.minsize(800, 600)

    def resetMainFrame(self: Self, *args, **kwargs):
        self.mainFrame: ctk.CTkFrame
        
        self.login: Optional[Login] = None
        self.odabirRazgovora: Optional[OdabirRazgovora] = None
        self.razgovor: Optional[Razgovor] = None

        self.mainFrame.destroy()
        self.mainFrame = ctk.CTkFrame(master=self, *args, **kwargs)
        self.mainFrame.grid(row=0, column=0, sticky="nsew")
    
    def checkLoggedIn(self: Self):
        return False #npr session token

    def initLoginOrChat(self: Self):
        if not self.checkLoggedIn():
            self.initLogin()
        
        else:
            self.initChat()

    def successfulLoginCallback(self: Self):
        self.login = None
        self.initChat()

    def successfulConnectCallback(self: Self):
        self.queue = asyncio.Queue()
        self.initLoginOrChat()
        asyncio.run_coroutine_threadsafe(self.readFromServer(self.reader), self.loop)
        asyncio.run_coroutine_threadsafe(self.write2Server(self.writer, self.queue), self.loop)

    async def aConnect(self: Self):
        if hasattr(self, "baza"):
            self.baza.conn.close()
        else:
            self.baza = Baza(__file__)
            self.baza.conn.close()
        
        print("baza izbrisana")
        del self.baza
        
        retryingT = ["Retrying", "Retrying.", "Retrying..", "Retrying..."]
        i=0
        while True:
            try:
                ReWr = await asyncio.wait_for(asyncio.open_connection(self.ip, self.port), timeout=0.5)
                break
            except (OSError, asyncio.TimeoutError):
                self.after(0, lambda:self.text2.configure(True, text=retryingT[i]))
                i = (i+1)%len(retryingT)

        self.reader, self.writer = ReWr

        self.baza = Baza(__file__)
        
        self.after(0, self.successfulConnectCallback)

    async def readFromServer(self: Self, reader: asyncio.StreamReader):
        while True:
            parser = RequestParser()
            data = await reader.readline()
            if not data:
                break
            parser.append(data)
            print(f"Primljeno: {data.decode()}", end="")
            serverRequest = parser.parse()
            #print(serverRequest)
            if serverRequest["command"] == "signIn" or serverRequest["command"] == "register":
                if serverRequest["success"]:
                    print("uspjesna prijava")
                    self.username = serverRequest["username"]
                    self.after(0, self.successfulLoginCallback)
                else:
                    assert type(self.login) is Login, "login nije inicijaliziran"
                    self.login.configureUsernamePasswordInput(border_color="red")

            elif serverRequest["command"] == "user":
                if not self.baza.checkUserExists(serverRequest["user"]):
                    self.after(0, lambda: self.odabirRazgovora.addRazgovor(serverRequest["user"]))
                    self.baza.cur.execute(
                        """
                        INSERT INTO Korisnici(korisnickoIme)
                        VALUES (?)
                        """, (serverRequest["user"],)
                    )
                    self.baza.conn.commit()
                    
                    

        self.after(0, self.disconnected)

    async def write2Server(self: Self, writer: asyncio.StreamWriter, queue: asyncio.Queue):
        while True:
            data = await queue.get() # messages
            if data == None:
                print("Server writer stopped")
                break
            writer.write(data + b'\n')
            await writer.drain()

    def networkingLoop(self: Self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def disconnected(self: Self):
        self.resetMainFrame()
        asyncio.run_coroutine_threadsafe(self.aConnect(), self.loop)

    def initConnectionUI(self: Self):
        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.columnconfigure(1, weight=1)
        self.mainFrame.columnconfigure(2, weight=1)
        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.rowconfigure(1, weight=1)
        self.mainFrame.rowconfigure(2, weight=1)

        
        #pocistiti memoriju
        gc.collect()

        frame = ctk.CTkFrame(self.mainFrame, fg_color=b_siva, height=350, width=300, corner_radius=20)

        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)
        

        frame.grid(row=1, column=1, sticky="nsew")

        self.text1 = ctk.CTkLabel(frame, text="Connection FAILED", font=("Arial", 30))
        self.text1.grid(row=0, column=0)

        self.text2 = ctk.CTkLabel(frame, text="", font=("Arial", 30))
        self.text2.grid(row=1, column=0)

    def initConnection(self: Self, ip, port):
        self.resetMainFrame()

        self.ip = ip
        self.port = port

        self.loop = asyncio.new_event_loop()

        self.networkingThread = Thread(target=self.networkingLoop, args=(self.loop,), name="networking", daemon=True)
        self.networkingThread.start()

        self.connectFuture = asyncio.run_coroutine_threadsafe(self.aConnect(), self.loop)
        #self.connectFuture.add_done_callback(lambda future: self.after(0, lambda: self.initLoginOrChat))#future nije koristen jer aConnect ne vraca vrijednost
        
        self.initConnectionUI()

    def initLogin(self: Self):
        self.resetMainFrame()

        #self.mainFrame = ctk.CTkFrame(self)
        #self.mainFrame.grid(row=0, column=0)

        self.mainFrame = Login(self.mainFrame)
        self.mainFrame.grid(row=0, column=0)
        self.config(bg=b_siva)

        self.login = self.mainFrame

    def initChat(self: Self):
        self.resetMainFrame()
        #selfID = baza.cur.execute("SELECT korisnikID FROM Korisnici WHERE korisnickoIme=?", ()).fetchone()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        #glavni frame koji sadrzava 2 podframea
        self.mainFrame=ctk.CTkFrame(master=self, corner_radius=0)
        self.mainFrame.grid(row=0, column=0, sticky="nsew")

        #odvojeni prikaz popisa razgovora i aktivnog razgovora
        self.mainFrame.columnconfigure(0, weight=1, uniform="column")
        self.mainFrame.columnconfigure(1, weight=3, uniform="column")
        
        #self.mainFrame.rowconfigure(0, weight=1) #doesnt expand vertically
        self.mainFrame.rowconfigure(1, weight=1)
        
        #lijeva strana, razgovori
        self.chatsLabel=ctk.CTkLabel(self.mainFrame, text="Razgovori", font=("Arial", 20)) 
        self.chatsLabel.grid(row=0, column=0, pady=10, sticky="new")
        self.odabirRazgovora = OdabirRazgovora(self.mainFrame, fg_color=b_plava1)
        self.odabirRazgovora.grid(row=1, column=0, sticky="nsew")

        #desna strana, ime razgovora, poruke i slanje
        self.imeRazgovora=ctk.CTkLabel(self.mainFrame, text="", font=("Arial", 20))
        self.imeRazgovora.grid(row=0, column=1, sticky="nsew")
        self.razgovor = Razgovor(self.mainFrame)
        self.razgovor.grid(row=1, column=1, sticky="nsew")


    def button_callback(self: Self):
        print("button pressed")

    def otvorirazgovor(self: Self):
        pass

    def slanje(self: Self, poruka):
        if poruka == "": return
        poruka = str({"command": "message", 
                      "sender": "a", 
                      "receiver": "b", 
                      "message": poruka
                      })
        asyncio.run_coroutine_threadsafe(self.queue.put(poruka.encode()), self.loop)

    def registracija(self: Self, username, password):
        poruka = str({"command": "register", 
                      "username": username, 
                      "passwordPlaintext": password
                      })
        asyncio.run_coroutine_threadsafe(self.queue.put(poruka.encode()), self.loop)

    def prijava(self: Self, username, password):
        poruka = str({"command": "signIn", 
                      "username": username, 
                      "passwordPlaintext": password
                      })
        asyncio.run_coroutine_threadsafe(self.queue.put(poruka.encode()), self.loop)

    def on_close(self: Self):
        self.destroy()

    def run(self: Self):
        """Starts the event loop manually."""
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Close button handling
        self.mainloop()

class DSA:
    def __init__(self: Self):
        self.p, self.q, self.g = self.parameter_generation()
        self.x, self.y = self.per_user_key()

    def is_prime(self: Self, n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def get_prime(self: Self, bits):
        while True:
            num = random.getrandbits(bits) | 1  # Ensure it's an odd number
            if self.is_prime(num):
                return num

    def hash_function(self: Self, message):
        return sha1(message.encode("UTF-8")).hexdigest()

    def hash_function1(self: Self, file_path):
        name=os.path.basename(file_path)
        with open(name,"r") as file:
            text=file.read()
        return self.hash_function(text)

    def mod_inverse(self: Self, a, m):
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return 1

    def parameter_generation(self: Self):
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

    def per_user_key(self: Self):
        x = random.randint(1, self.q - 1)
        y = pow(self.g, x, self.p)%self.p
        return x, y

    def sign(self: Self, file_path):
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

    def verify(self: Self, file_path, r, s):
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

# # Example usage:
# dsa = DSA()
# file_path = input("Put: ") #rC:\Users\DOMINIK-LPT\Desktop\Tujesjedio.txt 
# signature = dsa.sign(file_path)
# print("Signature (r, s, k):", signature)
# hash1=dsa.hash_function1(file_path)
# print("Hash: ",hash1)
# print()

# file_path = input("Put: ")
# print(dsa.verify(file_path, signature[0], signature[1])) #True ako je valjan False ako nije
try:
    if __name__ == "__main__":
        #ili input
        whatsApp=Aplikacija()
        whatsApp.initConnection("127.0.0.1", 9999)
        whatsApp.mainloop()
        whatsApp.networkingThread.join()
except Exception as e:
    print("Error:", e)  # Basic message
    traceback.print_exc()
