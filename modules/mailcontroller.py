import smtplib
from email.mime.text import MIMEText
 
class MailController:
  encoding = 'utf-8'

  def __init__(self, smtp_svr="127.0.0.1"):
    self.mail = smtplib.SMTP(smtp_svr)
  
  def send(self, src, to, subject, body):
    self.msg = MIMEText(body.encode(self.encoding), 'plain', _charset=self.encoding)
    self.msg['Subject'] = subject
    self.msg['From'] = src
    self.msg['To'] = to
    self.mail.send_message(self.msg)
