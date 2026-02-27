from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from app.core.config import settings


def _get_mail_config() -> ConnectionConfig:
    return ConnectionConfig(
        MAIL_USERNAME=settings.SMTP_USERNAME,
        MAIL_PASSWORD=settings.SMTP_PASSWORD,
        MAIL_FROM=settings.SMTP_FROM or settings.SMTP_USERNAME,
        MAIL_PORT=settings.SMTP_PORT,
        MAIL_SERVER=settings.SMTP_HOST,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
    )


async def send_otp_email(email: str, name: str, otp_code: str) -> None:
    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto;">
        <h2 style="color: #2563eb;">Xác thực tài khoản SmartFinance</h2>
        <p>Xin chào <strong>{name}</strong>,</p>
        <p>Mã OTP để hoàn tất đăng ký tài khoản của bạn là:</p>
        <div style="background: #f3f4f6; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0;">
            <span style="font-size: 36px; font-weight: bold; letter-spacing: 8px; color: #1d4ed8;">{otp_code}</span>
        </div>
        <p style="color: #6b7280;">Mã có hiệu lực trong <strong>2 phút</strong>. Vui lòng không chia sẻ mã này với bất kỳ ai.</p>
        <p style="color: #6b7280; font-size: 13px;">Nếu bạn không yêu cầu đăng ký, hãy bỏ qua email này.</p>
    </div>
    """

    message = MessageSchema(
        subject="Mã OTP xác thực tài khoản SmartFinance",
        recipients=[email],
        body=html_body,
        subtype=MessageType.html,
    )

    fm = FastMail(_get_mail_config())
    await fm.send_message(message)
