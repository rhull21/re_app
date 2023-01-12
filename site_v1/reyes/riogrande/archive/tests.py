# %%
import plotly.express as px
from skimage import io

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
from datetime import datetime, timedelta 

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.db import connection
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse

from django_filters.views import FilterView

sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande import models, tables, filters, forms, plotly_app
from riogrande.helpers import dictfetchall

#%%

# read in data
qry_rm_feat = models.FeatureRm.objects.all()
qry_dry = models.DryLengthAgg.objects.all()
df_rm_feat = pd.DataFrame.from_records(qry_rm_feat.values())
df_dry = pd.DataFrame.from_records(qry_dry.values())

minyr, maxyr = df_dry['dat'].min().year, df_dry['dat'].max().year+1
mindat, maxdat = datetime(1900,6,1), datetime(1900,11,1)

# loop through all dates 
dates = pd.date_range(mindat,maxdat,freq='d').date
yrs = [yr for yr in range(minyr, maxyr)]
rms = list(df_rm_feat['rm_rounded'])

# create figure
arr_all = np.zeros((len(dates), len(rms), len(yrs)))
i,j = 0,0
for yr in yrs:
    for date in dates:
        df_dry_date = df_dry[['rm_down_rd', 'rm_up_rd']][df_dry['dat']==datetime(yr,date.month,date.day)]
        print(datetime(yr,date.month,date.day))
        print(df_dry['dat'])
        print(df_dry_date.empty)
        if df_dry_date.empty == False: 
            for dry_date in df_dry_date:
                print(type(dry_date))
                k_down, k_up = rms.index(dry_date['rm_down_rd']), rms.index(dry_date['rm_up_rd'])
                arr_all[i,j,k_down:k_up] = 1
                del dry_date 
        del df_dry_date
    j = j + 1
i =i + 1
# %%
