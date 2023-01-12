import mysql.connector as cnctr
from mysql.connector import errorcode
import pandas as pd
 
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


def createHeader(tbl_name,cols,header_name):
    '''
    nb : current limitation - this doesn't seem to place the carrot symbols where we want them
    '''
    sql_header = f'''{header_name} INTO `{tbl_name}` (`{"`, `".join(cols)}`) VALUES '''
    return sql_header


def insertOne(sql_in,record):
    '''
    add just one
        nb : current limitation - works for just four columns
        nb " current limitation - assumes that the contents of data frame / data are formatted for insert
    '''
    if type(record) == pd.core.series.Series:
        record = record.to_list()
    sql = sql_in+f'''\n ({",".join([str(rec) for rec in record])}),'''
    return sql

def insertMany(data, tbl_name, header_name):
    '''
    add many data
    data : pandas df or iterable containing data (i.e. dictionary)
    tbl_name : name of table to do action on in db
    header_name : action to take (i.e. SELECT, INSERT, etc...)
    '''
    try:
        # to do - convert dictionary to dataframe if need be
        sql = createHeader(tbl_name=tbl_name,cols=data.columns,header_name=header_name)
        for i in range(len(data)):
            record = data.iloc[i]
            sql = insertOne(sql_in=sql,record=record)
        sql = (sql[:-1]+';').replace('nan','NULL')
    except cnctr.Error as e: 
        print(e)
    return sql