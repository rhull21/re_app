# %% first import the functions for downloading data from NWIS
import dataretrieval.nwis as nwis
import pandas as pd 
import sys

import models, tables, filters, forms, plotly_app
from helpers import dictfetchall

# %%
'''
to do : 
    - make sure the list of usgs stations is complete
    - look up max data for each site in database
    - look up prov flag
    - move to use models  
'''

# %%
usgs_dict = {'08358400': {'data' : None, 'usgs_id' : 1},
                '08331160' : {'data' : None, 'usgs_id' : 2},
                '08331510' : {'data' : None, 'usgs_id' : 3},
                '08332010' : {'data' : None, 'usgs_id' : 4},
                '08354900' : {'data' : None, 'usgs_id' : 5},
                '08355050' : {'data' : None, 'usgs_id' : 6},
                '08355490' : {'data' : None, 'usgs_id' : 7}}

# get daily values (dv)
for site, value in usgs_dict.items(): 
    usgs_dict[site]['data'] = nwis.get_record(sites=site, service='dv', start='1999-12-31', end='2023-01-01')[['00060_Mean', '00060_Mean_cd']].rename(columns={'00060_Mean' : 'flow_cfs', '00060_Mean_cd' : 'prov_flag', 'index' : 'date'})
    usgs_dict[site]['data']['usgs_id'] = usgs_dict[site]['usgs_id'] 


# %% append to database 
# DataFrame.to_sql(name, con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None, method=None)
for site, value in usgs_dict.items(): 
    usgs_dict[site]['data'].to_sql(name='usgs_data',con=cnx,if_exists='append',index=False,chunksize=1)
    break

crsr.close()
cnx.close()

# %%
