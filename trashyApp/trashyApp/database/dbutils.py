from flask import current_app, g

from . import jsonDb, DATABASE_PATH, DATABASE_TYPE

def get_db():

    if 'db' not in g:

        if DATABASE_TYPE == 'json':
            db = jsonDb(path=DATABASE_PATH)

        g.db = db

    return g.db