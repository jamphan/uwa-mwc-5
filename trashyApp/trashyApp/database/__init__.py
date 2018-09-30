DATABASE_PATH = 'data.json'
DATABASE_TYPE = 'json'

# Import the database interfaces
from .BaseBinDb import BaseBinDb
from .jsonDb import jsonDb
from .sqliteDb import SQLite3Db

# Import the utils
from .dbutils import get_db