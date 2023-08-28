
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from aplikace.auth import login_required
from aplikace.db import get_db

bp = Blueprint('extract', __name__)

@bp.route('/list')
def list():
    """
    _summary_
    """
    db = get_db()
    posts = db.execute(
        'SELECT name, surname, email FROM users'
    ).fetchall()
    return render_template('extract/extract_list.html', posts=posts)
