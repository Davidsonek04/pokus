
from flask import Blueprint, flash, g, render_template, redirect, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from aplikace.db import get_db
from aplikace.auth import login_required

# Vytvoření Blueprint pro modul 'create'
bp = Blueprint('create', __name__)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Zobrazí formulář pro vytvoření nového pojištěnce a uloží ho do databáze.

    Returns:
        flask.Response: HTML stránka s formulářem na vytvoření nového pojištěnce 
        a nebo na přesměrování zpět na seznam pojištěnců
    """
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        tel = request.form['tel']
        street_descriptive = request.form['street_descriptive']
        city = request.form['city']
        zip_code = request.form['zip_code']
        
        db = get_db()
        error = None
        
        # Kontrola zda jsou vyplněny všechny políčka formuláře.
        if (not name) or (not surname) or (not email) or (not tel) or (not city) or (not zip_code) or (not street_descriptive):
            error = 'Všechny poíčka jsou povinné!!'
            
        test = db.execute(
            'SELECT email FROM users WHERE email = ? ', (email,) 
            ).fetchone()
        
        # Kontrola jestli už pojištěnec není vytvořen.
        if test is not None:
            error = "Uživatel je již zaregistrován!"
            
        # Vytvoří pojištěnca a uloží do databáze.
        if error is None:
                db.execute(
                    "INSERT INTO users (email, name, surname, tel, street_descriptive, city, zip_code) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (email, name, surname, tel, street_descriptive, city, zip_code),
                )
                db.commit()
                error = "Pojištěnec byl uložen."
                flash(error)
                return redirect(url_for('extract.list'))
        flash(error)
    return render_template('create.html')