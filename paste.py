#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import os
import redis

from flask import Flask,request,Response,render_template
#local config.py
import config

app = Flask(__name__)

def redis_connect(host = config.HOST,port = config.PORT, password = config.PASS):
	return redis.Redis(host = host,port = port,password = password,decode_responses = True)

def newid():
	storage = redis_connect()
	key = os.urandom(config.LENGTH).hex()
	while storage.exists(key):
		key = os.urandom(config.LENGTH).hex()
	return key

def get_data(linkid):
	storage = redis_connect()
	try:
		data = storage.get(linkid)
	except redis.exceptions.ConnectionError:
		return False
	return data

def push_data(data):
	storage = redis_connect()
	linkid = newid()

	try:
		storage.setex(linkid,data,config.EXPIRE)
	except redis.exceptions.ConnectionError:
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
	return render_template('about.html',post_url=config.URL+config.POST_URI,client_url=config.CLIENT_URL,github_url=config.GITHUB_URL)
	
