from baza import Baza
from typing import Self, Any
import socket
import threading
import socketserver
import ssl
import ast

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

    def addData(self: Self, data: bytes):
        self.data.append(data)
    
    def parse(self: Self) -> dict[str, Any]:
        return ast.literal_eval("".join(data.decode("utf-8") for data in self.data)) #ocekuje dict, dekodira, spaja u jedan string i pretvara u dict

"""
Zahtjevi:
  Kreiranje racuna/prijava:
    provjeriti dal korisnik vec postoji
    provjeriti dal lozinka zadovoljava minimalne uvjete
    hash, pepper, salt (bcrypt?) -> provjera s bazom
"""
class RequestHandler(socketserver.BaseRequestHandler):
    def __init__(self: Self, baza, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.baza = baza

    def setup(self: Self) -> None: #prije handle()
        print("setup pozvan")
        if hasattr(socket, "SO_KEEPALIVE"):
            self.request.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  #TCP keep-alive
        if hasattr(socket, "TCP_QUICACK"): #nema
            #self.socket.setsockopt(socket.SOL_TCP, socket.TCP_QUICACK, 1)
            pass
        if hasattr(socket, "IP_TOS"):
            self.request.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, 0x10)  #low latency
        if hasattr(socket, "TCP_NODELAY"):
            self.request.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) 
        

    """
    zahtjev je dostupan ko self.request (socket za TCP)
    adresa klijenta ko self.client_address
    instanca servera ko self.server
    """
    def handle(self: Self) -> None:
        print("pozvan handle")
        conn: socket.socket = self.request #naslijedeno iz socketserver.BaseRequestHandler

        parser = RequestParser()

        while True:
            data = conn.recv(1024)
            if not data:
                break
            parser.addData(data)
        
        clientRequest = parser.parse()

        value = clientRequest.get("command")
        if value == "createUser":
            self.baza.createUser(clientRequest["username"], clientRequest["passwordPlaintext"])

            

    #def finish(self: Self) -> None: #poslje handle(), ne zove se ak setup(self) digne Exception

class Server(socketserver.ThreadingTCPServer):
    def __init__(self: Self, hostnameOrIp: str, port: int):
        super().__init__((hostnameOrIp, port), RequestHandler)
        self.baza = Baza(__file__)

    def notify_clients_when_server_is_interrupted(self) -> None:
        pass

    def server_bind(self: Self):
        print("server_bind pozvan")

        #default implementacija
        if self.allow_reuse_address and hasattr(socket, "SO_REUSEADDR"):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.allow_reuse_port and hasattr(socket, "SO_REUSEPORT"): #socket nema SO_REUSEPORT u windowsu
            #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) 
            pass
        
        #socket razina, drzi socket otvorenim, ukljuci opciju
        

        #default
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

    def get_request(self: Self):
        print("Pozvan get_request")
        #return self.socket.accept() #default implementacija
        return super().get_request()
    
    def verify_request(self: Self, request, client_address):
        print("Pozvan verify_request")
        return super().verify_request(request, client_address)
    
    def process_request(self: Self, request, client_address):
        print("Pozvan process_request")
        return super().process_request(request, client_address)
    
    #def server_close(self: Self): #cleanup: odspoji sve klijente
    



if __name__ == "__main__":
    server = Server("127.0.0.1", 9999)
    with server:
        ip, port = server.server_address
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        #server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server.serve_forever()
        #server.shutdown()
