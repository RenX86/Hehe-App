from flask import url_for, flash, redirect, Blueprint  # Added missing imports
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

mail = Mail()
serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

def send_verification_email(email, verification_token):
    verification_link = url_for('auth.verify_email', token=verification_token, _external=True)

    msg = Message('Verify Your Email', recipients=[email])
    msg.body = f'Click the link to verify your email: {verification_link}'

    mail.send(msg)

@auth_bp.route('/verify_email/<token>')  # Correct blueprint reference
def verify_email(token):
    try:
        email = serializer.loads(token, salt='email-verification', max_age=3600)  # 1-hour expiry
        flash('Email verified successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    except:
        flash('Verification link is invalid or expired.', 'danger')
        return redirect(url_for('auth.register'))
