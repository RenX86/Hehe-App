from app import create_app, db
from app.models import User, Work, Artist

app = create_app()

@app.cli.command("create_db")
def create_db():
    """Create database tables from SQLAlchemy models."""
    db.create_all()
    print("Database tables created!")

if __name__ == '__main__':
    app.run(debug=True)
