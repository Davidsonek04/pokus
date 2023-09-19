
import functools
from flask import Blueprint, flash, g, render_template, request, session, url_for, redirect
from werkzeug.security import check_password_hash
from aplikace.db import get_db

# Vytvoření Blueprint pro modul 'auth'
bp = Blueprint('auth', __name__, url_prefix='/')

@bp.route('/', methods= ['GET', 'POST'])
def login():
    """Zobrazí stránku pro přihlášení a umožní přihlásit se.

    Returns:
        flask.Response: MLHT stránka s formulářem pro přihlášení.
    """
    
    # Kontrola jestli uživatel existuje.
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM administration WHERE email = ?', (email,)
        ).fetchone()

        # Ověření platnosti zadaných údajů.
        if user is None or not check_password_hash(user['password'], password):
            error = 'Nesprávné jméno nebo heslo'

        # Po zadání platných údajů se zobrazí výpis pojištěnců.
        if error is None:
            session.clear()
            session['email'] = user['email']
            
            return redirect(url_for('extract.list'))   
            
        flash(error)

    return render_template('auth/login.html')
    
# end def

@bp.route('/logout')
def logout():
    """Odhlásí uživatele a přesměruje na stránku pro přihlášení.

    Returns:
        flask.Response: MLHT stránka s formulářem pro přihlášení.
    """
    session.clear()
    return redirect(url_for('auth.login'))
# end def

@bp.before_app_request
def load_logged_in_user():
    """Načte informace o přihlášeném uživateli, pokud je přihlášený.
    
    Popis:
        Tato funkce je spuštěna před každým HTML požadavkem a zajišťuje, že informace
        o přihlášeném uživatteli jsou načteny do globální promenné g.user
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
    """Dekorátor vyžadující aby uživatel, před zobrazením určitého zobrazení, byl přihlášen.

    Args:
        viev (funkce): Dekorátor který se aplikuje na zobrazení.

    Returns:
        funkce: Dekorovaná funkce.
    """
    @functools.wraps(viev)
    def wraped_viev(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return viev(**kwargs)
    
    return wraped_viev
# end def
        