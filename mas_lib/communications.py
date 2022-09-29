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
        while not self._connect_to_network():
           print(name, " failed to connect!!!")
           sleep(5)
    
    def _connect_to_network(self) -> bool:
        try:
            self._server_socket.connect((self.host, self.port))  # connect to the server
            Thread(name=self.name, target=self._recieve_broadcast, daemon=True).start()
        except:
            print("Connect to network failed!!!")
            return False
        return True
    
    def broadcast_message(self, message:str):
        return self._server_socket.send((":"+self.name+":"+message+":").encode())  # send message

    def _recieve_broadcast(self):
        data, name_msg = "", ""
        while data.lower().strip() != 'bye':
            data = self._server_socket.recv(1024).decode()  # receive response
            if not data:
                self._server_socket.close() 
                raise(ConnectionError("Broken Pipeline!"))
            name_msg = data.strip(":").split(":") # Had issues with two commands concatenated together or ovalaping
            if (l:=len(name_msg)) % 2:
                print("ERROR PARSING COMMAND:", name_msg)
                continue
            if name_msg[0] == self.name:
                continue
            for i in range(0, l, 2):    
                self.broadcast(*name_msg[i:i+2])

    def broadcast(self, name:str, state:str): # Override function
        print(name, state)
    

    def schedule_attr_broadcast(self, attr:str, interval:int) -> bool:
        try:
            Thread(name=attr, target=self._attr_broadcast, args=(attr, interval), daemon=True).start()
        except:
            print(f"Failed to schedule {attr} broadcast!")
            return False
        return True
    
    def _attr_broadcast(self, attr, interval):
        while True:
            try:
                self.broadcast_message(str(getattr(self, attr)))
            except:
                while not self._connect_to_network():
                    sleep(5)
            sleep(interval)


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
    
