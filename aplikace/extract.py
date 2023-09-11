
from flask import Blueprint, flash, g, redirect, session, render_template, request, url_for
from werkzeug.exceptions import abort
from aplikace.auth import login_required
from aplikace.db import get_db


bp = Blueprint('extract', __name__)

@bp.route('/list', methods=('GET', 'POST'))
def list():
    """
    _summary_ : Po přihlášení uživatele jako admina!!
    """
    db = get_db()
    users = db.execute(
        'SELECT * FROM users'
    ).fetchall()
    return render_template('extract/extract_list.html', users=users)

# TODO Připraveno na admin / user 
# @bp.route('/list_one', methods=('GET', 'POST'))
# def list_one():
#     """_summary_ : Po přihlášení uživatele jako pojištěnca!!!
#     """


#     email = session.get('email')
#     db = get_db()
#     users = db.execute(
#         'SELECT name, surname, email, id FROM users WHERE email = ?', (email,)
#     )
#     return render_template('extract/extract_list.html', users=users)