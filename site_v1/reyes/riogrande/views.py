# %%
import json

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
from datetime import datetime, date, timedelta 

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.db import connection
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.contrib import messages
from django.urls import reverse

from django_filters.views import FilterView

import django_tables2 as tables2
from django_tables2 import SingleTableMixin, SingleTableView, RequestConfig
from django_tables2.export.views import ExportMixin
from django_tables2.export.export import TableExport

# sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande import models, tables, filters, forms, plotly_app
from riogrande.helpers import dictfetchall


'''
to do: 
09222022 - figure out how to get models to import successfully w/o path.append
'''

def index(request):
    return render(request, 
                "riogrande/index.html",
                )

class MapView(TemplateView):
    """river eyes map view."""
    
    template_name = "riogrande/map.html"

    def get_context_data(self, **kwargs):
        '''return the view context data'''
        context = super().get_context_data(**kwargs)
        
        feat_list = []
        feat_dict = {
                        "type": "Feature",
                        "properties": {
                            "name": None,
                            "pk": None,
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": None # [14.08591836494682, 42.08632592463349]
                        }
                    }
        pk = 1
        for row in models.FeatureRm.objects.all():
            if row.feature is not None:
                feat_dict['name'] = row.feature
                feat_dict['pk'] = pk
                feat_dict['geometry']['coordinates'] = [row.longitude_rounded,row.latitude_rounded]
                feat_list.append(feat_dict)
                pk = pk + 1


        data = {
                        "type": "FeatureCollection",
                        "crs": {
                            "type": "name",
                            "properties": {
                                "name": "EPSG:4326"
                            }
                        },
                        "features": feat_list
                    }

        print(data)

        context["markers"] = data
        return context 

def dry(request):
    return HttpResponse("You're looking at the landing page for dryness")

def deltadry(request, grp_type='NULL'):
    '''
    to do - 
    20221228 : Can we apply a filterset to a dictionary of values
    20221229 : Download data from the filtered queryset
    '''

    if request.method == 'POST' :
        form = forms.DeltaDryForm(request.POST)
        if form.is_valid():
            grp_type = form.cleaned_data['group_by']
    else:
        form = forms.DeltaDryForm()

    with connection.cursor() as cursor:
        cursor.execute("CALL proc_delta_dry(%s)", params=[grp_type])
        data = dictfetchall(cursor)

    table = tables.DeltaDryTable(data=data,grp_type=grp_type)
    RequestConfig(request).configure(table)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))

    # filterset = filters.DeltaDryFilter(request.GET, data)
    return render(  request, 
                    "riogrande/deltadry.html", 
                    {"form" : form,
                    "table": table}
                     # "filter" : filterset}
                    ) 
    # df_deltadry = pd.DataFrame(data)
    # return HttpResponse(df_deltadry.to_html())

class FilteredDrySegs(ExportMixin, SingleTableMixin, FilterView):
    table_class = tables.DrySegsTable
    model = models.DryLengthAgg
    template_name = "riogrande/filtereddrysegs.html"
    filterset_class = filters.DrySegFilter
    export_formats = ("xls", "csv")

    def get_queryset(self):
        return super().get_queryset()

class FilteredFeatures(ExportMixin, SingleTableMixin, FilterView):
    table_class = tables.FeatureRmTable
    model = models.FeatureRm
    template_name = "riogrande/filteredfeatures.html"
    filterset_class = filters.FeatureFilter
    export_formats = ("xls", "csv")

    def get_queryset(self):
        return super().get_queryset()

