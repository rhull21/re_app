# This script used to create a color plot of dry year

# %%
import mysql.connector as cnctr
from utils.helpers import *
from utils.sqlreader import *
from __future__ import print_function
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# %% globals
config = {
  'user': 'root',
  'password': '300667',
  'host': '127.0.0.1',
  'raise_on_warnings' : True
  }

db_name = "rivereyes" 
sql_path = '../sql/'


# %% Define connection, prepare cursor, create database
cnx = cnctr.connect(**config)
crsr = cnx.cursor()
cnx.database = db_name

# %% extract views from db
# view 1 - dry_length
# view 2 - river mile, discretized by 0.5, with features joined
possyr = 2021
mindat, maxdat = datetime(possyr,6,1), datetime(possyr,10,31)
minrm, maxrm = 53.5, 164
qry_dry = f'''SELECT *, round((floor(((rm_down * 2) + 0.5)) / 2),1) AS `rm_down_rd`, round((floor(((rm_up * 2) + 0.5)) / 2),1) AS `rm_up_rd` FROM dry_length WHERE YEAR(dat) = {possyr};'''
qry_rm_feat = f'''	SELECT * FROM feature_rm;'''
df_dry = pd.read_sql_query(qry_dry,con=cnx)
df_rm_feat = pd.read_sql_query(qry_rm_feat,con=cnx)

# %% loop through all dates

cols = pd.date_range(mindat,maxdat,freq='d').date
df_all = pd.concat(
    [
        df_rm_feat,
        pd.DataFrame(
            np.zeros((len(df_rm_feat),len(cols))), 
            index=df_rm_feat.index, 
            columns=cols, 
            dtype=int
        )
    ], axis=1
)

# %% create the figure
for col in cols: 
    df_temp = df_dry[['rm_down_rd', 'rm_up_rd']][df_dry['dat']==col]
    for i in range(len(df_temp)):
        df_all.loc[(df_all['rm-rounded'] <= df_temp['rm_up_rd'].iloc[i]) & (df_all['rm-rounded'] >= df_temp['rm_down_rd'].iloc[i]),col] = 1

# %%
df_all.to_csv("../../data/shapefile_2021rm/rivereyes2021.csv")

#%% create the image
fig, ax = plt.subplots(figsize=(20,10))

ind_col = [x for x in range(0,len(cols),14)]
ind_row = df_all['feature'].dropna().index[::3]
ind_col_names = cols[ind_col]
ind_row_names = df_all['feature'].dropna()[::3]
extent = 0, len(cols), minrm, maxrm

ax.imshow(np.array(df_all[cols]), cmap='viridis_r', origin='upper', aspect='auto', extent=extent)
ax.set_xticks(ind_col, ind_col_names, rotation='45')
ax.set_xlabel('Day of year')
ax.set_ylabel('River Mile')
ax2 = ax.twinx()
ax2.set_yticks(ind_row, ind_row_names)

plt.show()



# %%
