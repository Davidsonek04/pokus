
from flask import Blueprint, flash, render_template, redirect, g, request,url_for
from aplikace.db import get_db
from aplikace.auth import login_required

bp = Blueprint('update', __name__)

@bp.route('/update/<int:user_id>', methods=('GET', 'POST'))
@login_required
def insured_update(user_id):
    db = get_db()

    edit = db.execute(
        'SELECT * FROM users WHERE id = ? ', (user_id,)
    ).fetchone()
    #return render_template('update.html', editovat=editovat)

    user_id = edit['id']

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
            (updated_name, updated_surname, updated_email, updated_tel, updated_street_descriptive, updated_city, updated_zip_code, user_id,)
        )
        db.commit()

        flash(f"Pojištěnec {updated_name} {updated_surname} byl upraven")
            # Přesměrování po úspěšné aktualizaci
        return redirect(url_for('extract.list'))

    return render_template('update.html', edit=edit)

   
@bp.route('/delete/<int:user_id>', methods=('GET', 'POST'))
@login_required
def insured_delete(user_id):
    db = get_db()
    
    db.execute(
        'DELETE FROM users WHERE id = ?', (user_id,)
    )
    db.execute(
        'DELETE FROM insurance WHERE user_id = ?', (user_id,)
    )
    db.commit()
    flash(f"Pijštěnec byl smazán")
    return redirect(url_for('extract.list'))

#return redirect(url_for('insurance.list_insurance',user_id = user_id))
#UPDATE "uzivatele" SET "prijmeni" = 'Dolejší', "pocet_clanku" = "pocet_clanku" + 1 WHERE "uzivatele_id" = 1;
#DELETE FROM users WHERE id=2;