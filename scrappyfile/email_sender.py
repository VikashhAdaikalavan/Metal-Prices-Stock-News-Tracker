import sqlite3
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "vikashhadaikalavansg@gmail.com"
app_password = "wafk fkid mkly zhry"

list_of_receivers = ['vikashhadaikalavan@gmail.com']

#sender_email = os.environ.get("EMAIL_USER")
#app_password = os.environ.get("EMAIL_PASS")

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
try:

    server.login(sender_email, app_password)

except smtplib.SMTPAuthenticationError as e:
    print("Authentication Error")
    print(f"Error: {e}")

with open('dashboard.html','r') as f:
    content = f.read()

message = MIMEMultipart['alternative']
message["Subject"] = "📰 Daily News Digest"
message["From"] = sender_email

message.attach(MIMEText(content, "html"))

for receiver_email in list_of_receivers:
    message["To"] = receiver_email
    
    try:
        server.sendmail(sender_email, receiver_email, message.as_string())
    
    except smtplib.SMTPRecipientsRefused as e:
        print("The recipient's email address was refused.")
        print(f"Error: {e}")

    except smtplib.SMTPConnectError as e:
        print("Failed to connect to the SMTP server.")
        print(f"Error: {e}")

    except smtplib.SMTPDataError as e:
        print("The server refused to accept the message data.")
        print(f"Error: {e}")

    except smtplib.SMTPException as e:
        print("A generic SMTP error occurred.")
        print(f"Error: {e}")

    except Exception as e:
        print("Something else went wrong.")
        print(f"Error: {e}")

    else:
        print("Email sent successfully!")

    finally:
        server.close()


