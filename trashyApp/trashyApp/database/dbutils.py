from flask import current_app, g

from . import jsonDb
from ..conf import AppConfig

def get_db():

    if 'db' not in g:

        if AppConfig.DATABASE_TYPE == 'json':
            db = jsonDb(path=AppConfig.DATABASE_PATH)

        g.db = db

    return g.db