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
from django.db.models import Q

import pickle

from django_filters.views import FilterView

import django_tables2 as tables2
from django_tables2 import SingleTableMixin, SingleTableView, RequestConfig
from django_tables2.export.views import ExportMixin
from django_tables2.export.export import TableExport

# sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande import models, tables, filters, forms, plotly_app
from riogrande.helpers import dictfetchall, GeoJsonContext, make_HeatMap, createmetadata, _make_FlowGrid


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

def deltadry(request, grp_type='DATE', reach_select='ALL'):
    '''
    to do - 
    20221228 : Can we apply a filterset to a dictionary of values
    20221229 : Download data from the filtered queryset
    '''

    if request.method == 'POST' :
        form = forms.DrySelectForm(request.POST)
        if form.is_valid():
            grp_type = form.cleaned_data['group_by']
            reach_select = form.cleaned_data['reach_select']
    else:
        form = forms.DrySelectForm()

    with connection.cursor() as cursor:
        cursor.execute("CALL proc_delta_dry(%s, %s)", params=[grp_type, reach_select])
        data = dictfetchall(cursor)

    table = tables.DeltaDryTable(data=data,grp_type=grp_type)
    RequestConfig(request, paginate={"per_page": 100}).configure(table)

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

    # metadata
    plot_dict = createmetadata(df=df_dry, df_rms=df_rm_feat)

    # transform
    arr_all = make_HeatMap(df=df_dry, plot_dict=plot_dict, read=True, write=False)

    # pass data to and return from plotly app
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

class DryCompView(ExportMixin, SingleTableMixin, FilterView):
    """river dry comp view."""
    table_class = tables.DryCompTable
    model = models.DryCompAgg
    template_name = "riogrande/drycomp.html"
    filterset_class = filters.DryCompFilter
    export_formats = ("xls", "csv")

    def get_queryset(self):
        return super().get_queryset()


def drydays(request, grp_type='DATE', reach_select='ALL'):
    '''
    '''

    if request.method == 'POST' :
        form = forms.DrySelectForm(request.POST)
        if form.is_valid():
            grp_type = form.cleaned_data['group_by']
            reach_select = form.cleaned_data['reach_select']
    else:
        form = forms.DrySelectForm()

    with connection.cursor() as cursor:
        cursor.execute("CALL proc_dry_days(%s, %s)", params=[grp_type, reach_select])
        data = dictfetchall(cursor)

    table = tables.DryDaysTable(data=data,grp_type=grp_type)
    RequestConfig(request, paginate={"per_page": 100}).configure(table)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))

    return render(  request, 
                    "riogrande/drydays.html", 
                    {"form" : form,
                    "table": table}
                     # "filter" : filterset}
                    ) 

class DryEventsView(TemplateView):
    """river eyes dry events view."""
    
    template_name = "riogrande/dryevents.html"

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


    data['year'] = [d.year for d in data['date']]
    target_plot = plotly_app.plotly_seriesusgs(data)

    return render(request, 
                "riogrande/seriesusgs.html",
                {
                    'target_plot' : target_plot,
                } #table}
                )

class DryLengthAggUsgsDataView(ExportMixin, SingleTableMixin, FilterView):
    table_class = tables.DryLengthAggUsgsDataTable
    model = models.DryLengthAggUsgsData
    template_name = "riogrande/DryLengthAggUsgsData.html"
    filterset_class = filters.DryLengthAggUsgsDataFilter
    export_formats = ("xls", "csv")

    def get_queryset(self):
        return super().get_queryset()
            

def dashdrylenflow1(request):
    '''
    This view is a dashboard for selecting characteristics of relationship between dryness and usgs data on scatterplot
    '''
    # read in data
    qry = models.DryLengthAggUsgsData.objects.all()
    data = pd.DataFrame.from_records(qry.values())

    data['year'] = [d.year for d in data['date']]
    target_plot = plotly_app.plotly_dry_usgs_dash_1(data)
    


    return render(request, 
                "riogrande/dash_drylen_aggusgsdata_view1.html",
                {'target_plot' : target_plot}
                )


def dashdrylenflow2(request):
    '''
    This view is a dashboard for selecting characteristics of relationship between dryness and flow data in time series on subplots 
    '''
    # data
    yrs, mos = (2002,2022), (6,11) 

    # read in data
    qry_rm_feat = models.FeatureRm.objects.all()
    qry_dry = models.DryLengthAgg.objects.all()
    df_rm_feat = pd.DataFrame.from_records(qry_rm_feat.values())
    df_dry = pd.DataFrame.from_records(qry_dry.values())
    qry_flow = models.UsgsFeatureData.objects.filter(
                                                        Q(date__month__gte=str(mos[0])) &
                                                        Q(date__month__lte=str(mos[1])) 
                                            ).filter(
                                                        Q(date__year__gte=str(yrs[0])) &
                                                        Q(date__year__lte=str(yrs[1]))
                                            )
    df_flow = pd.DataFrame.from_records(qry_flow.values())

    del qry_rm_feat, qry_dry, qry_flow

    ### Drynesss Stuff
    # metadata
    plot_dict = createmetadata(df=df_dry, df_rms=df_rm_feat)
    # transform
    arr_all = make_HeatMap(df=df_dry, plot_dict=plot_dict, read=True, write=False)


    ### Flow Stuff
    # metadata
    stations = pd.DataFrame(
                                {
                                    'usgs_station_name' : pd.unique(df_flow['usgs_station_name']),
                                    'usgs_feature_short_name' : pd.unique(df_flow['usgs_feature_short_name']),
                                    'rm' : pd.unique(df_flow['rm']).astype(float)
                                }
                            )
    stations = stations.sort_values(by='rm', ascending=False)
    plot_dict['stations_dict'] = stations

    # transform
    df_flow['Years'] = [d.year for d in df_flow['date']]
    df_flow['Dates'] = [date(1900,d.month,d.day) for d in df_flow['date']]
    arr_flow = make_HeatMap(df=df_flow,plot_dict=plot_dict, 
                                read=True, write=False,
                                nm='flowgrid')    # dimensions: 0=stations, 1=date_full, 2=years            

    # bring it together
    plot_data = {
                'arr_all' : arr_all, # this is the heatmap of dryness data
                'Dates' : plot_dict['Dates'], # this is the full range of dates, from 1900
                'strf_dates' : plot_dict['strf_dates'], # string formulated dates, for custom labels
                'River Miles' : plot_dict['River Miles'],
                'Years' : plot_dict['Years'],

                'arr_flow' : arr_flow, # this is the grid of flows 
                'usgs_station_name' : plot_dict["stations_dict"]['usgs_station_name'], #stations, order by rm!
                'Station River Miles' : plot_dict["stations_dict"]['rm'],
                }


    ### Return Flow 
    # pass data to and return from plotly app
    target_plot = plotly_app.plotly_dry_usgs_dash_2(plot_data)


    return render(request, 
                "riogrande/dash_drylen_aggusgsdata_view2.html",
                {
                 'target_plot' : target_plot,
                }
                )


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