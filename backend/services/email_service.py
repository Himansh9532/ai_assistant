import os
import random
import string
import traceback
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.orm import Session

from models.otp import OTP

load_dotenv()

# ==========================
# Environment Variables
# ==========================

MAIL_USER = os.getenv("MAIL_USERNAME")
MAIL_PASS = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")

DEV_MODE = os.getenv(
    "DEV_MODE",
    "false"
).lower() in ("1", "true", "yes")

print("MAIL USER:", MAIL_USER)
print("MAIL PASS OK:", bool(MAIL_PASS))
print("MAIL SERVER:", os.getenv("MAIL_SERVER"))
print("MAIL PORT:", os.getenv("MAIL_PORT"))

# ==========================
# Dev OTP Store
# ==========================

_dev_otps = {}

def get_dev_otp(email: str):
    return _dev_otps.get(email)


def _remember_otp(email: str, otp_code: str):
    _dev_otps[email] = otp_code


# ==========================
# Mail Configuration
# ==========================

def _get_mail_conf():

    return ConnectionConfig(
        MAIL_USERNAME=MAIL_USER,
        MAIL_PASSWORD=MAIL_PASS,
        MAIL_FROM=MAIL_FROM,
        MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
        MAIL_SERVER=os.getenv("MAIL_SERVER"),

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


# ==========================
# Generate OTP
# ==========================

def generate_otp():
    return ''.join(
        random.choices(
            string.digits,
            k=6
        )
    )


# ==========================
# Send OTP Email
# ==========================

async def send_otp_email(
    email: str,
    otp_code: str
):

    print("Sending OTP to:", email)

    if DEV_MODE:
        _remember_otp(email, otp_code)
        print("DEV OTP:", otp_code)
        return True

    try:

        html = f"""
        <html>
        <body style="font-family:Arial,sans-serif">

            <h2>AI Data Analyst Assessment</h2>

            <p>Hello,</p>

            <p>Your OTP for email verification is:</p>

            <h1 style="color:#0d6efd;">
                {otp_code}
            </h1>

            <p>
                This OTP is valid for
                <b>10 minutes</b>.
            </p>

            <p>
                Please do not share this OTP
                with anyone.
            </p>

        </body>
        </html>
        """

        message = MessageSchema(
            subject="AI Data Analyst Assessment - OTP Verification",
            recipients=[email],
            body=html,
            subtype="html"
        )

        fm = FastMail(_get_mail_conf())

        await fm.send_message(message)

        print("OTP email sent successfully.")

        return True

    except Exception as e:

        print("========== SMTP ERROR ==========")
        traceback.print_exc()
        print(e)
        print("================================")

        return False


# ==========================
# Save OTP
# ==========================

def save_otp(
    db: Session,
    email: str,
    otp_code: str
):

    db.query(OTP).filter(
        OTP.email == email
    ).delete()

    otp = OTP(
        email=email,
        otp_code=otp_code,
        is_verified=0,
        expires_at=datetime.utcnow()
        + timedelta(minutes=10)
    )

    db.add(otp)
    db.commit()
    db.refresh(otp)

    return otp


# ==========================
# Verify OTP
# ==========================

def verify_otp(
    db: Session,
    email: str,
    otp_code: str
):

    otp = db.query(OTP).filter(
        OTP.email == email,
        OTP.otp_code == otp_code
    ).first()

    if otp is None:
        return False

    if datetime.utcnow() > otp.expires_at:
        return False

    otp.is_verified = 1

    db.commit()

    return True