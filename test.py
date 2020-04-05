#!/bin/env /bin/python
# -*- coding: utf-8 -*-

from modules.ldapcontroller import LdapController
import ldif
import sys


ldap = LdapController("127.0.0.1", 389)
username = "user01@vuv.local"
ldap.bind(username, "Hogehoge")
ldap.set_basedn("cn=users, dc=vuv, dc=local")
ret = ldap.authentication("user01", ["cn=testgroup,cn=users,dc=vuv,dc=local", "cn=domain users,cn=users,dc=vuv,dc=local"])
if ret:
  print "success"
else:
  print "fail"

## for manual ##
#allow_group = ["cn=testgroup,cn=users,dc=vuv,dc=local", "cn=domain users,cn=users,dc=vuv,dc=local"]
#ldap = LdapController("127.0.0.1", 389)
#
#username = "user01@vuv.local"
#ldap.bind(username, "Hogehoge")
#ldap.set_basedn("cn=users, dc=vuv, dc=local")
#result = ldap.search("(sAMAccountName=user01)")
#
#ldif_writer=ldif.LDIFWriter(sys.stdout)
#for dn, entry in result:
#  for group in entry["memberOf"]:
#    if group.lower() in allow_group:
#      print "success" 
#
