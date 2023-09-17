
from flask import Blueprint, render_template
from aplikace.auth import login_required
from aplikace.db import get_db

bp = Blueprint('extract', __name__)

@bp.route('/list', methods=('GET', 'POST'))
@login_required
def list():
   
    db = get_db()
    users = db.execute(
        'SELECT * FROM users'
    ).fetchall()
    
    return render_template('extract/extract_list.html', users=users)