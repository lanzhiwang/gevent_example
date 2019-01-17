from __future__ import print_function
import socket

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("./06_unixsocket_server.py.sock")
s.send('GET / HTTP/1.0\r\n\r\n')
data = s.recv(1024)
print('received %s bytes' % len(data))
print(data)
s.close()

'''
$ python 07_unixsocket_client.py
received 94 bytes
HTTP/1.1 200 OK
Connection: close
Date: Thu, 17 Jan 2019 11:03:53 GMT
Content-Length: 0


$

'''
