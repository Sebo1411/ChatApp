#za cuvanje poruka na serveru(enkriptirano, bez dekripcije) i klijentu(enkriptirano, s dekripcijom)
import enum
import sqlite3
import os
from typing import Self
import secrets
import hashlib

stvoriPoruke =  """
                CREATE TABLE Poruke(
                    porukaID INTEGER PRIMARY KEY AUTOINCREMENT,
                    posiljateljID INTEGER NOT NULL,
                    ime VARCHAR(30) NOT NULL,
                    vrijeme DATETIME DEFAULT CURRENT_TIMESTAMP,
                    encInfo TEXT NOT NULL,
                    encPoruka BLOB,                                 -- datoteka ak NULL
                    FOREIGN KEY (posiljateljID) REFERENCES Korisnici(korisnikID) ON DELETE CASCADE
                    )
                """


stvoriKorisnikeServer = """
                        CREATE TABLE Korisnici(
                        korisnikID INTEGER PRIMARY KEY AUTOINCREMENT,
                        korisnickoIme VARCHAR(30) NOT NULL UNIQUE,
                        passSalt BLOB NOT NULL,
                        passHash BLOB NOT NULL,
                        datumPridruzivanja DATE DEFAULT CURRENT_TIMESTAMP,
                        uloga TEXT DEFAULT "user"
                        );
                        """

stvoriKorisnikeClient = """
                        CREATE TABLE Korisnici(
                        korisnikID INTEGER PRIMARY KEY AUTOINCREMENT,
                        korisnickoIme VARCHAR(30) NOT NULL UNIQUE,
                        uloga TEXT DEFAULT "user"
                        );
                        """


stvoriDatoteke =    """
                    CREATE TABLE Datoteke(
                        datotekaID INTEGER PRIMARY KEY AUTOINCREMENT, 
                        porukaID INTEGER NOT NULL,                              
                        filePath TEXT NOT NULL,                                 
                        fileType VARCHAR(30),                          
                        fileSize INTEGER,                              
                        FOREIGN KEY (porukaID) REFERENCES Poruke(porukaID) ON DELETE CASCADE
                        );
                    """

class Baza:
    def __init__(self: Self, file: str):
        noviF = os.path.splitext(os.path.basename(file))
        imeDatoteke = "".join(noviF[:len(noviF) - 1])
        folder = os.path.join(os.path.abspath(os.curdir), imeDatoteke)

        if not os.path.isdir(folder):
            os.makedirs(folder)
        
        dbPath = os.path.join(folder, 'podatci.db')
        
        self.conn: sqlite3.Connection = sqlite3.connect(dbPath)
        self.cur: sqlite3.Cursor = self.conn.cursor()

        self.checkCreateTable("Poruke", stvoriPoruke)

        if imeDatoteke == "server":
            self.checkCreateTable("Korisnici", stvoriKorisnikeServer)
        elif imeDatoteke == "client":
            self.checkCreateTable("Korisnici", stvoriKorisnikeClient)
        
        self.checkCreateTable("Datoteke", stvoriDatoteke)
    
    """
    Stvara table u bazi s tom naredbom,
    Naredba treba ukljucivati i "CREATE TABLE"   
    """
    def checkCreateTable(self, name: str, command: str) -> sqlite3.Cursor:
        self.cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}';")
        if (len(self.cur.fetchall()) == 0):
            return self.cur.execute(command)
        else:
            return self.cur
        
    def checkUserExists(self: Self, username: str):
        self.cur.execute(f"""
                            SELECT * FROM Korisnici WHERE korisnickoIme = ?
                          """, (username, ))
        return len(self.cur.fetchone()) != 0
            

    def createUser(self: Self, username: str, loznikaPlaintext: bytes) -> bool:
        if not self.checkUserExists(username): 
            return False
        
        salt = secrets.token_bytes(16)

        self.cur.execute(f"""
                            INSERT INTO Korisnici (korisnickoIme, passSalt, passHash) ; mozda jos uloga
                            VALUES (?, ?, ?)
                            ; n - cost factor, r - block size, p - paralelizacija
                         """, (username, salt, hashlib.scrypt(loznikaPlaintext, salt = salt, n = 16384, r = 8, p = 1)))
        
        return True


    








