#!/bin/env /bin/python
# -*- coding: utf-8 -*-

import sys
import json
import re
from bottle import route, run, hook, ServerAdapter
from bottle import get, post, request, response
from bottle import HTTPResponse
from modules.ldapcontroller import LdapController
#from modules.mongocontroller import MongoController

class WebServer(ServerAdapter):
  @route('/api/login', method='GET')  # or @get('/login')
 # def login():
 #     username = request.query.get('user')
 #     password = request.query.get('pass')
 # 
 #     #GETで何も渡されていない時はusername,passwordに何も入れない
 #     username = "" if username is None else username
 #     password = "" if password is None else password
 # 
 #     return '''
 #     <form action="/login" method="post">
 #             Username: <input name="username" type="text" value="{username}"/>
 #             Password: <input name="password" type="password" value="{password}"/>
 #             <input value="Login" type="submit" />
 #         </form>
 #     '''.format(username=username, password=password)
 # 
  
  @route('/api/login', method=['POST', 'OPTIONS'])  # or @post('/post')
  def do_login():
      body = {}
      DOMAIN = "@example.local"
      token = ""
      if request.method == "POST":
        ldap = LdapController("127.0.0.1", 389)
        auth = Authentication()
        body = json.load(request.body)
        username = body["username"]
        password = body["password"]
        username = username.encode('utf-8')
        password = password.encode('utf-8')
  
        try:
          ldap.bind(username + DOMAIN, password)
          ldap.set_basedn("cn=users, dc=example, dc=local")
          #ret = ldap.authentication(username, ["cn=testgroup,cn=users,dc=example,dc=local", "cn=domain users,cn=users,dc=example,dc=local"])
          ret = ldap.authentication(username, ["cn=testgroup,cn=users,dc=example,dc=local"])
          if ret:
            body = {"login": True, "username": username, "exp": datetime.utcnow() + timedelta(hours=8)}
            token = auth.encode(body)
          else:
            body = {"login": False, "username": username, "error_message": "authentication failed."}

        except:
          body = {"login": False, "username": username, "error_message": "authentication failed."}
  
      res = HTTPResponse(status=200, body=body)
      if token:
        res.set_cookie("access_token", token, max_age=28800, secure=True)
      res.set_header('Access-Control-Allow-Origin', 'http://127.0.0.1:4201')
      res.set_header('Access-Control-Allow-Headers', '*')
      res.set_header('Access-Control-Allow-Credentials', 'true')
      res.set_header('Content-Type', 'application/json')
      return res
  
  def run(self, handler):
    from gevent.pywsgi import WSGIServer

    #srv = WSGIServer((self.host, self.port), handler, certfile='certs/dev_cacert.pem', keyfile='certs/dev_privkey.pem')
    srv = WSGIServer((self.host, self.port), handler)

    srv.serve_forever()

run(host='127.0.0.1', port=8443, server=WebServer, debug=True)
