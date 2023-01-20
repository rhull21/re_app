# %%

import pickle 
import pandas as pd
import numpy as np 
import os
from openpyxl import Workbook

dir = '../site_v1/reyes/riogrande/static/data'
nm = 'heatmap'
nm_meta = 'heatmap_meta.pickle'


with open(os.path.join(dir,nm+'.pickle'), 'rb') as f:
    arr_all = pickle.load(f)

with open(os.path.join(dir,nm+'_meta.pickle'), 'rb') as f:
    plot_dict = pickle.load(f)

# %%
print(arr_all.shape)
print(plot_dict.keys())

# %%
wb = Workbook()
ws = wb.active

with pd.ExcelWriter(os.path.join(dir,nm+'.xlsx'), engine="openpyxl") as writer:
    writer.book = wb
    writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)
    for i in range(arr_all.shape[2]):
        df = pd.DataFrame(arr_all[:,:,i],index=plot_dict['River Miles'],columns=plot_dict['strf_dates'])
        df.to_excel(writer, sheet_name=str(plot_dict['Years'][i]))
        


# %%
arr_all2 = np.zeros((arr_all.shape[0],arr_all.shape[1]*arr_all.shape[2]))
for i in range(arr_all.shape[2]):
    arr_all2[:,i*len(plot_dict['strf_dates']):(i+1)*len(plot_dict['strf_dates'])] = arr_all[:,:,i]
    
columns2 =   [
                strf_date+'-'+str(yr) for yr in plot_dict['Years'] for strf_date in plot_dict['strf_dates']  
            ]

print(arr_all2.shape)
print(columns2)


# %%
wb = Workbook()
ws = wb.active

with pd.ExcelWriter(os.path.join(dir,nm+'_flat.xlsx'), engine="openpyxl") as writer:
    writer.book = wb
    writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)
    df = pd.DataFrame(arr_all2,index=plot_dict['River Miles'],columns=columns2)
    df.to_excel(writer)
        
# %%
