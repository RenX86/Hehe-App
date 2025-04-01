from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.work import Work
from app.models.artist import Artist
from sqlalchemy import desc, and_, func
from collections import defaultdict
from sqlalchemy.orm import joinedload, load_only
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('main/dashboard.html')
    return render_template('main/home.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html')

@bp.route('/sauce')
@login_required
def sauce():
    page = request.args.get('page', 1, type=int)
    per_page = 50  # Number of works per page
    
    # Get query parameters for filtering
    min_rating = request.args.get('min_rating', type=int)
    max_rating = request.args.get('max_rating', type=int)
    source = request.args.get('source')
    artist = request.args.get('artist')

    # Start with optimized base query with only necessary columns
    query = Work.query.options(
        load_only(Work.title, Work.code, Work.source, Work.rating, Work.url),
        joinedload(Work.artist).load_only(Artist.artist_name)
    ).join(Artist)

    # Apply filters if provided
    if min_rating is not None:
        query = query.filter(Work.rating >= min_rating)
    if max_rating is not None:
        query = query.filter(Work.rating <= max_rating)
    if source:
        query = query.filter(Work.source.ilike(f'%{source}%'))
    if artist:
        query = query.filter(Artist.artist_name.ilike(f'%{artist}%'))

    # Get total count for pagination
    total = query.count()
    
    # Add ordering and pagination
    works = query.order_by(Artist.artist_name.asc(), desc(Work.date_added))\
                .offset((page - 1) * per_page)\
                .limit(per_page)\
                .all()
    
    # Group works by artist
    works_by_artist = defaultdict(list)
    for work in works:
        artist_name = work.artist.artist_name if work.artist else 'Unknown'
        works_by_artist[artist_name].append(work)
    
    # Calculate total pages
    total_pages = (total + per_page - 1) // per_page
    
    return render_template(
        'main/sauce.html',
        works_by_artist=works_by_artist,
        page=page,
        total_pages=total_pages,
        total_works=total
    )

@bp.route('/sauce/<int:work_id>')
@login_required
def work_detail(work_id):
    work = Work.query.get_or_404(work_id)
    return render_template('main/work_detail.html', work=work)

@bp.route('/update_urls', methods=['GET'])
@login_required
def update_urls():
    """Utility endpoint to update URLs for testing"""
    try:
        # Update first 10 works with example URLs
        works = Work.query.limit(10).all()
        
        for i, work in enumerate(works):
            # Create different example URLs
            if i % 3 == 0:
                work.url = f"https://example.com/work/{work.code}"
            elif i % 3 == 1:
                work.url = f"https://source.com/{work.source.lower().replace(' ', '-')}/{work.work_id}"
            else:
                work.url = f"https://artist.com/{work.artist.artist_name.lower().replace(' ', '-')}/{work.title.lower().replace(' ', '-')}"
        
        db.session.commit()
        flash('URLs updated successfully for testing', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating URLs: {str(e)}', 'danger')
    
    return redirect(url_for('main.sauce'))
