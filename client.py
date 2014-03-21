#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import gevent
import time
from gevent import monkey
monkey.patch_all()
import urllib2


def fetch_url(url):
    t0 = time.time()
    try:
        resp = urllib2.urlopen(url)
        resp_code = resp.code
    except urllib2.HTTPError, e:
        resp_code = e.code
    t1 = time.time()
    print("\t@ %5.2fs got response [%d]" % (t1 - t0, resp_code))


def time_fetch_urls(url, num_jobs):
    print("Sending %d requests for %s..." % (num_jobs, url))
    t0 = time.time()
    gevent.joinall([gevent.spawn(fetch_url, url) for i in range(num_jobs)])
    t1 = time.time()
    print("SUM TOTAL = %.2fs" % (t1 - t0))


if __name__ == '__main__':

    try:
        num_requests = int(sys.argv[1])
    except IndexError:
        num_requests = 10

    time_fetch_urls("http://localhost:8080/test/postgres/", num_requests)
