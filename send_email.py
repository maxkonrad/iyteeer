import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASS")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))


msg = EmailMessage()
msg["Subject"] = "There is an update on İYTE EEE Department Website"
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL

def send_email(update_type, previous_content, current_content):
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            msg.set_content("There is an update on the İYTE EEE Department website. Please check it out! https://eee.iyte.edu.tr\n\n"
                            f"Update Type: {update_type}\n"
                            f"Previous Content: {previous_content}\n"
                            f"Current Content: {current_content}")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
