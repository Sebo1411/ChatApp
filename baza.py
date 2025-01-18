#za cuvanje poruka na serveru(enkriptirano, bez dekripcije) i klijentu(enkriptirano, s dekripcijom)
import sqlite3

conn: sqlite3.Connection = sqlite3.connect("poruke.db")
cur: sqlite3.Cursor = conn.cursor()

