#!/usr/bin/python
"""Resolve hostnames concurrently, exit after 2 seconds.

Under the hood, this might use an asynchronous resolver based on
c-ares (the default) or thread-pool-based resolver.

You can choose between resolvers using GEVENT_RESOLVER environment
variable. To enable threading resolver:

    GEVENT_RESOLVER=thread python dns_mass_resolve.py
"""
from __future__ import print_function
import gevent
from gevent import socket
from gevent.pool import Pool

N = 1000
# limit ourselves to max 10 simultaneous outstanding requests
pool = Pool(10)
finished = 0


def job(url):
    global finished
    try:
        try:
            ip = socket.gethostbyname(url)
            print('%s = %s' % (url, ip))
        except socket.gaierror as ex:
            print('%s failed with %s' % (url, ex))
    finally:
        finished += 1

with gevent.Timeout(2, False):
    for x in range(10, 10 + N):
        pool.spawn(job, '%s.com' % x)
    pool.join()

print('finished within 2 seconds: %s/%s' % (finished, N))

'''
$ python 02_dns_mass_resolve.py
12.com = 185.53.179.7
16.com = 199.59.242.151
18.com = 64.38.232.185
17.com = 123.56.91.195
10.com failed with [Errno -2] Name or service not known
11.com failed with [Errno -2] Name or service not known
13.com failed with [Errno -2] Name or service not known
20.com = 39.108.146.115
14.com = 199.59.242.151
15.com = 199.59.242.151
19.com = 199.59.242.151
finished within 2 seconds: 11/1000
$
$ python 02_dns_mass_resolve.py
12.com = 185.53.179.7
15.com = 199.59.242.151
14.com = 199.59.242.151
16.com = 199.59.242.151
17.com = 123.56.91.195
18.com = 64.38.232.185
19.com = 199.59.242.151
11.com failed with [Errno -2] Name or service not known
13.com failed with [Errno -2] Name or service not known
10.com failed with [Errno -2] Name or service not known
24.com = 104.20.82.244
21.com = 104.18.53.37
20.com = 39.108.146.115
22.com failed with [Errno -2] Name or service not known
27.com = 162.219.162.52
29.com = 199.59.242.151
23.com = 103.100.208.130
30.com failed with [Errno -2] Name or service not known
33.com failed with [Errno -2] Name or service not known
36.com failed with [Errno -2] Name or service not known
31.com failed with [Errno -2] Name or service not known
39.com = 219.238.238.103
28.com = 123.56.153.176
34.com failed with [Errno -2] Name or service not known
25.com = 184.168.131.241
44.com = 199.59.242.151
45.com failed with [Errno -2] Name or service not known
42.com failed with [Errno -2] Name or service not known
43.com = 199.59.242.151
26.com failed with [Errno -2] Name or service not known
48.com = 120.76.65.111
47.com = 82.98.86.164
50.com failed with [Errno -2] Name or service not known
49.com = 203.78.142.12
53.com = 23.213.40.245
54.com failed with [Errno -2] Name or service not known
52.com failed with [Errno -2] Name or service not known
56.com = 101.227.173.126
51.com = 124.232.162.203
58.com = 115.159.231.173
57.com = 104.209.208.151
59.com failed with [Errno -2] Name or service not known
60.com = 47.75.58.199
55.com = 23.64.191.9
63.com = 47.110.68.244
62.com = 120.24.162.166
65.com = 180.150.188.176
61.com failed with [Errno -2] Name or service not known
66.com failed with [Errno -2] Name or service not known
64.com failed with [Errno -2] Name or service not known
68.com failed with [Errno -2] Name or service not known
70.com = 104.171.24.25
71.com failed with [Errno -2] Name or service not known
67.com = 211.155.80.72
69.com = 107.180.41.84
74.com = 150.242.208.8
73.com = 199.59.242.151
76.com = 144.46.111.61
77.com = 199.59.242.151
finished within 2 seconds: 59/1000
$ 

'''
