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
                    primateljID INTEGER NOT NULL,
                    vrijeme DATETIME DEFAULT CURRENT_TIMESTAMP,
                    encInfo TEXT NOT NULL,
                    encPoruka BLOB,                                 -- datoteka ak NULL
                    FOREIGN KEY (posiljateljID) REFERENCES Korisnici(korisnikID) ON DELETE CASCADE,
                    FOREIGN KEY (primateljID) REFERENCES Korisnici(korisnikID) ON DELETE CASCADE
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
        
        self.dbPath = os.path.join(folder, 'podatci.db')
        
        self.conn: sqlite3.Connection = sqlite3.connect(self.dbPath)

        self.conn.execute("PRAGMA foreign_keys = ON;")  # Enforce foreign key constraints (optional)
        self.conn.execute("PRAGMA journal_mode = WAL;")  # Optional, for improved logging in WAL mode
        self.conn.execute("PRAGMA synchronous = FULL;")  # Ensures SQLite writes are fully committed

        # Enable SQLite to raise exceptions on errors:
        self.conn.row_factory = sqlite3.Row

        self.cur: sqlite3.Cursor = self.conn.cursor()

        print(f"baza: {self.dbPath}")

        self.checkCreateTable("Poruke", stvoriPoruke)

        if imeDatoteke == "server":
            self.checkCreateTable("Korisnici", stvoriKorisnikeServer)
        elif imeDatoteke == "client":
            self.checkCreateTable("Korisnici", stvoriKorisnikeClient)
        
        self.checkCreateTable("Datoteke", stvoriDatoteke)
    
    def __delete__(self: Self):
        if os.path.exists(self.dbPath):
            os.remove(self.dbPath)
            print(f"Database {self.dbPath} deleted successfully.")
        else:
            print(f"Database {self.dbPath} file not found.")

    def __del__(self: Self):
        if os.path.exists(self.dbPath):
            os.remove(self.dbPath)
            print(f"Database {self.dbPath} deleted successfully.")
        else:
            print(f"Database {self.dbPath} file not found.")
    
    """
    Stvara table u bazi s tom naredbom,
    Naredba treba ukljucivati i "CREATE TABLE"   
    """
    def checkCreateTable(self, name: str, command: str) -> sqlite3.Cursor:
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (name,))
        if (len(self.cur.fetchall()) == 0):
            return self.cur.execute(command)
        else:
            return self.cur
        
    def checkUserExists(self: Self, username: str):
        result = self.cur.execute("""
                          SELECT COUNT(*) FROM Korisnici WHERE korisnickoIme = ?
                         """, (username, )).fetchone()
        return result != None and result[0] != 0

    def IDfromUsername(self: Self, username):
        result = self.cur.execute(
            """
            SELECT korisnikID FROM Korisnici WHERE korisnickoIme = ?
            """, (username, )
        ).fetchone()

        return result[0] if result else None

    def enc(self: Self, message):
        return message

    def storeMessage(self: Self, sender, receiver, message, time = None):
        sender = self.IDfromUsername(sender)
        receiver = self.IDfromUsername(receiver)
        if sender == None or receiver == None:
            print("no sender or receiver in db")
            return False


        if time == None:
            self.cur.execute(
                """
                INSERT INTO Poruke (posiljateljID, primateljID, encInfo, encPoruka)
                VALUES (?, ?, ?, ?);
                """, (sender, receiver, "sha0", self.enc(message))
            )
        else:
            self.cur.execute(
                """
                INSERT INTO Poruke (posiljateljID, primateljID, vrijeme, encInfo, encPoruka)
                VALUES (?, ?, ?, ?, ?);
                """, (self.IDfromUsername(sender), self.IDfromUsername(receiver), time, "sha0", self.enc(message))
            )
        
        self.conn.commit()
        return True

    def getMessages(self: Self, username):
        if not self.checkUserExists(username):
            print(f"korisnik {username} ne postoji")
            return
        
        result = self.cur.execute(
            """
                SELECT 
                    k1.korisnickoIme AS posiljatelj,
                    k2.korisnickoIme AS primatelj,
                    p.vrijeme,
                    p.encInfo,
                    p.encPoruka
                FROM Poruke p
                JOIN Korisnici k1 ON p.posiljateljID = k1.korisnikID
                JOIN Korisnici k2 ON p.primateljID = k2.korisnikID
                ORDER BY p.vrijeme ASC;
            """
                ).fetchall()
        
        if result is None:
            print("nema poruka")
            return False
        
        yield from result

    def getUsers(self: Self, username):
        if not self.checkUserExists(username):
            print(f"korisnik {username} ne postoji")
            return False
        
        result = self.cur.execute(
            """
                SELECT korisnickoIme FROM Korisnici WHERE korisnickoIme != ?
            """, (username, )
                ).fetchall()
        
        if result is None:
            print("nema poruka")
            return False
        
        for korisnickoIme in result:
            yield korisnickoIme

    def countMessages(self: Self, username):
        if not self.checkUserExists(username):
            print(f"korisnik {username} ne postoji")
            return 0

        result = self.cur.execute(
            """
            SELECT COUNT(*) 
            FROM Poruke 
            WHERE posiljateljID = (SELECT korisnikID FROM Korisnici WHERE korisnickoIme = ?)
            OR primateljID = (SELECT korisnikID FROM Korisnici WHERE korisnickoIme = ?);
            """, (username, username)
        ).fetchone()

        return result[0]


    def verifyCreds(self: Self, username, password):
        if not self.checkUserExists(username):
            print(f"korisnik {username} ne postoji")
            return False
        
        result = self.cur.execute(
            """
            SELECT passSalt, passHash FROM Korisnici WHERE korisnickoIme = ?
            """, (username, )
        ).fetchone()

        if result is None:
            return False

        return result[1] == hashlib.scrypt(password.encode(), salt=result[0], n = 16384, r = 8, p = 1)

    def createUser(self: Self, username: str, loznikaPlaintext: str) -> bool:
        if self.checkUserExists(username): 
            return False
        
        salt = secrets.token_bytes(16)

        self.cur.execute("""
                            INSERT INTO Korisnici (korisnickoIme, passSalt, passHash) -- mozda jos uloga
                            VALUES (?, ?, ?)
                            -- n - cost factor, r - block size, p - paralelizacija
                         """, (username, salt, hashlib.scrypt(loznikaPlaintext.encode(), salt = salt, n = 16384, r = 8, p = 1)))
        
        self.conn.commit()

        return True


    








