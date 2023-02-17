# %%
import json

import pandas as pd 
import numpy as np
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
from riogrande.helpers import dictfetchall, GeoJsonContext, make_HeatMap


'''
to do: 
09222022 - figure out how to get models to import successfully w/o path.append
01172023 - Refactor and pull out functions
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
        d = GeoJsonContext()
        qs = models.FeatureRm.objects.all()
        context["markers"]  = d.to_GeoJsonDict(qs)
        print(context["markers"])
        return context  

class DryView(TemplateView):
    """river eyes map view."""
    
    template_name = "riogrande/dry.html"


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
    20230103 - Move the tables into separate views, and call them into this view 
    20230117 - cashe this file locally and set it up for ingestion and occasional update 
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

    arr_all = make_HeatMap(df_dry=df_dry, plot_dict=plot_dict, write=True)

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

class DryCompView(TemplateView):
    """river dry comp view."""
    
    template_name = "riogrande/drycomp.html"


class DryDaysView(TemplateView):
    """river eyes dry day view."""
    
    template_name = "riogrande/drydays.html"

class DryEventsView(TemplateView):
    """river eyes dry events view."""
    
    template_name = "riogrande/dryevents.html"


class UsgsView(TemplateView):
    """river eyes Flow Landing Page"""
    
    template_name = "riogrande/usgs.html"

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
                 'table' : table} #table}
                )

class DashboardView(TemplateView):
    
    template_name = "riogrande/dashboard.html"

class DashboardDrySegmentsView(TemplateView):
    
    template_name = "riogrande/dashboarddrysegments.html"

class DashboardDryEventsView(TemplateView):
    
    template_name = "riogrande/dashboarddryevents.html"

class FeatureListView(SingleTableView):
    model = models.Feature
    table_class = tables.FeatureTable
    template_name = 'riogrande/feature.html'

def contact_us(request):
    '''
    Update and create a bonified contact us page
    '''
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

def heatmap(request):
    return render(request, "riogrande/heatmap.html")

def about(request):
    return render(request, "riogrande/about.html")