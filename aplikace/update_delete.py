
from flask import Blueprint, flash, render_template, redirect, g, request,url_for
from aplikace.db import get_db
from aplikace.auth import login_required

bp = Blueprint('update', __name__)

@bp.route('/update/<user_id>', methods=('GET', 'POST'))
@login_required
def insured_update(user_id):
    db = get_db()

    edit = db.execute(
        'SELECT * FROM users WHERE id = ? ', (user_id,)
    ).fetchone()
    #return render_template('update.html', editovat=editovat)

    id = edit['id']

    if request.method == 'POST':
            # Získání hodnot z formuláře
            updated_name = request.form.get('name')
            updated_surname = request.form.get('surname')
            updated_email = request.form.get('email')
            updated_tel = request.form.get('tel')
            updated_street_descriptive = request.form.get('street_descriptive')
            updated_city = request.form.get('city')
            updated_zip_code = request.form.get('zip_code')
            #user_id = request.form.get('user_id')

    if updated_email != None:

        # Aktualizace hodnot v databázi
        db.execute(
            'UPDATE users SET name = ?, surname = ?, email = ?, tel = ?, street_descriptive = ?, city = ?, zip_code = ? WHERE id = ?',
            (updated_name, updated_surname, updated_email, updated_tel, updated_street_descriptive, updated_city, updated_zip_code, id,)
        )
        db.commit()

        flash(f"Pojištěnec {updated_name} {updated_surname} byl upraven")
            # Přesměrování po úspěšné aktualizaci
        return redirect(url_for('extract.list'))

    return render_template('update.html', edit=edit)

   
@bp.route('/delete/<user_id>', methods=('GET', 'POST'))
@login_required
def insured_delete(user_id):
    db = get_db()
    
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.execute('DELETE FROM insurance WHERE user_id = ?', (user_id,))
    db.commit()
    flash(f"Pijštěnec byl smazán")
    return redirect(url_for('extract.list'))

#return redirect(url_for('insurance.list_insurance',user_id = user_id))
#UPDATE "uzivatele" SET "prijmeni" = 'Dolejší', "pocet_clanku" = "pocet_clanku" + 1 WHERE "uzivatele_id" = 1;
#DELETE FROM users WHERE id=2;

@bp.route('/update_insurance/<insurance_id>', methods=('GET', 'POST'))
@login_required
def update_insurance(insurance_id):
    user_name = request.args.get('user_name')
    db = get_db()

    insurance_edit = db.execute(
        'SELECT * FROM insurance WHERE id = ? ', (insurance_id,)
    ).fetchone()
    

    insurance_id = insurance_edit['id']

    if request.method == 'POST':
            # Získání hodnot z formuláře
            updated_insurance = request.form.get('insurance')
            updated_amount = request.form.get('amount')
            updated_subject = request.form.get('subject')
            updated_valid_from = request.form.get('valid_from')
            updated_valid_until = request.form.get('valid_until')
            
            

    if updated_insurance != None:

        # Aktualizace hodnot v databázi
        db.execute(
            'UPDATE insurance SET insurance = ?, amount = ?, subject = ?, valid_from = ?, valid_until = ? WHERE id = ?',
            (updated_insurance, updated_amount, updated_subject, updated_valid_from, updated_valid_until, insurance_id,)
        )
        db.commit()

        flash(f"Pojištění: {updated_insurance} - {updated_subject} bylo upraveno!")
            # Přesměrování po úspěšné aktualizaci
        
        return redirect(url_for('insurance.list_insurance',user_id=user_name))

    return render_template('insurance_update.html', insurance_edit=insurance_edit, insurance_d=insurance_id)

@bp.route('/delete_insurance/<insurance_id>', methods=('GET', 'POST'))
@login_required
def insurance_delete(insurance_id):
    user_name = request.args.get('user_name')
    db = get_db()
    insurance_data = db.execute('SELECT * FROM insurance WHERE id = ?', (insurance_id,)).fetchone()
    db.execute('DELETE FROM insurance WHERE id = ?', (insurance_id,))
    db.commit()
    flash(f"Pojštění: {insurance_data['insurance']} bylo smazáno")
    return redirect(url_for('insurance.list_insurance',user_id=user_name))
    
    