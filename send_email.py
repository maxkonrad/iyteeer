import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASS")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))

def send_email(update_type, previous_content, current_content):
    try:
        # Mesaj objesi her çağrıldığında temiz ve yeni oluşturulmalı
        msg = EmailMessage()
        msg["Subject"] = f"İYTE EEE Güncellemesi: {update_type}"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        
        msg.set_content(f"İYTE EEE bölüm sitesinde bir güncelleme var!\nLink: https://eee.iyte.edu.tr\n\n"
                        f"Kategori: {update_type}\n"
                        f"Eski İçerik: {previous_content}\n"
                        f"Yeni İçerik: {current_content}")
        
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print(f"Email başarıyla gönderildi dayı: {update_type}")
    except Exception as e:
        print(f"Mail gönderimi patladı hacı: {e}")