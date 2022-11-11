import socket
from threading import Thread
from time import sleep


class ComBase:

    def __init__(self, name, host="", port = 10001 ) -> None:
        self._server_socket = socket.socket()  # instantiate
        self.name = name
        if host == "":
            self.host = socket.gethostname()
        else:
            self.host = host
        self.port = port
        if not self._connect_to_network():
            raise(Exception("Failed to connect!"))
    
    def _connect_to_network(self) -> bool:
        try:
            self._server_socket.connect((self.host, self.port))  # connect to the server
            Thread(name=self.name, target=self._recieve_broadcast, daemon=True).start()
        except:
            print("Connect to network failed!!!")
            return False
        return True
    
    def broadcast_message(self, message:str):
        message = self.name + ":" + message
        message = message + (" "*(32-len(message)))
        if len(message) != 32:
            raise(Exception("Invalid Message Size!!!"))
        return self._server_socket.send(message.encode())  # send message

    def _recieve_broadcast(self):
        data, name_msg = "", ""
        while data.lower().strip() != 'bye':
            data = self._server_socket.recv(32).decode()  # receive response
            if not data:
                self._server_socket.close() 
                raise(ConnectionError("Broken Pipeline!"))
            name_msg = data.strip().split(":") # Had issues with two commands concatenated together or ovalaping
            if len(name_msg) > 2:
                print("ERROR PARSING COMMAND:", name_msg)
                continue
            if name_msg[0] == self.name:
                continue  
            self.broadcast(*name_msg)

    def broadcast(self, name:str, state:str): # Override function
        raise(NotImplementedError("broadcast must be overwritten"))
    
    def schedule_attr_broadcast(self, attr:str, interval:int) -> bool:
        try:
            Thread(name=attr, target=self._attr_broadcast, args=(attr, interval), daemon=True).start()
        except:
            raise(Exception("Failed to schedule {attr} broadcast!"))
        return True
    
    def _attr_broadcast(self, attr, interval):
        while True:
            if callable(self._callback):
                self._callback(getattr(self, "name"), getattr(self, attr))
            self.broadcast_message(str(getattr(self, attr)))
            sleep(interval)
    
    @staticmethod
    def its_B(name:str) -> int|None:
        if len(name) > 1 and name[0] == "B" and name[1:].isnumeric():
            return int(name[1:])
    
    @staticmethod
    def its_DG(name:str) -> int|None:
        if len(name) > 2 and name[:2] == "DG" and name[2:].isnumeric():
            return int(name[2:])
    
    @staticmethod
    def its_CB(name:str) -> int|None:
        if len(name) > 2 and name[:2] == "CB" and name[2:-1].isnumeric():
            return int(name[2:-1])
    
    @staticmethod
    def its_SOURCE(name:str) -> int|None:
        if len(name) > 6 and name[:6] == "SOURCE" and name[6:-1].isnumeric():
            return int(name[6:-1])

if __name__ == "__main__":
    ComBase("agent1")
    b = ComBase("agent2")
    a = ComBase("agent3")
    # a.broadcast_message("hi to me")
    # a.state = 1000
    # a.schedule_attr_broadcast('state', 1)
    # b.state = "hey all"
    # b.schedule_attr_broadcast('state', 1)
    input()
    
