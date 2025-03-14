from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.services.db_service import DatabaseService
from urllib.parse import urlparse, urljoin
import re
from app.services.verify_service import send_verification_email
import secrets  # For generating verification tokens

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

ALLOWED_EMAIL_DOMAINS = ['gmail.com', 'protonmail.com', 'proton.me']

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def is_valid_email_domain(email):
    domain = email.split('@')[-1]  # Extract domain from email
    return domain in ALLOWED_EMAIL_DOMAINS

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        next_page = request.args.get('next')

        user = DatabaseService.get_user_by_username(username)

        if user and user.check_password(password):
            if not user.is_verified:
                flash('Please verify your email before logging in.', 'warning')
                return redirect(url_for('auth.login'))

            login_user(user)
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not is_valid_email_domain(email):
            flash('Invalid email domain. Please use @gmail.com, @protonmail.com, or @proton.me', 'danger')
            return render_template('auth/register.html')

        if DatabaseService.get_user_by_username(username):
            flash('Username already exists', 'danger')
            return render_template('auth/register.html')

        if DatabaseService.get_user_by_email(email):
            flash('Email already registered', 'danger')
            return render_template('auth/register.html')

        verification_token = secrets.token_urlsafe(32)
        new_user = DatabaseService.create_user(username, email, password, verification_token)

        send_verification_email(email, verification_token)
        flash('Registration successful! Please check your email for verification before logging in.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/verify_email/<token>')
def verify_email(token):
    user = DatabaseService.get_user_by_verification_token(token)
    if user:
        user.is_verified = True
        user.verification_token = None  # Clear the token after verification
        DatabaseService.save_user(user)
        flash('Email verified successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    else:
        flash('Invalid or expired verification token.', 'danger')
        return redirect(url_for('auth.register'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
