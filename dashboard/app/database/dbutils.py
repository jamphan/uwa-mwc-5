from flask import current_app, g

import app.database

def get_db():

    if 'db' not in g:

        if app.database.DATABASE_TYPE == 'json':
            db = app.database.jsonDb(path=app.database.DATABASE_PATH)

        g.db = db

    return g.db