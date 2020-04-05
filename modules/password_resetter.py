import os
import random
import string

from modules.ldapcontroller import LdapController
from modules.mailcontroller import MailController
from modules.mongocontroller import MongoController
 
class PasswordResetter():

  MONGO_HOST = os.getenv('MONGO_HOST')
  MONGO_PORT = os.getenv('MONGO_PORT')
  LDAP_HOST = os.getenv('LDAP_HOST')
  LDAP_PORT = os.getenv('LDAP_PORT')
  LDAP_ADMIN_USER = os.getenv('LDAP_ADMIN_USER') 
  LDAP_ADMIN_PASSWORD = os.getenv('LDAP_ADMIN_PASSWORD') 
  LDAP_USER_OU = os.getenv('LDAP_USER_OU')
  LDAP_BIND_DN = os.getenv('LDAP_BIND_DN')  
  SMTP_HOST = os.getenv('SMTP_HOST')
  MAIL_FROM_ADDR = os.getenv('MAIL_FROM_ADDR')

  def __init__(self):
    self.mongo = MongoController(self.MONGO_HOST, self.MONGO_PORT)
    self.ldap = LdapController(self.LDAP_HOST, self.LDAP_PORT)
    self.ldap.set_basedn(self.LDAP_BIND_DN)
    self.ldap.set_userou(self.LDAP_USER_OU)
    self.ldap.bind(
        username=self.LDAP_ADMIN_USER, 
        password=self.LDAP_ADMIN_PASSWORD
    )
    self.mail = MailController(smtp_host=self.SMTP_HOST)

  def __gen_random_value(self, num=10 ):
    chars = string.ascii_letters + string.digits
    return ''.join([random.choice(chars) for i in range(num)])

  def gen_token(self):
    return self.__gen_random_value(num=10)

  def gen_password(self):
    return self.__gen_random_value(num=5)

  def send_token(self, uid):
    token = self.gen_token()
    self.mongo.add_token(uid=uid, token=token)
    to_addr = self.ldap.get_mail_addr(uid=uid)
    self.mail.send(src=self.MAIL_FROM_ADDR, to=to_addr, subject="confirmation token", body=token)

  def reset_password(self, uid, token):
    ret = self.mongo.get_token(uid=uid)
    if not ret:
      return False
    if not token == ret["token"]:
      return False

    password = self.gen_password()
    ret = self.ldap.reset_password(uid=uid, password=password)
    if not ret:
      return False

    to_addr = self.ldap.get_mail_addr(uid=uid)
    self.mail.send(src=self.MAIL_FROM_ADDR, to=to_addr, subject="your new password", body=password)
    return True
