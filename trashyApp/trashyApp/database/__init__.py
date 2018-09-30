DATABASE_PATH = 'data.json'
DATABASE_TYPE = 'json'

# Import the database interfaces
from trashyApp.database.BaseBinDb import BaseBinDb
from trashyApp.database.jsonDb import jsonDb
from trashyApp.database.sqliteDb import SQLite3Db

# Import the utils
from trashyApp.database.dbutils import get_db