import sqlite3
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import html
import sqlite3
import os


# Reading files 

base_dir = os.path.dirname(os.path.abspath(__file__))

with open (os.path.join(base_dir, "emailformat.html"),'r') as f:
    html_content = f.read()

connection = sqlite3.connect(os.path.join(base_dir, "news.db"))
cursor = connection.cursor()
cursor.execute("SELECT * FROM articles LIMIT 10 ")
news_items = cursor.fetchall()
connection.close()



#Creating html to inject

news_html = ""

for topic, title, url,summary, llm_summary in news_items:

    llm_summary = llm_summary.strip()
    llm_summary = llm_summary[0].upper() + llm_summary[1:]


    news_html += f"""
    <tr>
        <td align="center" style="padding: 20px;">
        <table width="90%" cellpadding="0" cellspacing="0" border="0" style="background:#ffffff; border:1px solid #dddddd; border-radius:8px; padding:20px; box-shadow:0 2px 5px rgba(0,0,0,0.05);">
            <tr>
            <td>
                <p style="margin-top:10px; font-size:12px; color:#888888;">Topic : {html.escape(topic).capitalize()}</p>
                <h2 style="margin:0 0 10px 0; font-size:20px; color:#222831;">{html.escape(title).capitalize()}</h2>
                <p style="margin:0 0 10px 0; font-size:15px; color:#555555;">{html.escape(llm_summary)}</p>
                <a href="{html.escape(url)}" style="font-size:12px; color:#1e88e5; text-decoration:none;">Know more</a>
            </td>
            </tr>
        </table>
        </td>
    </tr>
    """

start_marker = "<!-- START LOOP HERE -->"
end_marker = "<!-- END LOOP HERE -->"
start_index = html_content.find(start_marker) + len(start_marker)
end_index = html_content.find(end_marker)
final_html = html_content[:start_index] + news_html + html_content[end_index:]



# Email_sending

sender_email = "vikashhadaikalavansg@gmail.com"
app_password = "ugyt ibyk dhwc vnnl"

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


message = MIMEMultipart('alternative')
message["Subject"] = "📰 Daily News Digest"
message["From"] = sender_email

message.attach(MIMEText(final_html, "html"))

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

server.close()


