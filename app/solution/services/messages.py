import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config

FIXED_EMAIL = config ("FIXED_EMAIL")
def send_email(subject, to_email, email_body):
    try:
        SMTP_SERVER = config ("SMTP_SERVER")
        SMTP_PORT = config ("SMTP_PORT")
        SMTP_USER = config ("SMTP_USER")
        SMTP_PASSWORD = config ("SMTP_PASSWORD")
        
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(email_body, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        print("Email sent successfully")
    
    except Exception as e:
        print(f"Error sending email: {e}")