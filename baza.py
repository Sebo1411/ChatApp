#za cuvanje poruka na serveru(enkriptirano, bez dekripcije) i klijentu(enkriptirano, s dekripcijom)
import sqlite3
import os

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


stvoriKorisnike =   """
                    CREATE TABLE Korisnici(
                        korisnikID INTEGER PRIMARY KEY AUTOINCREMENT,
                        korisnickoIme VARCHAR(30) NOT NULL UNIQUE,
                        passHash TEXT NOT NULL,
                        datumPridruzivanja DATE DEFAULT CURRENT_TIMESTAMP,
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
    def __init__(self, file):
        noviF = os.path.splitext(os.path.basename(file))
        folder = os.path.join(os.path.abspath(os.curdir), "".join(noviF[:len(noviF) - 1]))

        if not os.path.isdir(folder):
            os.makedirs(folder)
        
        dbPath = os.path.join(folder, 'podatci.db')
        
        self.conn: sqlite3.Connection = sqlite3.connect(dbPath)
        self.cur: sqlite3.Cursor = self.conn.cursor()

        self.checkCreateTable("Poruke", stvoriPoruke)
        self.checkCreateTable("Korisnici", stvoriKorisnike)
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

    








