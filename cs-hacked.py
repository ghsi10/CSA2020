from arc4 import ARC4
from scapy.all import *
import socket


def get_flag():
    io = remote('3.126.154.76', 80)
    io.recvuntil('csa-mitm-key')
    flag = str(io.clean(1)).replace("\n", "")
    io.close()
    return flag


def decrypt(chiper):
    arc4 = ARC4('csa-mitm-key')
    return arc4.decrypt(chiper)


def encrypt(plaintext):
    arc4 = ARC4('csa-mitm-key')
    return arc4.encrypt(plaintext)


def decrypt_as_array(cipher, key):
    for element in key:
        cipher = decrypt(cipher, element)
    return cipher


def send_sequence(a, b, c, d, e, f, g, h, i, j):
    io = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    io.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    io.connect(('3.126.154.76', 80))
    io.recv(39)
    shit = io.recv(32)
    d = encrypt(shit + a + b + c + d + e + f + g + h + i + j)
    data = d[len(shit):]
    io.send(data[0:13])
    io.send(data[13:28])
    io.send(data[28:30])
    io.send(data[30:33])
    io.send(data[33:35])
    io.send(data[35:49])
    io.send(data[49:55])
    io.send(data[55:62])
    io.send(data[62:70])
    io.send(data[70:80])
    try:
        rt = io.recv(44) 
        print(decrypt(d+rt).split("\n")[-2])
    except:
        print("**ERROR***")


def send_as_string(seq):
    encrypted = "\n".join([encrypt(x) for x in seq])
    io = remote('3.126.154.76', 80)
    io.clean(0.5)
    io.send(encrypted + "\n")
    try:
        print(io.clean(0.5))
        io.close()
    except:
        pass


def brute_server(A, B, C, D, E, F, G, H, I, J):
    for a in A:
        for b in B:
            for c in C:
                for d in D:
                    for e in E:
                        for f in F:
                            for g in G:
                                for h in H:
                                    for i in I:
                                        for j in J:
                                            data = send_sequence(a, b, c, d, e, f, g, h, i, j)


l2 = ['I\n', 'a\n']
l3 = ['as\n', 'at\n', 'be\n']
l4 = ['age\n', 'act\n', 'add\n']
l5 = ['also\n', 'able\n', 'area\n', 'away\n']
l6 = ['about\n']
l7 = ['accept\n', 'across\n']
l8 = ['ability\n']
l9 = ['activity\n', 'although\n', 'actually\n']
l10 = ['according\n']
l11 = ['conference\n', 'collection\n', 'commercial\n']
l12 = ['development\n', 'environment\n', 'information\n']
l13 = ['organization\n', 'particularly\n']
l14 = ['environmental\n']
l15 = ['administration\n']

brute_server(l13, l15, l2, l3, l2, l14, l6, l7, l8, l10)

# 13 15 2 3 2 14 6 7 8 10

