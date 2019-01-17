#!/usr/bin/env python
from __future__ import print_function
import gevent
from gevent import subprocess

import sys

if sys.platform.startswith("win"):
    print("Unable to run on windows")
else:
    # run 2 jobs in parallel
    p1 = subprocess.Popen(['uname'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['ls'], stdout=subprocess.PIPE)

    gevent.wait([p1, p2], timeout=2)

    # print the results (if available)
    if p1.poll() is not None:
        print('uname: %r' % p1.stdout.read())
    else:
        print('uname: job is still running')
    if p2.poll() is not None:
        print('ls: %r' % p2.stdout.read())
    else:
        print('ls: job is still running')

    p1.stdout.close()
    p2.stdout.close()

'''
$ python 04_processes.py
uname: b'Linux\n'
ls: b'01_concurrent_download.py\n02_dns_mass_resolve.py\n03_threadpool.py\n04_processes.py\nechoserver.py\ngeventsendfile.py\nportforwarder.py\npsycopg2_pool.py\nserver.crt\nserver.key\nudp_client.py\nudp_server.py\nunixsocket_client.py\nunixsocket_server.py\nwebchat\nwebproxy.py\nwebpy.py\nwsgiserver.py\nwsgiserver_ssl.py\n'
$
$ python 04_processes.py
uname: b'Linux\n'
ls: b'01_concurrent_download.py\n02_dns_mass_resolve.py\n03_threadpool.py\n04_processes.py\nechoserver.py\ngeventsendfile.py\nportforwarder.py\npsycopg2_pool.py\nserver.crt\nserver.key\nudp_client.py\nudp_server.py\nunixsocket_client.py\nunixsocket_server.py\nwebchat\nwebproxy.py\nwebpy.py\nwsgiserver.py\nwsgiserver_ssl.py\n'
$

'''
