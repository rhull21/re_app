# %%
from __future__ import print_function
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
from datetime import datetime, timedelta 
from django.http import HttpResponse 
sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande.models import *  

'''
to do: 
09222022 - figure out how to get models to import successfully w/o path.append
'''

def index(request):
    return HttpResponse("Hello, world. You're at the riogrande index.")

def usgs(request, yr):
    return HttpResponse("You're looking at usgs station for year %s." % yr)

def alldrylen(request, yr):
    '''
    to do
    09222022 - create a dedicated template for this page, improve layout, documentation
    '''
    # response = "You're looking at weekly summarized dry lengths for the rio grande for year %s."
    rs = AllLen.objects.filter(thedate__year= yr)
    df = pd.DataFrame.from_records(rs.values())
    response = df.to_html()
    return HttpResponse(response)

def drysegments(request, yr):
    '''
    to do - 
    20220922 - create subfunctoins
    20220922 - make flexible for more complex queries w. mindat, maxdat, minrm, maxrm
    20220922 - html template
    '''
    # locals
    mindat, maxdat = datetime(yr,6,1), datetime(yr,10,31)
    minrm, maxrm = 53.5, 164

    # read in data
    qry_rm_feat = FeatureRm.objects.all()
    qry_dry = DryLengthAgg.objects.filter(dat__year= yr)
    df_rm_feat = pd.DataFrame.from_records(qry_rm_feat.values())
    df_dry = pd.DataFrame.from_records(qry_dry.values())

    # loop through all dates 
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

    # create figure
    for col in cols: 
        df_temp = df_dry[['rm_down_rd', 'rm_up_rd']][df_dry['dat']==col]
        for i in range(len(df_temp)):
            df_all.loc[(df_all['rm_rounded'] <= df_temp['rm_up_rd'].iloc[i]) & (df_all['rm_rounded'] >= df_temp['rm_down_rd'].iloc[i]),col] = 1

    # create the image
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

    # save fig and set response
    # fullpath = 'c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande/outputs/'
    
    figpath = 'riogrande/static/riogrande/dryseg_v1.png'
    plt.savefig(figpath)
    response = '''{% load static %} <img src="{% static "riogrande/dryseg_v1.png" %}" alt="dryseg" />'''
    
    return HttpResponse(response)
# %%
