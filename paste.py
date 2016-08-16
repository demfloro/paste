#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import os
import redis

from flask import Flask,request,Response
#local config.py
import config

app = Flask(__name__)
storage = redis.Redis(host = config.HOST, port = config.PORT, password = config.PASS,decode_responses=True)

def newid():
    return os.urandom(config.LENGTH).hex()

@app.route('/add',methods = ['POST'])
def post():
	if request.form['data']!='':
		linkid = newid()
		value = request.form['data']
		try:
			storage.set(linkid,value)
			return config.URL+linkid
		except redis.exceptions.ConnectionError:
			return Response("Internal server error, try again later",status=500)
@app.route('/<linkid>')
def get(linkid):
	try:
		data = storage.get(linkid)
	except redis.exceptions.ConnectionError:
		return Response("Internal server error, try again later",status=500)
	if data == None:
		return Response("No data",status=403)
	
	return Response(storage.get(linkid),mimetype='text/plain')

