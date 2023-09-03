from flask import Blueprint, session, g, render_template, request, url_for, redirect
from aplikace.db import get_db

bp = Blueprint('insurance', __name__)

@bp.route('/insurance', methods=('GET', 'POST'))
def list_insurance():
    """_summary_
    """
    db = get_db()
    
    u_mail = request.form.get('user_mail')
    #u_id = request.form.get('id')
    #email = session.get('name')
    
    user_name = db.execute(
        'SELECT name, surname, email, id FROM users WHERE email = ?', (u_mail,)
    ).fetchone()

    u_id = user_name['id']

    # if email == 'David':
    #     posts = db.execute(
    #         'SELECT * FROM insurance AS i '
    #         'JOIN users AS u ON u.id = i.user_id '
    #         'WHERE u.id = ?', (u_id,)            
    #     ).fetchall()

    posts = db.execute(
        'SELECT * FROM insurance AS i '
        'JOIN users AS u ON u.id = i.user_id '
        'WHERE u.id = ?', (u_id,)
    ).fetchall()

    return render_template('insurance_list.html', posts=posts, user_name=user_name)