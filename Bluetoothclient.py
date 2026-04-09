import socket
import threading
import curses
from cifer import encode, decode
messages = []

def receive(sock, key, win_messages, lock):
    while True:
        try:
            raw_len = sock.recv(4)
            if not raw_len:
                break
            msg_len = int.from_bytes(raw_len, 'big')
            data = b""
            while len(data) < msg_len:
                chunk = sock.recv(msg_len - len(data))
                if not chunk:
                    break
                data += chunk
            msg = data.decode()
            if msg.startswith("["):
                msg = decode(msg, key)
            with lock:
                messages.append(msg.strip())
                redraw_messages(win_messages)
        except Exception as e:
            with lock:
                messages.append(f"[ERROR] {e}")
                redraw_messages(win_messages)
            break

def redraw_messages(win):
    win.clear()
    h, w = win.getmaxyx()
    visible = messages[-(h):]
    for i, msg in enumerate(visible):
        win.addstr(i, 0, msg[:w-1])
    win.refresh()

def main(stdscr):
    curses.curs_set(1)
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    win_messages = curses.newwin(h - 2, w, 0, 0)
    win_input = curses.newwin(1, w, h - 1, 0)

    stdscr.addstr(h - 2, 0, "-" * w)
    stdscr.refresh()

    lock = threading.Lock()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 5555))

    while True:
        win_input.clear()
        win_input.addstr(0, 0, "Username: ")
        win_input.refresh()
        username = win_input.getstr().decode()
        sock.send(username.encode())
        response = sock.recv(1024).decode()
        if response == "OK":
            messages.append(f"[+] Connected as {username}")
            redraw_messages(win_messages)
            break
        else:
            messages.append("[!] Username taken, try another")
            redraw_messages(win_messages)

    win_input.clear()
    win_input.addstr(0, 0, "Key: ")
    win_input.refresh()
    key = win_input.getstr().decode()[:8]
    curses.noecho()

    thread = threading.Thread(target=receive, args=(sock, key, win_messages, lock))
    thread.daemon = True
    thread.start()

    while True:
        win_input.clear()
        win_input.addstr(0, 0, "> ")
        win_input.refresh()
        curses.echo()
        msg = win_input.getstr().decode()
        curses.noecho()
        if msg.lower() == "quit":
            break
        data = encode(f"[{username}]: {msg}", key).encode()
        sock.send(len(data).to_bytes(4, 'big') + data)
        with lock:
            messages.append(f"[{username}]: {msg}")
            redraw_messages(win_messages)

    sock.close()

curses.wrapper(main)