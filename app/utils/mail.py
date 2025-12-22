import smtplib
import random
from email.message import EmailMessage
from datetime import datetime, timedelta

def send_admin_otp(admin):
    otp = str(random.randint(100000, 999999))
    admin.otp = otp
    admin.otp_expiry = datetime.utcnow() + timedelta(minutes=10)

    msg = EmailMessage()
    msg["Subject"] = "Confirm Admin Credential Change"
    msg["From"] = "anantham1102@gmail.com"
    msg["To"] = admin.email
    msg.set_content(f"Your OTP is {otp}. Valid for 10 minutes.")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("anantham1102@gmail.com", "APP_PASSWORD")
        server.send_message(msg)
