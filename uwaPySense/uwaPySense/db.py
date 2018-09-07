""" Handles all database connections

Changes:
    2018/09/07: Jamie Phan, Initial version
"""

import pyodbc

def get_db_sqlserver(server, database, trusted_connection = True, integrated_security = r'SSPI'):
    """ Returns an open connection to the database

    Args:
        server (str): the server address that the database is hosted on
        database (str): the name of the database to connect to
        trusted_connection (bool, default True): use trusted connection
        integrated security (bool ,default True): use integrated security

    Returns:
        pyodbc.Connection
    """

    if trusted_connection:
        trusted_connection_str = 'Yes'
    else:
        trusted_connection_str = 'No'

    connection_params = ["Driver={{{}}}".format("SQL Server"),
        "Server={}".format(server),
        "Database={}".format(database),
        "Trusted_Connection={}".format(trusted_connection_str),
        "Integrated Security={}".format(integrated_security)]

    connection_str = r";".join(connection_params)
    return pyodbc.connect(connection_str)

def close_cxn_sqlserver(cxn):
    """ Closes the connection to a SQL server instance. Do any cleanup here

    Args:
        cxn (pyodbc.Connection): The instance to close

    Returns:
        bool: True when the connection is closed, or if the parameter passed to
        begin with was not a connection
    """
    
    if isinstance(cxn, pyodbc.Connection):
        cxn.close()
        return True
    else:
        return True