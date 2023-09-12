import functools
from flask import Blueprint, flash, g, render_template, redirect, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from aplikace.db import get_db
from aplikace.auth import login_required

bp = Blueprint('create', __name__)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
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
        
        if (not name) or (not surname) or (not email) or (not tel) or (not city) or (not zip_code) or (not street_descriptive):
            error = 'Všechny poíčka jsou povinné!!'
            
        test = db.execute(
            'SELECT email FROM users WHERE email = ? ', (email,) 
            ).fetchone()
        
        if test is not None:
            error = "Uživatel je již zaregistrován!"
            
        if error is None:
                db.execute(
                    "INSERT INTO users (email, name, surname, tel, street_descriptive, city, zip_code) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (email, name, surname, tel, street_descriptive, city, zip_code),
                )
                db.commit()
                error = "Pojištěnec byl uložen."
                return redirect(url_for('extract.list'))
        flash(error)
    return render_template('create.html')