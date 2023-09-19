from flask import Blueprint, session, g, render_template, request, url_for, redirect, flash
from aplikace.db import get_db
from aplikace.auth import login_required


# Vytvoření Blueprint pro modul 'insurance'
bp = Blueprint('insurance', __name__)

@bp.route('/insurance/<user_id>', methods=('GET', 'POST'))
@login_required
def list_insurance(user_id):
    """Zobrazí seznam pojištění pro konkrétního pojištěnce.
        
    Args:
        user_id (int): ID pojištěnce, pro kterého se má zobrazit seznam pojištění.
        
    Returns:
        flask.Response: HTML stránka se seznamem pojištění.
    """
    db = get_db()

    user = db.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()

    posts = db.execute(
        'SELECT * FROM insurance AS i '
        'JOIN users AS u ON u.id = i.user_id '
        'WHERE u.id = ?', (user_id,)
    ).fetchall()

    page_title = f"Výpis pojištění uživatele {user['name']} {user['surname']}"
    return render_template('insurance_list.html', posts=posts, user_name=user, user=user, page_title=page_title)

@bp.route('/create_insurance/<user_id>', methods=('GET', 'POST'))
@login_required
def create_insurance(user_id):
    """Vytvoří nové pojištění pro konkrétního pojištěnce.

    Args:
        user_id (int): ID pojištěnce, pro ketrého se má vytvořit pojištění.

    Returns:
        _type_: HTML stránka pro vytvoření pojištění.
    """

    if request.method == 'POST':
        insurance = request.form['insurance']
        amount = request.form['amount']
        subject = request.form['subject']
        valid_from = request.form['valid_from']
        valid_until = request.form['valid_until']
        user_id = request.form['user_id']

        db = get_db()
        chyba = None

        if (not insurance) or (not amount) or (not subject) or (not valid_from) or (not valid_until):
            chyba = 'Všechny poíčka jsou povinné!!'

        test = db.execute(
            'SELECT insurance FROM insurance WHERE insurance = ? AND user_id = ? ', (insurance, user_id,)
            ).fetchone()

        if test is not None:
            chyba = "Pojištění je již sjednáno!"

        if  chyba is None:

            db.execute(
                    'INSERT INTO insurance (insurance, amount, subject, valid_from, valid_until, user_id) VALUES (?, ?, ?, ?, ?, ?)',
                    (insurance, amount, subject, valid_from, valid_until, user_id),
                )
            db.commit()
            chyba = "Pojištění bylo vytvořeno."
            return redirect(url_for('insurance.list_insurance', user_id = user_id))
        flash(chyba)
    return render_template('create_insurance.html', user_id = user_id)

    
@bp.route('/insurance_detail/<user_name_id>/<posts>', methods=('GET', 'POST'))
@login_required
def insurance_detail(user_name_id, posts):
    """Zobrazí detaily konkrétního pojištění.

    Args:
        user_name_id (int): ID pojištěnce, pro kterého se zobrazují detaily pojištění.
        posts (int): ID pojištěni, které se má zobrazit.

    Returns:
        flask.Response: HTML stránka s detaily pojištění.
    """

    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_name_id,)).fetchone()
    post = db.execute('SELECT * FROM insurance WHERE id = ?', (posts,)).fetchall()
    page_title = f"Detajl pojištění uživatele {user['name']} {user['surname']}"
    return render_template('insurance_detail.html', user_name=user, posts=post, page_title=page_title)
    