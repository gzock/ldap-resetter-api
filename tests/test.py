from modules.password_resetter import PasswordResetter
#from modules.ldapcontroller import LdapController

#ldap = LdapController("127.0.0.1", "389")
#ldap.bind(username="uid=test-user,ou=People,dc=example,dc=com", password="hogehoge")
#ldap.set_basedn("ou=People, dc=example, dc=com")
#mail = ldap.get_mail_addr(uid="0024a59b6ad1")
#print(mail)


reset = PasswordResetter()

#token = reset.gen_token()
#password = reset.gen_password()
#reset.send_token("test-user")
#
#print(token)
#print(password)
token = "S4vYh02RJI"
reset.reset_password("test-user", token)
