from flask import current_app, render_template
from flask_mail import Message
from app import mail

def send_verification_email(user):
    """Send verification email to user."""
    verification_code = user.generate_verification_code()
    
    msg = Message('Verify Your Email',
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    msg.html = render_template('email/verify.html',
                             username=user.username,
                             verification_code=verification_code)
    
    mail.send(msg) 