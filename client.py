#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import urllib3
import sys

from select import select

URL="https://paste.demfloro.ru/add"
TIMEOUT=5

def has_data(fd):
	return select([fd], [], [], 0.0) == ([fd], [], [])

def quit(code, msg):
	print(msg)
	exit(code)

if not has_data(sys.stdin):
	quit(1, "no data given via stdin")
try:
	stdin = sys.stdin.read()
except UnicodeDecodeError:
	quit(2, "an error occured reading stdin")

post_data = { "data": stdin }

http = urllib3.PoolManager()

try:
	r = http.request('POST', URL,fields=post_data,timeout=TIMEOUT)
except urllib3.exceptions.MaxRetryError as err:
	print("{0}".format(err))
	exit(2)
print(r.data.decode('utf-8'))
