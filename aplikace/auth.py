
import functools
from flask import Blueprint, flash, g, render_template, request, session, url_for, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from aplikace.db import get_db

# toto je opsaná 
bp = Blueprint('auth', __name__, url_prefix='/')

@bp.route('/', methods= ['GET', 'POST'])
def login():
    """
    Purpose: přihlášení
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM administration WHERE email = ?', (email,)
        ).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            error = 'Nesprávné jméno nebo heslo'

        if error is None:
            session.clear()
            session['email'] = user['email']
            if user['name'] == 'David':
                return redirect(url_for('extract.list'))    # TODO vytvořit extract.list
            return redirect(url_for('extract.list_one'))
        flash(error)

    return render_template('auth/login.html')
    
# end def

@bp.route('/logout')        # NOTE nevím jestli je routa správně
def logout():
    """
    Purpose: 
    """
    session.clear()
    return redirect(url_for('auth.login'))
# end def

@bp.before_app_request
def load_logged_in_user():
    """
    Purpose: 
    """
    user_id = session.get('email')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM administration WHERE email = ?', (user_id,)
        ).fetchone()
    
# end def

def login_required(viev):
    """
    Purpose: 
    """
    @functools.wraps(viev)
    def wraped_viev(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return viev(**kwargs)
    
    return wraped_viev
# end def
        