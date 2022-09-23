import mysql.connector as cnctr
from utils.helpers import executeSQL



def _takeSQLfromfile(filename):
    '''
    Take any hardcoded SQL statement in file
    '''
   # Open and read the file as a single buffer
    with open(filename) as fd:
        next(fd)
        sqlFile = fd.read()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    return sqlCommands

def SQLfromfile(filename,crsr,verbose=False,execute=True):
    '''
    execute queries in file in Python
    https://stackoverflow.com/questions/19472922/reading-external-sql-script-in-python
    '''

    # Parsed SQL statements
    sqlCommands = _takeSQLfromfile(filename)

    if execute:
        # Execute every command from the input file
        for command in sqlCommands:
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands   
            executeSQL(command,crsr)

    if verbose:
        return sqlCommands