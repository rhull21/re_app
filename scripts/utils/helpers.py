import mysql.connector as cnctr
from mysql.connector import errorcode
 
def createDB(db_name, crsr):
    '''
    see if db exists, else throw error
    '''
    try: 
        crsr.execute(f"CREATE DATABASE {db_name}")
    except cnctr.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def addTable(table_name, table_description, crsr):
    '''
    add a table
    '''
    try:
        print("Creating table {}: ".format(table_name), end='')
        crsr.execute(table_description)
    except cnctr.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

def executeSQL(sqlcommand,crsr):
    try:
        crsr.execute(sqlcommand)
    except cnctr.Error as err:
        print(err.msg)
    else:
        print("OK")


def insertOne():
    '''
    add just one
    '''
    return None 

def insertMany():
    '''
    add many data
    '''
    return None