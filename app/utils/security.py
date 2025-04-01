import re
from html import escape

def sanitize_input(input_str):
    """Sanitize input string by removing potentially harmful characters."""
    if not input_str:
        return ""
    # Remove any HTML tags
    input_str = re.sub(r'<[^>]+>', '', input_str)
    # Remove any script tags and their content
    input_str = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', input_str, flags=re.IGNORECASE)
    # Remove any SQL keywords
    input_str = re.sub(r'(?i)(select|insert|update|delete|drop|union|alter|create|truncate|backup|restore)', '', input_str)
    # Remove any special characters except basic punctuation
    input_str = re.sub(r'[^a-zA-Z0-9\s.,!?-]', '', input_str)
    # Trim whitespace
    input_str = input_str.strip()
    return input_str

def sanitize_email(email):
    """Sanitize email address."""
    if not email:
        return ""
    # Remove any HTML tags
    email = re.sub(r'<[^>]+>', '', email)
    # Remove any script tags and their content
    email = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', email, flags=re.IGNORECASE)
    # Remove any special characters except email-valid characters
    email = re.sub(r'[^a-zA-Z0-9@._+-]', '', email)
    # Trim whitespace
    email = email.strip().lower()
    return email

def validate_email_domain(email):
    """Validate that the email domain is allowed (Gmail or ProtonMail)."""
    if not email or '@' not in email:
        return False, "Invalid email format"
    
    allowed_domains = ['gmail.com', 'protonmail.com', 'proton.me', 'pm.me']
    domain = email.split('@')[1].lower()
    
    if domain not in allowed_domains:
        return False, f"Only Gmail and ProtonMail email addresses are allowed. Got: {domain}"
    
    return True, "Email domain is valid"

def validate_password(password):
    """Validate password strength."""
    if not password:
        return False, "Password cannot be empty"
    
    # Check minimum length
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    # Check for uppercase letters
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    # Check for lowercase letters
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    # Check for numbers
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    # Check for special characters
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"

def sanitize_verification_code(code):
    """Sanitize verification code."""
    if not code:
        return ""
    # Remove any non-digit characters
    code = re.sub(r'[^0-9]', '', code)
    # Limit to 6 digits
    code = code[:6]
    return code 