# %%
import pickle 
import pandas as pd
import numpy as np 
import os
from openpyxl import Workbook


'''
to do : 
    ~ - automate download of heatmap ~ NOTE now accessed from helpers.py make_heatmap():
    ~ - refactor into three functions ~
        ~ - automate writing of xlsx, 2 ways ~ 
    - move to use models  
'''

def main(arr_all=None, plot_dict=None, dir='riogrande/static/data', nm='heatmap'):

    if arr_all is None or plot_dict is None:
        with open(os.path.join(dir,nm+'.pickle'), 'rb') as f:
            arr_all = pickle.load(f)

        with open(os.path.join(dir,nm+'_meta.pickle'), 'rb') as f:
            plot_dict = pickle.load(f)

    make_excel(arr_all, plot_dict, dir, nm, excel_form='3d')
    make_excel(arr_all, plot_dict, dir, nm, excel_form='2d')


def make_excel(arr_all, plot_dict, dir,nm, excel_form):
    print(excel_form)

    excel_file = os.path.join(dir,nm+'.xlsx')

    try:
        os.remove(excel_file)
    except:
        print('file doesn\'t exist')

    # wb = Workbook() # NOTE: for some reason, these were required in the windows, but not linux
    # ws = wb.active # See NOTE

    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        # writer.book = wb # See NOTE
        # writer.sheets = dict((ws.title, ws) for ws in wb.worksheets) See NOTE

        if excel_form == '3d':  # %% 3d (rm, date, yr) file
            
            for i in range(arr_all.shape[2]):
                df = pd.DataFrame(arr_all[:,:,i],index=plot_dict['River Miles'],columns=plot_dict['strf_dates'])
                df.to_excel(writer, sheet_name=str(plot_dict['Years'][i]))
        
        if excel_form == '2d': # %% 2d (flat) file        

            arr_all2 = np.zeros((arr_all.shape[0],arr_all.shape[1]*arr_all.shape[2]))
            for i in range(arr_all.shape[2]):
                arr_all2[:,i*len(plot_dict['strf_dates']):(i+1)*len(plot_dict['strf_dates'])] = arr_all[:,:,i]
                
            columns2 =   [
                            strf_date+'-'+str(yr) for yr in plot_dict['Years'] for strf_date in plot_dict['strf_dates']  
                        ]
            
            df = pd.DataFrame(arr_all2,index=plot_dict['River Miles'],columns=columns2)
            df.to_excel(writer)
    
    print('excel file created')
            

if __name__ == "__main__":
    main()