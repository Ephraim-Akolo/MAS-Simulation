import socket
from threading import Thread
from os import name as _OS_Name_
if _OS_Name_ == 'nt':
    from os import environ
    environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy import require
require("2.1.0")
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty


class AppUI(Label):

    myinfo = (
        "MAS Server Running!",
        "Agents in network: {}"
    )

    connections = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgb=(1, 1, 1))
            self.background = Rectangle(pos=self.pos, size=self.size)
        self.display_info(0)
        self.color= "green" 
        self.font_size="30"
        self.halign = "center"
        self.valign = "center"

    def on_connections(self, obj, num):
        num = num if num <= 0 else num-1
        self.display_info(num)
    
    def display_info(self, num:int):
        self.text = f"{self.myinfo[0]}\n\n{self.myinfo[1].format(num)}" 
    
    def on_size(self, obj, size):
        self.background.size = size
        self.text_size = size

    def on_pos(self, obj, pos):
        self.background.pos = pos
    
    def added_connection(self):
        self.connections += 1
    
    def lost_connection(self):
        self.connections -= 1


class ServerApp(App):

    CONNECTIONS = {}

    def build(self):
        host = socket.gethostname()
        port = 10001  # initiate port no above 1024

        self.server_socket = socket.socket()  # get instance
        self.server_socket.bind((host, port))  # bind host address and port together

        # configure how many client the server can listen simultaneously
        self.server_socket.listen(10)
        return AppUI()

    def on_start(self):
        Thread(name="accept_connections", target=self.accept_connections, daemon=True).start()
        return super().on_start()

    def accept_connections(self):
        i = 1
        while True:
            conn, address = self.server_socket.accept()  # accept new connection
            Thread(name=f"agent_{i}_{address}", target=self.create_agent_thread, args=(conn, address), daemon=True).start()
            if address[0] in self.CONNECTIONS.keys():
                self.CONNECTIONS[address[0]].append(conn)
            else:
                self.CONNECTIONS[address[0]] = [conn]
            Clock.schedule_once(lambda x: self.root.added_connection())


    def create_agent_thread(self, conn, address):
        print("Connection from: " + str(address[0]))
        try:
            while True:
                try:
                    data = None
                    data = conn.recv(32).decode()
                except:
                    pass
                if not data:
                    if len(self.CONNECTIONS[address[0]]) <= 1:
                        self.CONNECTIONS.pop(address[0])
                    else:
                        self.CONNECTIONS[address[0]].remove(conn)
                    Clock.schedule_once(lambda x: self.root.lost_connection())
                    break
                n = sum([len(val) for val in self.CONNECTIONS.values()])
                print("from " + str(data).strip().strip(":"), f" *(broadcasting to {n-1} out of {n} self.connections in network!)")
                if len(data) != 32:
                    raise(Exception("Invalid Message Size!!!"))
                for addr, connection in self.CONNECTIONS.items():
                    for c in connection:
                        if c == conn:
                            continue
                        try:
                            c.send(data.encode())
                        except:
                            print("failed to send to connection:", c)
                            self.CONNECTIONS[addr].remove(c)
                            Clock.schedule_once(lambda x: self.root.lost_connection())
                            if len(self.CONNECTIONS[addr]) < 1:
                                self.CONNECTIONS.pop(addr)
        finally:
            conn.close()


if __name__ == '__main__':
    ServerApp().run()
    