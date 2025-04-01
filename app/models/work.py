from datetime import datetime
from app import db

class Work(db.Model):
    __tablename__ = 'works'
    
    work_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer)
    code = db.Column(db.String(50), unique=True)
    source = db.Column(db.String(50))
    url = db.Column(db.String(500))  # New column for external URLs
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id', ondelete='CASCADE'))
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship with Artist
    artist = db.relationship('Artist', backref=db.backref('works', lazy=True))
    
    def __repr__(self):
        return f'<Work {self.title}>' 