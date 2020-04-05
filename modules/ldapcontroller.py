import os
import ldap
 
class LdapController:

  LDAP_MAIL_ATTR = os.getenv('LDAP_MAIL_ATTR')
  __ldap = None
  __basedn = None

  def __init__(self, host, port):
    uri = "ldap://" + str(host) + ":" + str(port)
    self.__ldap = ldap.initialize(uri, bytes_mode=False)

  def set_basedn(self, dn):
    self.__basedn = dn

  def set_userou(self, ou):
    self.__userou = ou

  def bind(self, username, password):
    self.__ldap.simple_bind_s("cn=%s,%s" % (username, self.__basedn), password)

  def search(self, filter):
    return self.__ldap.search_s(self.__basedn, ldap.SCOPE_SUBTREE, filter)

  def get_mail_addr(self, uid):
    ret = self.search("(uid=%s)" % uid)
    return ret[0][1][self.LDAP_MAIL_ATTR][0].decode()

  def reset_password(self, uid, password):
    return self.__ldap.passwd_s("uid=%s,ou=%s,%s" % (uid, self.__userou, self.__basedn), None, password)
  
  #def authentication(self, username, groups):
  #  if type(username) is not str or type(groups) is not list or self.__basedn is None:
  #    raise AttributeError

  #  allow_groups = []
  #  for group in groups:
  #    allow_groups.append(group.lower())
  #    
  #  result = self.search("(sAMAccountName=" + username + ")")

  #  for dn, entry in result:
  #    for group in entry["memberOf"]:
  #      if group.lower() in allow_groups:
  #        return True
  #  return False
