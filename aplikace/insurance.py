from flask import Blueprint, session, g, render_template, request, url_for, redirect, flash
from aplikace.db import get_db

bp = Blueprint('insurance', __name__)

@bp.route('/insurance/<user_id>', methods=('GET', 'POST'))
def list_insurance(user_id):
    """_summary_
    """
    db = get_db()

    user = db.execute(
        'SELECT name, surname, email, id FROM users WHERE id = ?', (user_id,)
    ).fetchone()

    posts = db.execute(
        'SELECT * FROM insurance AS i '
        'JOIN users AS u ON u.id = i.user_id '
        'WHERE u.id = ?', (user_id,)
    ).fetchall()

    flash(user_id)
    return render_template('insurance_list.html', posts=posts, user_name=user)

@bp.route('/create_insurance/<user_id>', methods=('GET', 'POST'))
def create_insurance(user_id):

    if request.method == 'POST':
        insurance = request.form['insurance']
        amound = request.form['amound']
        subject = request.form['subject']
        valid_from = request.form['valid_from']
        valid_until = request.form['valid_until']
        user_id = request.form['user_id']

        db = get_db()
        error = None

        if (not insurance) or (not amound) or (not subject) or (not valid_from) or (not valid_until):
            error = 'Všechny poíčka jsou povinné!!'

        test = db.execute(
            'SELECT insurance FROM insurance WHERE insurance = ? AND user_id = ? ', (insurance, user_id,)
            ).fetchone()

        if test is not None:
            error = "Pojištění je již sjednáno!"

        if error is None:

            db.execute(
                    'INSERT INTO insurance (insurance, amound, subject, valid_from, valid_until, user_id) VALUES (?, ?, ?, ?, ?, ?)',
                    (insurance, amound, subject, valid_from, valid_until, user_id),
                )
            db.commit()
            error = "Pojištění bylo vytvořeno."
            return redirect(url_for('insurance.list_insurance', user_id = user_id))
        flash(error)
    return render_template('create_insurance.html', user_id = user_id)