import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


async def send_contact_notification(
    name: str,
    email: str,
    phone: str,
    message: str
) -> bool:
    """Send email notification when contact form is submitted."""
    try:
        # Create MIME message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"New Contact Form Submission from {name}"
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = settings.ADMIN_EMAIL
        
        # HTML content
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; direction: rtl; text-align: right;">
                <h2 style="color: #333;">پیام جدید از فرم تماس</h2>
                <p><strong>نام:</strong> {name}</p>
                <p><strong>ایمیل:</strong> {email}</p>
                <p><strong>شماره تلفن:</strong> {phone}</p>
                <hr>
                <p><strong>پیام:</strong></p>
                <p>{message.replace(chr(10), '<br>')}</p>
                <hr>
                <p style="color: #666; font-size: 12px;">
                    این پیام به صورت خودکار از سایت GeoBiro ارسال شده است.
                </p>
            </body>
        </html>
        """
        
        # Text content
        text_content = f"""
        New Contact Form Submission from {name}
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        
        Message:
        {message}
        """
        
        # Attach both versions
        msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))
        
        # Send email
        async with aiosmtplib.SMTP(hostname=settings.SMTP_HOST, port=settings.SMTP_PORT) as smtp:
            await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            await smtp.send_message(msg)
        
        logger.info(f"✓ Contact notification sent to {settings.ADMIN_EMAIL}")
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to send email: {str(e)}")
        return False


async def send_contact_confirmation(
    recipient_email: str,
    name: str
) -> bool:
    """Send confirmation email to user who submitted contact form."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"تشکر از تماس با ما - Thank you for contacting us"
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = recipient_email
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Thank You, {name}!</h2>
                <p>We have received your message and will respond as soon as possible.</p>
                <hr>
                <h2 style="direction: rtl; text-align: right;">سلام {name} عزیز!</h2>
                <p style="direction: rtl; text-align: right;">ما پیام شما را دریافت کردیم و در اسرع وقت پاسخ خواهیم داد.</p>
                <hr>
                <p style="color: #666; font-size: 12px;">GeoBiro Team</p>
            </body>
        </html>
        """
        
        text_content = f"""
        Thank You, {name}!
        
        We have received your message and will respond as soon as possible.
        
        GeoBiro Team
        """
        
        msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))
        
        async with aiosmtplib.SMTP(hostname=settings.SMTP_HOST, port=settings.SMTP_PORT) as smtp:
            await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            await smtp.send_message(msg)
        
        logger.info(f"✓ Confirmation email sent to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to send confirmation email: {str(e)}")
        return False
