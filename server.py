import socket
import threading

def handle_client(conn, addr, clients, usernames):
    while True:
        username = conn.recv(1024).decode()
        if not username:
            continue
        if username in usernames.values():
            conn.send("TAKEN".encode())
        else:
            conn.send("OK".encode())
            break

    usernames[conn] = username
    print(f"[+] {username} connected from {addr}")
    broadcast(f"{username} joined the chat\n".encode(), conn, clients, usernames, length_prefix=False)

    while True:
        try:
            raw_len = conn.recv(4)
            if not raw_len:
                break
            msg_len = int.from_bytes(raw_len, 'big')
            msg = b""
            while len(msg) < msg_len:
                chunk = conn.recv(msg_len - len(msg))
                if not chunk:
                    break
                msg += chunk
            broadcast(raw_len + msg, conn, clients, usernames)
        except:
            break

    clients.remove(conn)
    broadcast(f"{username} left the chat\n".encode(), conn, clients, usernames, length_prefix=False)
    conn.close()

def broadcast(msg, sender, clients, usernames, length_prefix=True):
    for client in clients:
        if client != sender:
            try:
                if length_prefix:
                    client.send(msg)
                else:
                    msg_len = len(msg).to_bytes(4, 'big')
                    client.send(msg_len + msg)
            except:
                pass

def main():
    host = "0.0.0.0"
    port = 9999

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[*] Server listening on {host}:{port}")

    clients = []
    usernames = {}

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr, clients, usernames))
        thread.start()

main()