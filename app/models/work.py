from datetime import datetime
from app import db

class Work(db.Model):
    __tablename__ = 'works' 
    work_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    code = db.Column(db.String(50), unique=True, nullable=True)
    source = db.Column(db.String(50), nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id', ondelete='CASCADE'), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)