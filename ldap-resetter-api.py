#!/bin/env /bin/python
# -*- coding: utf-8 -*-

import sys
import json
import re
from gevent.pywsgi import WSGIServer
from bottle import route, run, hook, ServerAdapter
from bottle import get, post, request, response
from bottle import HTTPResponse
from modules.password_resetter import PasswordResetter

class WebServer(ServerAdapter):

  @route('/api/token', method=['POST', 'OPTIONS'])
  def do_gen_token():
    reset = PasswordResetter()
    body = {}
    if request.method == "POST":
      body = json.load(request.body)
      uid = body["uid"]
  
      try:
        ret = reset.send_token(uid)
        body = {"code": 200, "result": "success"}
      except Exception as e:
        print(e)
        body = {"code": 500, "result": "fail"}
  
    res = HTTPResponse(status=200, body=body)
    res.set_header('Access-Control-Allow-Origin', '*')
    res.set_header('Access-Control-Allow-Headers', '*')
    res.set_header('Access-Control-Allow-Credentials', 'true')
    res.set_header('Content-Type', 'application/json')
    return res

  @route('/api/reset', method=['POST', 'OPTIONS'])
  def do_reset_password():
    reset = PasswordResetter()
    body = {}
    if request.method == "POST":
      body = json.load(request.body)
      uid = body["uid"]
      token = body["token"]
  
      try:
        ret = reset.reset_password(uid=uid, token=token)
        body = {"code": 200, "result": "success"}
      except Exception as e:
        print(e)
        body = {"code": 500, "result": "fail"}
  
    res = HTTPResponse(status=200, body=body)
    res.set_header('Access-Control-Allow-Origin', '*')
    res.set_header('Access-Control-Allow-Headers', '*')
    res.set_header('Access-Control-Allow-Credentials', 'true')
    res.set_header('Content-Type', 'application/json')
    return res
  
  def run(self, handler):
    srv = WSGIServer((self.host, self.port), handler)
    srv.serve_forever()

run(host='0.0.0.0', port=8080, server=WebServer, debug=True)
