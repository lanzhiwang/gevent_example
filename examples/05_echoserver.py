#!/usr/bin/env python
"""Simple server that listens on port 16000 and echos back every input to the client.

Connect to it with:
  telnet 127.0.0.1 16000

Terminate the connection by terminating telnet (typically Ctrl-] and then 'quit').
"""
from __future__ import print_function
from gevent.server import StreamServer


# this handler will be run for each incoming connection in a dedicated greenlet
def echo(socket, address):
    print('New connection from %s:%s' % address)
    socket.sendall(b'Welcome to the echo server! Type quit to exit.\r\n')
    # using a makefile because we want to use readline()
    rfileobj = socket.makefile(mode='rb')
    while True:
        line = rfileobj.readline()
        if not line:
            print("client disconnected")
            break
        if line.strip().lower() == b'quit':
            print("client quit")
            break
        socket.sendall(line)
        print("echoed %r" % line)
    rfileobj.close()

if __name__ == '__main__':
    # to make the server use SSL, pass certfile and keyfile arguments to the constructor
    server = StreamServer(('127.0.0.1', 16000), echo)
    # to start the server asynchronously, use its start() method;
    # we use blocking serve_forever() here because we have no other jobs
    print('Starting echo server on port 16000')
    server.serve_forever()

'''
$ python 05_echoserver.py
Starting echo server on port 16000
New connection from 127.0.0.1:57708
echoed b'hello world\r\n'
client quit
^CKeyboardInterrupt
2019-01-17T10:57:32Z
Traceback (most recent call last):
  File "05_echoserver.py", line 37, in <module>
    server.serve_forever()
  File "/home/lanzhiwang/work/py_web/venv/lib/python3.5/site-packages/gevent/baseserver.py", line 369, in serve_forever
    self._stop_event.wait()
  File "src/gevent/event.py", line 127, in gevent._event.Event.wait
  File "src/gevent/_abstract_linkable.py", line 192, in gevent.__abstract_linkable.AbstractLinkable._wait
  File "src/gevent/_abstract_linkable.py", line 165, in gevent.__abstract_linkable.AbstractLinkable._wait_core
  File "src/gevent/_abstract_linkable.py", line 169, in gevent.__abstract_linkable.AbstractLinkable._wait_core
  File "src/gevent/_greenlet_primitives.py", line 60, in gevent.__greenlet_primitives.SwitchOutGreenletWithLoop.switch
  File "src/gevent/_greenlet_primitives.py", line 60, in gevent.__greenlet_primitives.SwitchOutGreenletWithLoop.switch
  File "src/gevent/_greenlet_primitives.py", line 64, in gevent.__greenlet_primitives.SwitchOutGreenletWithLoop.switch
  File "src/gevent/__greenlet_primitives.pxd", line 35, in gevent.__greenlet_primitives._greenlet_switch
KeyboardInterrupt
$ 

'''

'''
lanzhiwang@lanzhiwang-desktop:~$ telnet 127.0.0.1 16000
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
Welcome to the echo server! Type quit to exit.
hello world
hello world
quit
Connection closed by foreign host.
$

'''
