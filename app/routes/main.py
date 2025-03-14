from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.db_service import DatabaseService


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    works_with_artists = DatabaseService.get_works_with_artists()
    return render_template('index.html', works=works_with_artists)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')