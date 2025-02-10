from baza import Baza
from typing import Self, Any
import socket
import threading
import socketserver
import ssl
import ast
import asyncio

baza = Baza(__file__)

"""
prijenos parametara tj. naredbi s clienta do servera:
    https -> siroko podrzano, komplicirano, skupo
    json -> svi kovertirani tipovi u json-u su stringovi tak da json.loads(json.dumps(x)) != x # ne moraju biti isti tip
    ast (abstract syntax tree) -> ast.literal_eval: sigurnije nego eval, ali ograniceno u tipovima koje podrzava, moze potrositi stack i srusiti program
    pickle -> podrzava sve tipove za serializaciju, ali omogucuje pokretanje neodredenog koda(sigurnosni propust) -> dill prosiruje
    protocol buffers -> siroko podrzano, radi s (skoro) svim jezicima, komplicirano
"""

class RequestParser:
    def __init__(self: Self):
        self.data: list[bytes] = []

    def append(self: Self, data: bytes):
        self.data.append(data)
    
    def parse(self: Self) -> dict[str, Any]:
        return ast.literal_eval("".join(data.decode() for data in self.data)) #ocekuje dict, dekodira, spaja u jedan string i pretvara u dict
    
    def isEmpty(self: Self):
        return len(self.data) == 0

"""
Zahtjevi:
  Kreiranje racuna/prijava:
    provjeriti dal korisnik vec postoji
    provjeriti dal lozinka zadovoljava minimalne uvjete
    hash, pepper, salt (bcrypt?) -> provjera s bazom
""" 
class Server:
    def __init__(self: Self):
        self.clients: dict[str, asyncio.StreamWriter] = dict()

    async def run(self: Self):
        server = await asyncio.start_server(self.handle, '127.0.0.1', 9999)

        async with server:
            await server.serve_forever()

    async def handle(self: Self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        while True:
            parser = RequestParser()
            data = await reader.readline()
            if not data:
                break
            parser.append(data)

            if not parser.isEmpty():
                clientRequest = parser.parse()

                print(clientRequest)

                command = clientRequest.get("command")
                if command == "message":
                    success = baza.storeMessage(clientRequest["sender"], clientRequest["receiver"], clientRequest["message"])
                    response = str({"success": success, "message": ""})
                    writer.write(response.encode())
                    await writer.drain()
                elif command == "register":
                    success = baza.createUser(clientRequest["username"], clientRequest["passwordPlaintext"])
                    response = str({"success": success, "message": "", "token": 0x01, "expiresIn": 3600})

                    if success: self.clients[clientRequest["username"]] = writer

                    writer.write(response.encode())
                    await writer.drain()
                elif command == "signIn":
                    success = baza.verifyCreds(clientRequest["username"], clientRequest["passwordPlaintext"])
                    self.clients[clientRequest["username"]] = writer
                    pass
                
                else:
                    print(f"unknown command: {command}")
                    writer.close()
                    await writer.wait_closed()
                    return
        
        #writer.write(data)
        #await writer.drain()

        


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.run())

    """
    server = Server("127.0.0.1", 9999)
    with server:
        ip, port = server.server_address
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        #server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server.serve_forever()
        #server.shutdown()
    """
