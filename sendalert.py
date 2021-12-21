from datetime import datetime
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from alertkey import *

mail_content_html = """
    <html>
  <head></head>
  <body>
    <h1>Hello,</h1>
    <h2>Drowsiness Alert System Here !</h2>
    <p><b>Please take a look, someone is feeling drowsy.</b> </p>
    <p><b>Thank You </b></p>
  </body>
</html>
"""
mail_content_html_space = '''
    <html>
    <body><p></p></body>
    </html>
'''
mail_content_hostname =  "\U0001F697" +" " + socket.gethostname() + " " 

mail_content_ip = "\U0001F30F"+" " + " IP = " + socket.gethostbyname(socket.gethostname()) + " "

mail_content_date = "\U0001F570"+ " "+ datetime.now().strftime("%A:%d:%B:%Y") + " "

mail_content_time = " " + " " + datetime.now().strftime("%H:%M:%S") + " "


#The mail addresses and password
sender_address = send_address
sender_pass = password
receiver_address = receive_address

#Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = socket.gethostname() + ' User is feeling drowsy.'   #The subject line

#The body and the attachments for the mail
message.attach(MIMEText(mail_content_html, 'html'))
message.attach(MIMEText(mail_content_html_space, 'html'))

message.attach(MIMEText(mail_content_hostname,'plain'))
message.attach(MIMEText(mail_content_html_space, 'html'))

message.attach(MIMEText(mail_content_ip,'plain'))
message.attach(MIMEText(mail_content_html_space, 'html'))

message.attach(MIMEText(mail_content_date,'plain'))
message.attach(MIMEText(mail_content_time,'plain'))


attach_file_name = 'image.jpg'

with open(attach_file_name, 'rb') as f:
    # set attachment mime and file name, the image type is png
    mime = MIMEBase('image', 'jpg', filename='image.jpg')
    # add required header data:
    mime.add_header('Content-Disposition', 'attachment', filename='Drowsiness.png')
    mime.add_header('X-Attachment-Id', '0')
    mime.add_header('Content-ID', '<0>')
    # read attachment file content into the MIMEBase object
    mime.set_payload(f.read())
    # encode with base64
    encoders.encode_base64(mime)
    # add MIMEBase object to MIMEMultipart object
    message.attach(mime)
try:
  #Create SMTP session for sending the mail
  session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
  session.starttls() #enable security
  session.login(sender_address, sender_pass) #login with mail_id and password
  text = message.as_string()
  session.sendmail(sender_address, receiver_address, text)
  session.quit()
  print('[Info] Alert Sent')
except smtplib.SMTPException:
    print ("Error: unable to send alert")
   





