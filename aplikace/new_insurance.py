
from flask import Blueprint, flash, g, render_template, redirect, request, url_for
from aplikace.db import get_db

bp = Blueprint('new_insurance', __name__)

@bp.route('/new_insurance', methods=('GET', 'POST'))
def create_insurance():
        

    if request.method == 'POST':
        insurance = request.form['insurance']
        amound = request.form['amound']
        subject = request.form['subject']
        valid_from = request.form['valid_from']
        valid_until = request.form['valid_until']
        user_id = request.form.get('user_id')
        
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
            return redirect(url_for('insurance.list_insurance'))
        flash(error)
    return render_template('create_insurance.html')