def drysegments(request):
    '''
    to do - 
    20220922 - create subfunctions
    20230103 - Move the tables into separate views, and call them into this view 
    '''

    # read in data
    qry_rm_feat = models.FeatureRm.objects.all()
    qry_dry = models.DryLengthAgg.objects.all()
    df_rm_feat = pd.DataFrame.from_records(qry_rm_feat.values())
    df_dry = pd.DataFrame.from_records(qry_dry.values())

    #tables
    table1 = tables.DrySegsTable(qry_dry)
    table2 = tables.FeatureRmTable(qry_rm_feat)
    RequestConfig(request,paginate={"per_page" : 10}).configure(table1)
    RequestConfig(request,paginate={"per_page" : 10}).configure(table2)
    
    del qry_rm_feat, qry_dry

    # loop through all dates
    minyr, maxyr = df_dry['dat'].min().year, df_dry['dat'].max().year+1
    mindat, maxdat = date(1900,6,1), date(1900,11,1)
    full_date = list(pd.date_range(mindat,maxdat,freq='d'))
    strf_date = [date.strftime(d, '%m-%d') for d in full_date]
    yrs = [yr for yr in range(minyr, maxyr)]
    rms = list(df_rm_feat['rm_rounded'])
    plot_dict = {
            'Dates' : full_date,
            'strf_dates' : strf_date,
            'Years' : yrs,
            'River Miles' : rms
            }
    del full_date, strf_date, yrs, rms, minyr, maxyr, mindat, maxdat

    # create figure
    arr_all = np.zeros((len(plot_dict['River Miles']), len(plot_dict['Dates']), len(plot_dict['Years']))) # , dtype=bool)
    i,j = 0,0
    for yr in plot_dict['Years']:
        for d in plot_dict['Dates']: 
            df_dry_date = df_dry[['rm_down_rd', 'rm_up_rd']][df_dry['dat']==date(yr,d.month,d.day)]
            if df_dry_date.empty == False: 
                for k in range(len(df_dry_date)):
                    dry_date = df_dry_date.iloc[k]
                    # print(dry_date)
                    k_down, k_up = plot_dict['River Miles'].index(dry_date['rm_down_rd']), plot_dict['River Miles'].index(dry_date['rm_up_rd'])
                    # print(j, k_down, k_up)
                    arr_all[k_down:k_up+1,j,i] = 1
                    # print(arr_all[i,j,k_down:k_up+1])
                    del dry_date, k_down, k_up 
            del df_dry_date
            j = j + 1
        i =i + 1

    target_plot = plotly_app.plotly_drysegsimshow(arr_all, plot_dict, df_rm_feat)
    
    return render(request, 
                "riogrande/drysegments.html",
                {'target_plot' : target_plot, 
                "table1" : table1,
                "table2" : table2,
                "filter" : filter}
                )

class FilteredDryLen(ExportMixin, SingleTableMixin, FilterView):
    table_class = tables.DryLenTable
    model = models.AllLen
    template_name = "riogrande/drylen.html"
    filterset_class = filters.DryLenFilter
    export_formats = ("xls", "csv")

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

def usgs(request, yr=2021):
    return HttpResponse("You're looking at the landing page for flow in year %s." % yr)

class FilteredSummaryUsgs(ExportMixin, SingleTableMixin, FilterView):
    '''
    to do - Modify to have this thing actually be able to filter a selction using the appropriate queryset with the choice filter
    '''
    table_class = tables.SummaryUsgsTable
    model = models.UsgsFeatureData
    template_name = "riogrande/summaryusgs.html" # could merge this back with drylen.html
    filterset_class = filters.SummaryUsgsFilter
    export_formats = ("xls", "csv")

    def get_queryset(self):
        return super().get_queryset()

def usgs_series(request):

    # read in data
    qry = models.UsgsFeatureData.objects.all()
    data = pd.DataFrame.from_records(qry.values())

    table = FilteredSummaryUsgs.table_class(qry)
    RequestConfig(request,paginate={"per_page" : 10}).configure(table)

    data['year'] = [d.year for d in data['date']]
    target_plot = plotly_app.plotly_seriesusgs(data)

    return render(request, 
                "riogrande/seriesusgs.html",
                {'target_plot' : target_plot,
                 'table' : table}
                )
    # return HttpResponse("You're looking at time series for station %s for year %s." % (station, yr))

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

def plotly_test_plot(request):
    data = pd.DataFrame(
        {"Column1": [1,2,3,4],
         "Column2": [8,7,6,5]})

    target_plot = plotly_app.plotly_plot(data)
    
    return render(request, 
                "riogrande/plotly_test_plot.html",
                {'target_plot' : target_plot}
                )

def plotly_imshow(request):
    img_rgb = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255]],
                        [[0, 255, 0], [0, 0, 255], [255, 0, 0]]
                    ], dtype=np.uint8)

    # img_rgb = np.array([[1,2],[4,3],[5,6],[9,8]])

    target_plot = plotly_app.plotly_imshow(img_rgb)
 
    return render(request, 
                "riogrande/plotly_imshow.html",
                {'target_plot' : target_plot}
                )


# %%
