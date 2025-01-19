from baza import Baza
from typing import Self
from socket import socket
import threading
import socketserver
import ssl

baza = Baza(__file__)

class RequestHandler(socketserver.BaseRequestHandler):
    def __init__(self: Self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #def setup(self: Self) -> None: #prije handle()

    """
    zahtjev je dostupan ko self.request (socket za TCP)
    adresa klijenta ko self.client_address
    instanca servera ko self.server
    """
    def handle(self: Self) -> None:
        conn: socket = self.request #naslijedeno iz socketserver.BaseRequestHandler
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

    #def finish(self: Self) -> None: #poslje handle(), ne zove se ak setup digne Exception

class Server(socketserver.ThreadingTCPServer):
    def __init__(self: Self, hostnameOrIp: str, port: int):
        super().__init__((hostnameOrIp, port), RequestHandler)
        self.baza = Baza(__file__)

    def notify_clients_when_server_is_interrupted(self) -> None:
        pass

    def get_request(self: Self):
        print("Pozvan get_request")
        return super().get_request()
    
    def verify_request(self: Self, request, client_address):
        print("Pozvan verify_request")
        return super().verify_request(request, client_address)
    
    def process_request(self: Self, request, client_address):
        print("Pozvan process_request")
        return super().process_request(request, client_address)
    



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
