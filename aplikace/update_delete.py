
from flask import Blueprint, flash, render_template, redirect, g, request,url_for
from aplikace.db import get_db
from aplikace.auth import login_required

bp = Blueprint('update', __name__)

@bp.route('/update/<int:user_id>', methods=('GET', 'POST'))
@login_required
def insured_update(user_id):
    db = get_db()

    editovat = db.execute(
        'SELECT * FROM users WHERE id = ? ', (user_id,)
    ).fetchone()
    return render_template('update.html', editovat=editovat)
   
    


#UPDATE "uzivatele" SET "prijmeni" = 'Dolejší', "pocet_clanku" = "pocet_clanku" + 1 WHERE "uzivatele_id" = 1;
