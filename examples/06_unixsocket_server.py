import os
from gevent.pywsgi import WSGIServer
from gevent import socket


def application(environ, start_response):
    assert environ
    start_response('200 OK', [])
    return []  # 返回的数据类型是什么


if __name__ == '__main__':
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sockname = './' + os.path.basename(__file__) + '.sock'  # 06_unixsocket_server.py.sock=
    if os.path.exists(sockname):
        os.remove(sockname)
    listener.bind(sockname)
    listener.listen(1)
    WSGIServer(listener, application).serve_forever()
