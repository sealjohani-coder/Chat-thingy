import socket
import threading
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 5555))
sock.listen(1)
server_address = "XX:XX:XX:XX:XX:XX"
port = 3

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.setblocking(True)
s.connect((server_address, port))

conn, info = sock.accept()

def forward(src, dst):
    while True:
        try:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
        except:
            break

t1 = threading.Thread(target=forward, args=(conn, s))
t2 = threading.Thread(target=forward, args=(s, conn))
t1.daemon = True
t2.daemon = True
t1.start()
t2.start()
t1.join()
t2.join()
