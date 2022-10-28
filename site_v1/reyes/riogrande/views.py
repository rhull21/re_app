# %%
from __future__ import print_function
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
from datetime import datetime, timedelta 

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django_filters.views import FilterView

from django_tables2 import MultiTableMixin, RequestConfig, SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin
from django_tables2.paginators import LazyPaginator
import django_tables2 as tables2

sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande.models import * 
from riogrande.tables import *
from riogrande.filters import *

'''
to do: 
09222022 - figure out how to get models to import successfully w/o path.append
'''

def index(request):
    return HttpResponse("Hello, world. You're at the riogrande index.")

def usgs(request, yr=2021):
    return HttpResponse("You're looking at usgs station for year %s." % yr)

def usgs_series(request, yr=2021, station='09110000'):
    return HttpResponse("You're looking at time sereis for station %s for year %s." % (station, yr))

def geospatial(request):
    return HttpResponse("You're looking at a map")

def deltadry(request, yr=2021):
    response = "You're looking at •	Rates of change of dried extent grouped by {days, months, years} grouped by {river mile, reach, subreach} (SQL only) for year %s."
    return HttpResponse(response % yr)

def drysegments(request, yr=2021):
    '''
    to do - 
    20220922 - create subfunctoins
    20220922 - make flexible for more complex queries w. mindat, maxdat, minrm, maxrm
    20220922 - html template
    20221010 - ingest year
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

# class DryLenTable(tables2.Table):
#     class Meta:
#         model = AllLen

class FilteredDryLen(ExportMixin, SingleTableMixin, FilterView):
    table_class = DryLenTable
    model = AllLen
    template_name = "riogrande/drylen.html"

    filterset_class = DryLenFilter

    export_formats = ("csv", "xls")

    def get_queryset(self):
        return super().get_queryset()


def drycomp(request, yr=2021):
    response = "You're looking at •	First Day Drying, Last Day Drying, Maximum One-Day Extent, Date of Maximum One-Day Extent Grouped By {reach, subreach} (SQL only) for year %s."
    return HttpResponse(response % yr)

def drydays(request, yr=2021):
    response = "You're looking at •	Total Number of Intermittent Days, Maximum Length, Mean Length grouped by {month, year} for each Reach for year %s."
    return HttpResponse(response % yr)
