import socket
import struct
import binascii
import requests
import chardet

from scapy.all import  *
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("52.28.255.56", 1080))
s.send(bytearray.fromhex("5a01fedd749c2e"))
r = s.recv(100)

raw =struct.unpack('BBB',r[3:6])
cookie =[hex(x) for x in raw]
cookie =hex(int("".join(x[2:] for x in cookie),16)^4412225)

mb = bytearray()
mb.append(0x5a)
mb.append(r[2])
mb.append(int(cookie[2:4],16))
mb.append(int(cookie[4:6],16))
mb.append(int(cookie[6:],16))
sh = hex(binascii.crc32(mb) % (1 << 32))[2:]
for i in range(0, len(sh), 2):
    mb.append(bytearray.fromhex(str(sh[i]) + str(sh[i + 1]))[0])
s.send(mb)


s.send(bytearray.fromhex("5a010001c0a8ad140050624A3063"))
s.recv(100)
request = 'GET /Flag.jpg HTTP/1.1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36\r\nHost: www.tutorialspoint.com\r\nAccept-Language: en-us\r\nConnection: Keep-Alive\r\n\r\n'

s.send(request.encode())

with open('Flag.jpg','ab') as file:
    for i in range(75):
        res = s.recv(2048)
        file.write(res)

# run binwalk -D .* Flag.jpg --> get the flag

