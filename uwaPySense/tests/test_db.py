""" Test class for database queries and connections

Changes:
    2018/09/07: Jamie Phan, Initial version
"""
import pytest

SERVER = ''
DATABASE = ''

from uwaPySense import db

def test_getDbSqlserver():
    """ Use an actual SQL server instance to test this. Checks that a 
    connection is made
    """

    import pyodbc
    assert (isinstance(db.get_db_sqlserver(SERVER,DATABASE),
                                pyodbc.Connection))
