
import sqlite3
import click
from flask import current_app, g

def get_db():
    """
    Purpose: přístup k databázi
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        
    return g.db
    
# end def

def close_db(e = None):
    """
    Purpose: ukončuje práci s databází
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()
    
# end def
def init_db():
    """
    Purpose: 
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
# end def

@click.command('init-db')
def init_db_command():
    """
    Purpose: Vymaže existující data a vytvoří nové tabulky
    """
    init_db()
    click.echo('Inicializuji databázi')
# end def

def init_app(app):
    """
    Purpose: 
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
# end def