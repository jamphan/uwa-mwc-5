from flask import current_app, g

import trashyApp.database

def get_db():

    if 'db' not in g:

        if trashyApp.database.DATABASE_TYPE == 'json':
            db = trashyApp.database.jsonDb(path=trashyApp.database.DATABASE_PATH)

        g.db = db

    return g.db