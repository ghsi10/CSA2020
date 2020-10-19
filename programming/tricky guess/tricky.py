import socket

HOST = "tricky-guess.csa-challenge.com"
PORT = 2222

with open("words.txt", "r") as file:
    words = file.readlines()


def counter_chars(str1, str2):
    counter = 0 
    for char in str1:
        if str2.find(char) >= 0:
            counter += 1
    return counter


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.recv(10240)
s.recv(1024)

while words:
    w = words.pop().replace("\n", "")
    s.send(w.encode())
    msg = s.recv(1024)
    try:
        num = int(msg.decode().replace("\n", ""))
        for j in words:
            if counter_chars(j, w) != num:
                words.remove(j)
    except ValueError:
        print(msg.decode())
s.close()
