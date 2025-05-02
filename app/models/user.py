from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from app import db, login_manager
from datetime import datetime, timedelta
import random

bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6))
    verification_code_expiry = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_verification_code(self):
        """Generate a 6-digit verification code and set its expiry."""
        self.verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.verification_code_expiry = datetime.utcnow() + timedelta(minutes=10)
        db.session.commit()
        return self.verification_code

    def verify_code(self, code):
        """Verify the provided code."""
        if not self.verification_code or not self.verification_code_expiry:
            return False
        if self.verification_code_expiry < datetime.utcnow():
            return False
        return self.verification_code == code

    def clear_verification_code(self):
        """Clear the verification code and its expiry."""
        self.verification_code = None
        self.verification_code_expiry = None
        db.session.commit()

    @classmethod
    def cleanup_stale_codes(cls):
        """Clean up any verification codes that have expired."""
        expired_users = cls.query.filter(
            cls.verification_code.isnot(None),
            cls.verification_code_expiry < datetime.utcnow()
        ).all()
        
        for user in expired_users:
            user.clear_verification_code()

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))