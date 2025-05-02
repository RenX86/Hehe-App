from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db
from app.utils.email import send_verification_email
from app.utils.security import (
    sanitize_input, sanitize_email, validate_password, 
    sanitize_verification_code, validate_email_domain
)
from datetime import datetime
from sqlalchemy.exc import OperationalError
from flask_mail import Message

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        try:
            # Sanitize and validate inputs
            username = sanitize_input(request.form.get('username', ''))
            email = sanitize_email(request.form.get('email', ''))
            password = request.form.get('password', '')
            
            # Validate password strength
            is_valid_password, password_message = validate_password(password)
            if not is_valid_password:
                flash(password_message, 'error')
                return redirect(url_for('auth.register'))
            
            # Validate email domain
            is_valid_domain, domain_message = validate_email_domain(email)
            if not is_valid_domain:
                flash(domain_message, 'error')
                return redirect(url_for('auth.register'))
            
            # Debug print
            print(f"Registration attempt - Username: {username}, Email: {email}")
            
            if not username or not email:
                flash('Username and email are required', 'error')
                return redirect(url_for('auth.register'))
            
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'error')
                return redirect(url_for('auth.register'))
                
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return redirect(url_for('auth.register'))
            
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            
            # Debug print
            print(f"User created successfully - ID: {user.id}, Email: {user.email}")
            
            try:
                # Generate verification code and send email
                send_verification_email(user)
                flash('Registration successful! Please check your email for the verification code.', 'success')
            except Exception as e:
                print(f"Email sending error: {str(e)}")
                # If email sending fails, clear the verification code
                user.clear_verification_code()
                flash('Registration successful but we could not send the verification email. Please try resending the code.', 'warning')
            
            return redirect(url_for('auth.verify'))
            
        except OperationalError as e:
            print(f"Database error: {str(e)}")
            db.session.rollback()
            flash('Database connection error. Please try again.', 'error')
            return redirect(url_for('auth.register'))
            
    return render_template('auth/register.html')

@bp.route('/verify', methods=['GET', 'POST'])
def verify():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    # Clean up any stale verification codes
    User.cleanup_stale_codes()
        
    if request.method == 'POST':
        try:
            # Sanitize inputs
            email = sanitize_email(request.form.get('email', ''))
            code = sanitize_verification_code(request.form.get('code', ''))
            
            # Debug print
            print(f"Verification attempt - Email: {email}, Code: {code}")
            
            if not email or not code:
                flash('Email and verification code are required', 'error')
                return redirect(url_for('auth.verify'))
            
            user = User.query.filter_by(email=email).first()
            
            if not user:
                print(f"User not found for email: {email}")
                flash('Email not found', 'error')
                return redirect(url_for('auth.verify'))
            
            # Debug print
            print(f"User found - ID: {user.id}, Email: {user.email}, Verification Code: {user.verification_code}")
                
            if user.verify_code(code):
                user.is_verified = True
                user.clear_verification_code()
                db.session.commit()
                
                flash('Email verified successfully! You can now log in.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Invalid or expired verification code', 'error')
                
        except OperationalError as e:
            print(f"Database error: {str(e)}")
            db.session.rollback()
            flash('Database connection error. Please try again.', 'error')
            return redirect(url_for('auth.verify'))
            
    return render_template('auth/verify.html')

@bp.route('/resend-code', methods=['POST'])
def resend_code():
    try:
        # Sanitize email
        email = sanitize_email(request.form.get('email', ''))
        
        if not email:
            flash('Email is required', 'error')
            return redirect(url_for('auth.verify'))
            
        # Debug print
        print(f"Resend code attempt - Email: {email}")
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            print(f"User not found for email: {email}")
            flash('Email not found', 'error')
            return redirect(url_for('auth.verify'))
            
        if user.is_verified:
            flash('This account is already verified', 'error')
            return redirect(url_for('auth.login'))
            
        try:
            send_verification_email(user)
            flash('New verification code has been sent to your email', 'success')
        except Exception as e:
            print(f"Email sending error: {str(e)}")
            user.clear_verification_code()
            flash('Failed to send verification email. Please try again.', 'error')
            
        return redirect(url_for('auth.verify'))
        
    except OperationalError as e:
        print(f"Database error: {str(e)}")
        db.session.rollback()
        flash('Database connection error. Please try again.', 'error')
        return redirect(url_for('auth.verify'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        login = request.form.get('login', '')
        password = request.form.get('password', '')
        
        if not login or not password:
            flash('Both login and password are required', 'danger')
            return render_template('auth/login.html')
        
        # Check if login is email or username
        if '@' in login:
            # If it looks like an email, sanitize it as email
            login = sanitize_email(login)
            user = User.query.filter_by(email=login).first()
        else:
            # If it's a username, sanitize it as input
            login = sanitize_input(login)
            user = User.query.filter_by(username=login).first()
        
        if user and check_password_hash(user.password_hash, password):
            if not user.is_verified:
                flash('Please verify your email before logging in.', 'warning')
                return redirect(url_for('auth.verify'))
            
            if not user.is_approved:
                flash('Your account is pending approval. Please contact the administrator.', 'warning')
                return render_template('auth/login.html')
            
            login_user(user)
            return redirect(url_for('main.dashboard'))
        
        flash('Invalid login credentials', 'danger')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
