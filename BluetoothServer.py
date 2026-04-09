import socket
import threading
MAC = "XX:XX:XX:XX:XX:XX"
port = 3
backlog = 1
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((MAC,port))
s.listen(backlog)


print("[-] No Connection Yet")
conn, info = s.accept()
print(f"[+] Connection Received from {info}")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 9999))
def forward(src, dst):
    while True:
        try:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
        except:
            break

t1 = threading.Thread(target=forward, args=(conn, sock))
t2 = threading.Thread(target=forward, args=(sock, conn))
t1.daemon = True
t2.daemon = True
t1.start()
t2.start()
t1.join()
t2.join()
