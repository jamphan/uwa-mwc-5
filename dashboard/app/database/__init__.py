DATABASE_PATH = 'app/data.json'
DATABASE_TYPE = 'json'

# Import the database interfaces
from app.database.BaseBinDb import BaseBinDb
from app.database.jsonDb import jsonDb
from app.database.sqliteDb import SQLite3Db

# Import the utils
from app.database.dbutils import get_db