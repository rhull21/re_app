# %%
import mysql.connector as cnctr
from utils.helpers import *
from utils.sqlreader import *
import pandas as pd 
from utils.accessetc import read_db_info

# %% globals

db_info_dir = '/home/quinn/re_app_dev/etc/db_info.json' # use absolute paths here
config = read_db_info(db_info_dir)

sql_path = '../../data/imports/2023_data/'
fname = 'table_dryness.csv'

#  Define connection, prepare cursor, create database
cnx = cnctr.connect(**config)
crsr = cnx.cursor()
# createDB(db_name, crsr)
# cnx.database = db_name

# # %% 1. Create Tables
# SQLfromfile(sql_path+'create.sql',crsr)

# # %% 2. Insert Data
# SQLfromfile(sql_path+fname,crsr)
# cnx.commit()

# # # %% 3. Create functions
# # SQLfromfile(sql_path+'functions.sql',crsr)
# # cnx.commit()

# # # %% 4. Create Views
# # SQLfromfile(sql_path+'views.sql',crsr)
# # cnx.commit()

# # # %% 5. Actively read and visualize queries
# # # qry = SQLfromfile(sql_path+'drylength.sql',crsr,verbose=True,execute=False)[0]
# # qry = '''SELECT * FROM observation WHERE obstype='Remnant Pool';'''

# # df = pd.read_sql_query(qry,con=cnx)
# # print(df)

# # SQLfromfile(sql_path+'query.sql',crsr)
# # for out in crsr:
# #   print(out)

# %% 6. Close
crsr.close()
cnx.close()