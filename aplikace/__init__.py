import os
from flask import Flask
from . import db, auth,  extract#, create

def create_app(test_config=None):
    """
    Purpose: vytvoří a nastavý aplikaci
    """
    # vytvoření a nastavení app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'databaze.db'),
    )
    
    # registrace Blueprintů
    app.register_blueprint(auth.bp)
    app.register_blueprint(extract.bp)
    #app.register_blueprint(create.bp)

    app.add_url_rule('/', view_func=auth.login)
    
    db.init_app(app)

    if test_config is None:
        # načtěte konfiguraci instance, pokud existuje, když netestujete
        app.config.from_pyfile("config.py", silent=True)
    else:
        # načtěte testovací konfiguraci, pokud byla zadána
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    return app
    
# end def