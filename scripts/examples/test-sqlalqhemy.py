# %%
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pandas as pd
# %%

config = {
  'user': 'root',
  'password': '300667',
  'host': '127.0.0.1',
  'port': '5432', 
  'raise_on_warnings' : True,
  'db_name' : "rivereyes"
  }

# 'dialect+drive://username:password@host:port/database' 
engine_path = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}/{config['db_name']}"
print(engine_path)
engine = create_engine(engine_path)
# %%
with engine.connect() as conn:
    statement = text(''' SELECT * FROM rivermile WHERE (rm < :x) AND (rm > :y) LIMIT 10;''')
    param = {"x": 60, "y": 50}

    # Option 1
    rs = conn.execute(statement, param)    
    for row in rs:
        print(row)

    # Option 2
    df = pd.read_sql_query(statement, params=param, con=conn)
    print(df)

# %%

