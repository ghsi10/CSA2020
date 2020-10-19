import socket
import string


def only_upper(bs):
    return ''.join([ch for ch in bs.decode() if ch in string.ascii_uppercase]).encode()


IP = "18.156.68.123"
PORT = 80
WRONG = b"I don't understand you"
MSG = only_upper("""
HELLO FIELD AGENT!
COMMANDS:
    SEND-SECRET-DATA
    GET-SECRET-DATA
    GOODBYE
    """.encode())


sock = socket.socket()
sock.connect((IP, PORT))

sock.recv(1024)
first = sock.recv(1024).split(b'\n')
get = first[4] + b'\n'
_flaga = b""
while True:
    sock.send(get)
    answer = sock.recv(1024)
    encrypted = sock.recv(1024)
    encrypted2 = encrypted.split(b'\n')
    if WRONG not in answer:
        _flaga = answer
        break
print(_flaga)

flaga = only_upper(_flaga)
text = encrypted
for _ in range(30):
    sock.send(b'\n')
    sock.recv(1024)
    data = sock.recv(1024)
    text += (data)
text = only_upper(text)
print(len(text))

flag = ""

for i, ch in enumerate(flaga):
    done = False
    for j in range(17+i, len(text), 26):
        if text[j] == ch:
            relative = j % len(MSG)
            flag += chr(MSG[relative])
            done = True
            break
    if not done:
        flag += '?'
print(flag)
