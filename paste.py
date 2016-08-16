#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import os
import redis

from flask import Flask,request,Response,render_template
#local config.py
import config

app = Flask(__name__)

def newid():
    return os.urandom(config.LENGTH).hex()

def get_data(linkid):
	storage = redis.Redis(host = config.HOST, port = config.PORT, password = config.PASS,decode_responses=True)
	try:
		data = storage.get(linkid)
	except redis.exception.ConnectionError:
		return False
	return data

def push_data(data):
	storage = redis.Redis(host = config.HOST, port = config.PORT, password = config.PASS,decode_responses=True)
	linkid = newid()
	try:
		storage.setex(linkid,data,config.EXPIRE)
	except redis.exception.ConnectionError:
		return False
	return config.URL+"/"+linkid
	

@app.route(config.POST_URI,methods = ['POST'])
def post():
	if request.form['data']!='':
		url = push_data(request.form['data']);
		if url == False:
			return Response("Internal server error, try again later",status=500)
		return Response(url)

@app.route('/<linkid>')
def get(linkid):
	data = get_data(linkid)
	if data == False:
		return Response("Can't connect to server, try again later\n",status=500)
	elif data == None:
		return Response("No data",status=403)
	
	return Response(data,mimetype='text/plain')

@app.route('/')
def about():
	return render_template('about.html',post_url=config.URL+config.POST_URI,client_url=config.CLIENT_URL)
	
