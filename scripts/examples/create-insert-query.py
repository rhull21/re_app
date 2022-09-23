# %%
import sys
sys.path.append("../")
import mysql.connector as cnctr
from utils.helpers import *
from utils.sqlreader import *
from __future__ import print_function

# %% globals
config = {
  'user': 'root',
  'password': '300667',
  'host': '127.0.0.1',
  'raise_on_warnings' : True
  }

db_name = "testing" 
TABLES = {}

data_path = None # 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/rivereyes/' # '../data/'

cnx = cnctr.connect(**config)
crsr = cnx.cursor()
createDB(db_name, crsr)
cnx.database = db_name

# %% tables
TABLES[db_name] = (
f'''CREATE TABLE IF NOT EXISTS {db_name} (
  id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  rm DECIMAL (4,1) NOT NULL UNIQUE,
  position POINT NOT NULL SRID 0,
  latlong POINT SRID 4326,
  SPATIAL INDEX(position)
) ENGINE=INNODB;'''
)

for table_name in TABLES:
    table_description = TABLES[table_name]
    addTable(table_name, table_description, crsr)

# %% insert data
'''Option 1'''
# for table_name in TABLES:
#     query = f'''LOAD DATA INFILE "{data_path}{table_name}.txt" INTO TABLE {table_name};'''
#     print(query)
#     crsr.execute(query)
#     cnx.commit()

'''Option 2'''
query = (f'''INSERT INTO {table_name}
                  (rm, position) 
                      VALUES 
                  (%s, ST_GeomFromText('POINT(0 %s)'))''')

data = (0, 0)
crsr.execute(query,data)
cnx.commit()

# %% query data
'''Option 1'''
query = (f'''SELECT * FROM {table_name}
         WHERE id BETWEEN %s AND %s''')

crsr.execute(query, (-1, 1))
for out in crsr:
  print(out)

'''Option 2'''


# %% 
delQuery = f"DROP DATABASE {db_name}"
executeSQL(delQuery,crsr)

crsr.close()
cnx.close()



# %%
