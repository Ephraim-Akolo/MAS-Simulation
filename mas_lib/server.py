import socket
from threading import Thread

CONNECTIONS = {}

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 10001  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(10)
    i = 1
    while True:
        conn, address = server_socket.accept()  # accept new connection
        Thread(name=f"agent_{i}_{address}", target=_connect_to_network, args=(conn, address), daemon=True).start()
        if address[0] in CONNECTIONS.keys():
            CONNECTIONS[address[0]].append(conn)
        else:
            CONNECTIONS[address[0]] = [conn]


def _connect_to_network(conn, address):
    print("Connection from: " + str(address[0]))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            if len(CONNECTIONS[address[0]]) <= 1:
                CONNECTIONS.pop(address[0])
            else:
                CONNECTIONS[address[0]].remove(conn)
            break
        n = sum([len(val) for val in CONNECTIONS.values()])
        print("from " + str(data), f" *(broadcasting to {n-1} out of {n} connections in network!)")
        for connection in CONNECTIONS.values():
            for c in connection:
                if c == conn:
                    continue
                try:
                    c.send(data.encode())
                except:
                    print("failed to send to connection:", c)
    conn.close()


if __name__ == '__main__':
    server_program()
    