import ldap
import ldif
import sys
 
class LdapController:

  __ldap = None
  __basedn = None

  def __init__(self, host, port):
    uri = "ldap://" + host + ":" + str(port)
    #self.__ldap = ldap.initialize(uri, bytes_mode=False)
    self.__ldap = ldap.initialize(uri, bytes_mode=True)

  def bind(self, username, password):
    self.__ldap.simple_bind_s(username, password)

  def set_basedn(self, dn):
    self.__basedn = dn

  def search(self, filter):
    return self.__ldap.search_s(self.__basedn, ldap.SCOPE_SUBTREE, filter)

  def get_mail_addr(self):
    pass
  
  def authentication(self, username, groups):
    if type(username) is not str or type(groups) is not list or self.__basedn is None:
      raise AttributeError

    allow_groups = []
    for group in groups:
      allow_groups.append(group.lower())
      
    result = self.search("(sAMAccountName=" + username + ")")

    for dn, entry in result:
      for group in entry["memberOf"]:
        if group.lower() in allow_groups:
          return True
    return False
