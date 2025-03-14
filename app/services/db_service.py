from app import db
from app.models.user import User
from app.models.work import Work
from app.models.artist import Artist

class DatabaseService:
    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def create_user(username, email, password,verification_token=None):
        user = User(
        username=username, 
        email=email,
        verification_token=verification_token,  # Save the token here
        is_verified=False  # Ensure new users are unverified by default
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_works_with_artists():
        return db.session.query(Work, Artist.artist_name).join(
            Artist, Work.artist_id == Artist.artist_id
        ).all()
    
    @staticmethod
    def get_user_by_verification_token(token):
        return User.query.filter_by(verification_token=token).first()

    @staticmethod
    def save_user(user):
        db.session.commit()
