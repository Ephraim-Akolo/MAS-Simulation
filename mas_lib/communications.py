import socket
from threading import Thread


class ComBase:

    def __init__(self, name, host = socket.gethostname(), port = 10001 ) -> None:
        server_socket = socket.socket()  # instantiate
        server_socket.connect((host, port))  # connect to the server
        self._server_socket = server_socket
        self.name = name
        Thread(name=name, target=self._recieve_broadcast, daemon=True).start()
    
    def broadcast_message(self, message:str):
        return self._server_socket.send((self.name+":"+message).encode())  # send message

    def _recieve_broadcast(self):
        data, msg, name, = "", "", ""
        while data.lower().strip() != 'bye':
            data = self._server_socket.recv(1024).decode()  # receive response
            if not data:
                self._server_socket.close() 
                raise(ConnectionError("Broken Pipeline!"))
            name, msg = data.strip().split(":")
            if name == self.name:
                continue
            self.broadcast(name, msg)

    def broadcast(self, name, state): # Override function
        print(name, state)


if __name__ == "__main__":
    ComBase("agent1")
    b = ComBase("agent2")
    a = ComBase("agent3")
    a.broadcast_message("hi to me")
    input()
    
