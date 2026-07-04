import os
import random
import string
from datetime import datetime, timedelta
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.orm import Session
from models.otp import OTP
from database.database import SessionLocal

# Dev mode toggle: when true, OTP is printed to console instead of being emailed.
# Enable this when SMTP credentials are missing or during local development.
DEV_MODE = os.getenv("DEV_MODE", "false").lower() in ("1", "true", "yes")



# In-memory store of the most recently generated OTPs (per email). Only used in
# dev mode so the UI can display the code to the tester without needing SMTP.
_dev_otps: dict[str, str] = {}

# Lazy-initialized mail config (only built when we actually need to send mail,
# so dev mode doesn't require valid SMTP credentials).
_mail_conf = None


def get_dev_otp(email: str) -> str | None:
    """Return the last OTP generated for `email` in dev mode (if any)."""
    return _dev_otps.get(email)


def _remember_otp(email: str, otp_code: str) -> None:
    """Cache the latest OTP for retrieval in dev mode."""
    _dev_otps[email] = otp_code


def _get_mail_conf() -> ConnectionConfig:
    """Build the FastMail ConnectionConfig on demand."""
    global _mail_conf
    if _mail_conf is None:
        _mail_conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
            MAIL_FROM=os.getenv("MAIL_FROM", "noreply@aidataanalyst.com"),
            MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
            MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )
    return _mail_conf


def generate_otp() -> str:
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))


async def send_otp_email(email: str, otp_code: str):
    """Send OTP to user's email. In dev mode, just log it to the console."""
    if DEV_MODE:
        # Dev mode: print OTP to console so it can be used without an SMTP server.
        _remember_otp(email, otp_code)
        print("=" * 60)
        print(f"[DEV MODE] OTP for {email}: {otp_code}")
        print("=" * 60)
        return True

    try:
        message = MessageSchema(
            subject="AI Data Analyst Assessment - Verify Your Email",
            recipients=[email],
            body=f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2563eb;">Email Verification</h2>
                        <p>Welcome to AI Data Analyst Assessment!</p>
                        <p>Your OTP for email verification is:</p>
                        <div style="background: #f3f4f6; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0;">
                            <h1 style="color: #2563eb; letter-spacing: 5px; margin: 0;">{otp_code}</h1>
                        </div>
                        <p>This OTP will expire in 10 minutes.</p>
                        <p>If you didn't request this verification, please ignore this email.</p>
                        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
                        <p style="color: #6b7280; font-size: 12px;">
                            © 2026 AI Data Analyst Assessment. All rights reserved.
                        </p>
                    </div>
                </body>
            </html>
            """,
            subtype="html",
        )

        fm = FastMail(_get_mail_conf())
        await fm.send_message(message)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def save_otp(db: Session, email: str, otp_code: str):
    """Save OTP to database"""
    # Delete existing OTP for this email
    db.query(OTP).filter(OTP.email == email).delete()

    # Create new OTP
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


def verify_otp(db: Session, email: str, otp_code: str) -> bool:
    """Verify OTP"""
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
