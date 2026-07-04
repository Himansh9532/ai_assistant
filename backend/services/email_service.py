import os
import random
import string
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.orm import Session

from models.otp import OTP

load_dotenv()

DEV_MODE = os.getenv("DEV_MODE", "false").lower() in ("1", "true", "yes")

_dev_otps = {}
_mail_conf = None


def get_dev_otp(email: str):
    return _dev_otps.get(email)


def _remember_otp(email: str, otp_code: str):
    _dev_otps[email] = otp_code


def _get_mail_conf():
    global _mail_conf

    if _mail_conf is None:
        _mail_conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
            MAIL_FROM=os.getenv("MAIL_FROM", ""),
            MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
            MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),

            MAIL_STARTTLS=os.getenv(
                "MAIL_STARTTLS",
                "true"
            ).lower() == "true",

            MAIL_SSL_TLS=os.getenv(
                "MAIL_SSL_TLS",
                "false"
            ).lower() == "true",

            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )

    return _mail_conf


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


async def send_otp_email(email: str, otp_code: str):
    if DEV_MODE:
        _remember_otp(email, otp_code)

        print("=" * 60)
        print(f"[DEV MODE] OTP for {email}: {otp_code}")
        print("=" * 60)

        return True

    try:
        print("MAIL_USERNAME =", os.getenv("MAIL_USERNAME"))
        print("MAIL_SERVER =", os.getenv("MAIL_SERVER"))
        print("MAIL_PORT =", os.getenv("MAIL_PORT"))

        message = MessageSchema(
            subject="AI Data Analyst Assessment - Verify Your Email",
            recipients=[email],
            body=f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="max-width:600px;margin:auto;padding:20px;">
                        <h2>Email Verification</h2>

                        <p>Welcome to AI Data Analyst Assessment.</p>

                        <p>Your OTP is:</p>

                        <div style="
                            text-align:center;
                            padding:20px;
                            background:#f3f4f6;
                            border-radius:10px;
                        ">
                            <h1>{otp_code}</h1>
                        </div>

                        <p>This OTP will expire in 10 minutes.</p>
                    </div>
                </body>
            </html>
            """,
            subtype="html"
        )

        fm = FastMail(_get_mail_conf())

        await fm.send_message(message)

        print(f"OTP sent successfully to {email}")

        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def save_otp(db: Session, email: str, otp_code: str):
    db.query(OTP).filter(
        OTP.email == email
    ).delete()

    new_otp = OTP(
        email=email,
        otp_code=otp_code,
        is_verified=0,
        expires_at=datetime.utcnow() + timedelta(minutes=10)
    )

    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)

    return new_otp


def verify_otp(db: Session, email: str, otp_code: str):
    otp = db.query(OTP).filter(
        OTP.email == email,
        OTP.otp_code == otp_code
    ).first()

    if not otp:
        return False

    if datetime.utcnow() > otp.expires_at:
        return False

    otp.is_verified = 1

    db.commit()

    return True