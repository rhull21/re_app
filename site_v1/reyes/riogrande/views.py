# %%
from __future__ import print_function
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
from datetime import datetime, timedelta 

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django_filters.views import FilterView
from django.db import connection
from django.core.mail import send_mail

import django_tables2 as tables2
from django_tables2 import SingleTableMixin, SingleTableView, RequestConfig
from django_tables2.export.views import ExportMixin

sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande import models, tables, filters, forms
from riogrande.helpers import dictfetchall


'''
to do: 
09222022 - figure out how to get models to import successfully w/o path.append
'''

def index(request):
    return HttpResponse("Hello, world. You're at the riogrande index.")

def geospatial(request):
    return HttpResponse("You're looking at a map")

def dry(request):
    return HttpResponse("You're looking at the landing page for dryness")

def deltadry(request, grp_type='NULL'):
    '''
    to do - 
    20221228 : Can we apply a filterset to a dictionary of values
    '''

    if request.method == 'POST' :
        form = forms.DeltaDryForm(request.POST)
        if form.is_valid():
            grp_type = form.cleaned_data['group_by']
            print(grp_type)
            # return HttpResponseRedirect('/../../riogrande/dry/deltadry')
    else:
        form = forms.DeltaDryForm()

    with connection.cursor() as cursor:
        cursor.execute("CALL proc_delta_dry(%s)", params=[grp_type])
        data = dictfetchall(cursor)

    table = tables.DeltaDryTable(data=data,grp_type=grp_type)
    RequestConfig(request).configure(table)

    # filterset = filters.DeltaDryFilter(request.GET, data)

    return render(  request, 
                    "riogrande/deltadry.html", 
                    {"form" : form,
                    "table": table}
                     # "filter" : filterset}
                    ) 

    # df_deltadry = pd.DataFrame(data)
    # return HttpResponse(df_deltadry.to_html())

def drysegments(request, yr=2021):
    '''
    to do - 
    20220922 - create subfunctions
    20220922 - make flexible for more complex queries w. mindat, maxdat, minrm, maxrm
    20220922 - html templatels
    20221010 - ingest year
    '''
    # locals
    mindat, maxdat = datetime(yr,6,1), datetime(yr,10,31)
    minrm, maxrm = 53.5, 164

    # read in data
    qry_rm_feat = models.FeatureRm.objects.all()
    qry_dry = models.DryLengthAgg.objects.filter(dat__year= yr)
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

class FilteredDryLen(ExportMixin, SingleTableMixin, FilterView):
    table_class = tables.DryLenTable
    model = models.AllLen
    template_name = "riogrande/drylen.html"
    filterset_class = filters.DryLenFilter
    export_formats = ("csv", "xls")

    def get_queryset(self):
        return super().get_queryset()

def drycomp(request, yr=2021):
    response = "You're looking at •	First Day Drying, Last Day Drying, Maximum One-Day Extent, Date of Maximum One-Day Extent Grouped By {reach, subreach} (SQL only) for year %s."
    return HttpResponse(response % yr)

def drydays(request, yr=2021):
    response = "You're looking at •	Total Number of Intermittent Days, Maximum Length, Mean Length grouped by {month, year} for each Reach for year %s."
    return HttpResponse(response % yr)

def dryevents(request, yr=2021):
    response = '''You're looking at •	For each day of drying it would be helpful to know the total number of days dry within the reach, which dried “event” it is for the year, and the day within the dried “event”. For context, during most years the Rio dries, but reconnects after storm events, then redries, and so on. So we have multiple drying events within a single year. For example, lets say the Rio initially dried on June 1, remained dry for three days (June 1-3), reconnected by June 4, but then redried on June 10. It would be ideal to design queries around: \n
                   \t  o	June 1 was the first day of the first drying event of the year
                    \t o	June 3 was the third day of the first drying event of the year
                    \t o	June 10 was the first day of the second drying event of the year and also the fourth total day of drying for the year
                    \t for year %s.'''
    return HttpResponse(response % yr)

def flow(request, yr=2021):
    response =  "you're looking at the landing page for flow stuff for year %s"
    return HttpResponse(response % yr) 

def usgs(request, yr=2021):
    return HttpResponse("You're looking at average flow at usgs station for year %s." % yr)

def usgs_series(request, yr=2021, station='09110000'):
    return HttpResponse("You're looking at time series for station %s for year %s." % (station, yr))

def dashboards(request):
    return HttpResponse("You're looking at the landing page for dashboards")

def dashdryevents(request):
    response =  "query dryevents (number of days dry within each reach) by flow conditions (flow summary) and dates (months too) when individual drying events initially started."
    return HttpResponse(response)

def dashdrysegments(request):
    response =  "query drysegments (rm-discretized dry and non-dry segments) by flow conditions and dates (months too)"
    return HttpResponse(response)

class FeatureListView(SingleTableView):
    model = models.Feature
    table_class = tables.FeatureTable
    template_name = 'riogrande/feature.html'

def name_table(request):
    data = [
    {"name": "Bradley"},
    {"name": "Stevie"},
    ]
    nt = tables.NameTable(data)
    RequestConfig(request).configure(nt)



    return(render(request, "riogrande/name.html", 
            {"table": nt}))

def your_name(request):
    if request.method == 'POST' :
        form = forms.NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/../../riogrande')

    else:
        form = forms.NameForm()

    return render(request, "riogrande/your-name.html", {'form' : form})

def contact_us(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['info@example.com']
            if cc_myself:
                recipients.append(sender)

            # send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/../../riogrande')
    
    else:
        form = forms.ContactForm()

    return render(request, "riogrande/contact_us.html", {'form' : form})

