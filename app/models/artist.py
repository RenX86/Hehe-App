from datetime import datetime
from app import db

class Artist(db.Model):
    __tablename__ = 'artists'
    artist_id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(50), unique=True, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship to works
    works = db.relationship('Work', backref='artist', lazy=True, cascade="all, delete")