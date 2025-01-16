# %% first import the functions for downloading data from NWIS
import dataretrieval.nwis as nwis
import mysql.connector as cnctr
import pandas as pd 
from datetime import date
from utils import helpers
from utils.accessetc import read_db_info

'''
to do (01032022): 
    - look up max data for each site in database
    - look up prov flag
    - move to use models  (or maybe not)
    - chronologically update
    - Use the automated SQL rendering approach (helpers.insertMany)
'''
# define database connection, prepare cursor
db_info_dir = '/home/quinn/re_app_dev/etc/db_info.json' # use absolute paths here
config = read_db_info(db_info_dir)
cnx = cnctr.connect(**config)
crsr = cnx.cursor()

# globals (usgs sites)
usgs_dict = {'08358400': {'data' : None, 'usgs_id' : 1},
                '08331160' : {'data' : None, 'usgs_id' : 2},
                '08331510' : {'data' : None, 'usgs_id' : 3},
                '08332010' : {'data' : None, 'usgs_id' : 4},
                '08354900' : {'data' : None, 'usgs_id' : 5},
                '08355050' : {'data' : None, 'usgs_id' : 6},
                '08355490' : {'data' : None, 'usgs_id' : 7},
                '08330000': {'data' : None, 'usgs_id' : 8},
                '08329928' : {'data' : None, 'usgs_id' : 9},
                '08329918' : {'data' : None, 'usgs_id' : 10},
}

start = '2024-01-01'
end = '2024-12-31'

# get daily values (dv)
for site, value in usgs_dict.items(): 
    usgs_dict[site]['data'] = nwis.get_record(sites=site, service='dv', start=start, end=end)[['00060_Mean', '00060_Mean_cd']].rename(columns={'00060_Mean' : 'flow_cfs', '00060_Mean_cd' : 'prov_flag'})
    usgs_dict[site]['data']['date'] = usgs_dict[site]['data'].index
    usgs_dict[site]['data']['usgs_id'] = usgs_dict[site]['usgs_id'] 

# %% append to database (see more refined version below, too)
for site, value in usgs_dict.items():
    try:  
        tbl_name = 'usgs_data'
        cols = usgs_dict[site]['data'].columns
        sql = helpers.createHeader(tbl_name,cols,header_name='INSERT')
        for row in range(len(usgs_dict[site]['data'])):
            record = usgs_dict[site]['data'].iloc[row]
            sql = '\n'.join((sql,f''' ({record[cols[0]]}, '{record[cols[1]]}', '{date.strftime(record[cols[2]],'%Y-%m-%d')}', {record[cols[3]]}),'''))
        sql = (sql[:-1]+';').replace('nan','NULL')
        crsr.execute(sql)
        cnx.commit()
    except cnctr.Error as e:
        print(site)
        print(e)




# %% testing a more streamlined version of doing the above
# from utils import helpers
# import pandas as pd
# tbl_name = 'usgs_data'
# df = pd.DataFrame({'ones' : [1,2], 'text' : ['five','three'], 'date' : ['1999-10-03', '2035-02-05']})
# sql = helpers.insertMany(data=df,tbl_name='usgs_data',header_name='INSERT')
# print(sql)
# # crsr.execute(sql)
# cnx.commit()

# %%
crsr.close()
cnx.close()


# %%
