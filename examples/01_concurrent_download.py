#!/usr/bin/python
# Copyright (c) 2009 Denis Bilenko. See LICENSE for details.

"""Spawn multiple workers and wait for them to complete"""
from __future__ import print_function
import gevent
from gevent import monkey

# 什么时候需要打补丁
# 是大部分补丁还是所有的标准库都打补丁
# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()

import requests

# Note that we're using HTTPS, so
# this demonstrates that SSL works.
urls = [
    'https://www.baidu.com/',
    'https://www.163.com/',
    'https://www.python.org/'
]



def print_head(url):
    print('Starting %s' % url)
    data = requests.get(url).text
    print('%s: %s bytes: %r' % (url, len(data), data[:50]))

jobs = [gevent.spawn(print_head, _url) for _url in urls]

gevent.wait(jobs)

'''
$ python 01_concurrent_download.py
Starting https://www.baidu.com/
Starting https://www.163.com/
Starting https://www.python.org/
https://www.baidu.com/: 2443 bytes: '<!DOCTYPE html>\r\n<!--STATUS OK--><html> <head><met'
https://www.163.com/: 677959 bytes: ' <!DOCTYPE HTML>\n<!--[if IE 6 ]> <html class="ne_u'
https://www.python.org/: 48988 bytes: '<!doctype html>\n<!--[if lt IE 7]>   <html class="n'
$ 

'''
