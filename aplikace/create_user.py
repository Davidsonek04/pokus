
from flask import Blueprint, flash, g, render_template, redirect, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from aplikace.db import get_db

bp = Blueprint('create_user', __name__)

@bp.route('/user_create', methods=('GET', 'POST'))
def create_user():
    """
    Zobrazí formulář pro vytvoření nového uživatele a provede uložení do databáze.

    Returns:
        flask.Response: HTML stránka s formulářem pro vytvoření nového uživatele
        a provede uložení do databáze.
        
    """
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        
        if (not name) or (not surname) or (not email) or (not password):
            error = 'Všechny poíčka jsou povinné!!'
            
        test = db.execute(
            'SELECT email FROM administration WHERE email = ? ', (email,) 
            ).fetchone()
        
        if email == test:
            error = "Uživatel je již zaregistrován!"
            
        if error is None:
                db.execute(
                    "INSERT INTO administration (email, password, name, surname) VALUES (?, ?, ?, ?)",
                    (email, generate_password_hash(password), name, surname),
                )
                db.commit()
                return redirect(url_for('extract.list'))
        flash(error)
    return render_template('create_user.html')