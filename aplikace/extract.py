
from flask import Blueprint, render_template
from aplikace.auth import login_required
from aplikace.db import get_db

# Vytvoření Blueprint pro modul 'extract'
bp = Blueprint('extract', __name__)

@bp.route('/list', methods=('GET', 'POST'))
@login_required
def list():
    """Zobrazí seznam pojištěnců v aplikaci.

    Popis:
        Tato funkce získá seznam pojištěnců z databáze a zobrazí je na stránce.
        Na zobrazení seznamu pojištěnců je použit šablonovací systém Flask.
        
    Returns:
        flasl.Repsonse: HTML stránka seznam uživatelů.
    """
    db = get_db()
    users = db.execute(
        'SELECT * FROM users'
    ).fetchall()
    
    return render_template('extract/extract_list.html', users=users)