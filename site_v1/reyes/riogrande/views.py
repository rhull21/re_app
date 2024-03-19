# %%
import json

import pandas as pd 
import numpy as np
import sys
import os
from datetime import datetime, date, timedelta 

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView
from django.db import connection
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

from django_filters.views import FilterView

import django_tables2 as tables2
from django_tables2 import SingleTableMixin, SingleTableView, RequestConfig
from django_tables2.export.views import ExportMixin
from django_tables2.export.export import TableExport

from riogrande import models, tables, filters, forms, plotly_app
from riogrande.helpers import dictfetchall, GeoJsonContext, make_HeatMap, createmetadata 

# Globals for procedure-based views
grp_type="YEAR"
reach_select="ALL"
year_by = [2022]

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
    
def deltadry(request):
    '''
    to do - 
    20221228 : Can we apply a filterset to a dictionary of values
    20221229 : Download data from the filtered queryset
    '''

    if request.method == 'POST' :
        # POST
        form = forms.DrySelectForm(request.POST)
        if form.is_valid():
            # make sticky
            global grp_type, reach_select
            grp_type = form.cleaned_data['group_by']
            reach_select = form.cleaned_data['reach_select']

    else:
        # GET
        form = forms.DrySelectForm(initial=
                                    {'group_by' : grp_type,
                                     "reach_select" : reach_select
                                    }
        )

    with connection.cursor() as cursor:
        cursor.execute("CALL proc_delta_dry(%s, %s)", params=[grp_type, reach_select])
        data = dictfetchall(cursor)

    table = tables.DeltaDryTable(data=data,grp_type=grp_type)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

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
    table_pagination = False
    model = models.FeatureRm
    template_name = "riogrande/filteredfeatures.html"
    filterset_class = filters.FeatureFilter
    export_formats = ("xls", "csv")

    def get_queryset(self):
        return super().get_queryset()

def drysegments(request, mos=(4,11), ds=(1, 1), read=True, write=False, 
                readfig=True, writefig=False,
                ): 
    '''
    if read = False, write must be True; if read = True, write must be False
        both cannot be set to True, otherwise too much memory is consumed by this script

    Note that write=True also triggers writing the excel version of the file via io_heatmap, which can be kind of finnicky 
    '''

    # read in data
    qry_rm = models.RoundedRm.objects.all()
    qry_dry = models.DryLengthAgg.objects.all()
    qry_rm_feat = models.FeatureRm.objects.all()
    qry_reach = models.Reach.objects.all()
    qry_subreach = models.Subreach.objects.all()

    df_rm = pd.DataFrame.from_records(qry_rm.values())
    df_dry = pd.DataFrame.from_records(qry_dry.values())
    df_rm_feat = pd.DataFrame.from_records(qry_rm_feat.values())
    df_reach = pd.DataFrame.from_records(qry_reach.values())
    df_subreach = pd.DataFrame.from_records(qry_subreach.values())
    

    del qry_rm, qry_dry, qry_rm_feat, qry_reach, qry_subreach

    # metadata
    plot_dict = createmetadata(df=df_dry, df_rms=df_rm, mos=mos, ds=ds)

    # transform
    arr_all = make_HeatMap(df=df_dry, plot_dict=plot_dict, read=read, write=write)
    df_rm_feat['rm'] = df_rm_feat['rm'].astype(float)

    # pass data to and return from plotly app
    target_plot = plotly_app.plotly_drysegsimshow(arr_all, plot_dict, df_rm_feat, df_reach, df_subreach, readfig=readfig, writefig=writefig)
     
    return render(request, 
                "riogrande/drysegments.html",
                {
                 'target_plot' : target_plot,
                }
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
        # print(self.model.objects.order_by('year').distinct('year').values_list('year', flat=True))
        return super().get_queryset()

def drydays(request):
    '''
    '''

    if request.method == 'POST' :
        form = forms.DryDaysForm(request.POST)
        if form.is_valid():
            # make sticky
            global grp_type, reach_select
            grp_type = form.cleaned_data['group_by']
            reach_select = form.cleaned_data['reach_select']
    else:
        form = forms.DryDaysForm(initial=
                                    {'group_by' : grp_type,
                                     "reach_select" : reach_select
                                    }
                                )

    with connection.cursor() as cursor:
        cursor.execute("CALL proc_dry_days(%s, %s)", params=[grp_type, reach_select])
        data = dictfetchall(cursor)

    table = tables.DryDaysTable(data=data,grp_type=grp_type)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

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

def dryevents(request, dir='riogrande/static/data', nm='df_events.csv'):
    """river eyes dry events view."""

    df = pd.read_csv(os.path.join(dir,nm),parse_dates=['date'])

    if request.method == 'POST' :
        form = forms.DryEventsForm(request.POST)
        if form.is_valid():
            # make sticky
            global year_by
            year_by = form.cleaned_data['year_by']
            print(year_by)
        else:
            print("invalid form entry")
    else:
        form = forms.DryEventsForm(initial=
                                    {'year_by' : year_by,
                                    }
                                )
        
    year_by = [int(year) for year in year_by]
    df = df[df['year'].isin(year_by)]

    # -- table 1
    data = df.to_dict(orient='records')
    table = tables.DryEventsTable(data)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))

    # -- table 2
    if len(year_by) > 1: 
        # Aggregate variables
        agg = { 
            'event_number' : 'nunique',
            'day_number' : 'count'
        }
        # groupby
        df_summary = df[['year', 'event_number', 'day_number']].groupby(by='year').agg(agg).reset_index() 
    else: 
        agg = {
            'date' : 'min',
            'day_number' : 'max',
            'rm_up' : 'max',
            'rm_down' : 'min',
            'dry_length' : 'max',
        }
        df_summary = df[['event_number', 'rm_up', 'rm_down', 'dry_length', 'date', 'day_number']].groupby(by='event_number').agg(agg).reset_index()
    
    # rename columns
    df_summary.columns = [col if col not in agg else f'{col}_{agg[col]}' 
                for col in df_summary.columns]
    # for table rendering
    data = df_summary.to_dict(orient='records')

    if len(year_by) > 1: 
        table2 = tables.DryEventsGroupManyTable(data)
    else:
        table2 = tables.DryEventsGroupOneTable(data)

    RequestConfig(request, paginate={"per_page": 10}).configure(table2)

    return render(  request, 
                    "riogrande/dryevents.html", 
                    {
                    "form" : form,
                    "table": table,
                    "table2" : table2
                    # "filter" : filterset
                    }
                    ) 
    
class FilteredSummaryUsgs(ExportMixin, SingleTableMixin, FilterView):
    '''
    to do - Modify to have this thing actually be able to filter a selction using the appropriate queryset with the choice filter
    '''
    table_class = tables.SummaryUsgsTable
    model = models.UsgsFeatureData
    template_name = "riogrande/summaryusgs.html"
    filterset_class = filters.SummaryUsgsFilter
    export_formats = ("xls", "csv")

    def get_queryset(self):
        return super().get_queryset()

def usgs_series(request, readfig=True, writefig=False):

    # read in data
    qry = models.UsgsFeatureData.objects.all()
    data = pd.DataFrame.from_records(qry.values())

    data.rename(columns={'dat' : 'date'}, inplace=True)
    # print('#####################')
    # print(data.columns)
    # print('\n, \n, \n, \n')

    data['year'] = [d.year for d in data['date']]
    target_plot = plotly_app.plotly_seriesusgs(data, readfig=readfig, writefig=writefig)

    return render(request, 
                "riogrande/seriesusgs.html",
                {
                 'target_plot' : target_plot,
                }
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


def dashdrylenflow2(request, yrs=(2002,2023), mos=(4,11), read=True, write=False, readfig=True, writefig=False,
                    short_plot=True, target_plot_include=None, 
                    nm='plotly_dry_usgs_dash_2', template_dir = "riogrande/includes/", plotly_dir="riogrande/static/figs/"):
    '''
    This view is a dashboard for selecting characteristics of relationship between dryness and flow data in time series on subplots 
        template_dir : the location within the Django templating framework (reyes/riogrande/templates/...) for raw html version `included` in `target_plot_include`
        plotly_dir : the location within the django application (reyes/...) with pickled version. 
        
        short_plot : boolean decision of whether or not load directly from template_dir
        target_plot_include : by default None, an alternative target plot if that of the name `nm` is not desired 
        
        In other dashboard / figure views, when `readfig` is called, `plotly_dir` is the default figure read; however, this approach yields unsuitable loading times
            relative to directly passing the html from the `include`.  The logic of the code below is as follows: 
        
        if short_plot: # fastest
            load from template_dir
        else:
            if writefig: # slowest
                update the figure pythonically
                save to plotly_dir
                save to template_dir
                load from plotly_dir
            elif writefig: # slow
                load from plotly_dir 

        TO DO: 
            Need to think through the logic of target_plot_include, as I think it makes things unnecessarily convoluted (even more so than usual)

    '''
    if target_plot_include is None:
        target_plot_include = os.path.join(template_dir,nm+".html")

    # for casual rendering
    if short_plot:
        print('short plot')
        target_plot = None

    # for on-demand rendering (takes a long time)
    else: 
        now = datetime.now()
        print('started')
    
        # read in data
        qry_rm = models.RoundedRm.objects.all()
        qry_dry = models.DryLengthAgg.objects.all()
        qry_flow = models.UsgsFeatureData.objects.filter(
                                                            Q(dat__year__gte=str(yrs[0])) &
                                                            Q(dat__year__lte=str(yrs[1]))
                                                ).filter(
                                                            Q(dat__month__gte=str(mos[0])) &
                                                            Q(dat__month__lte=str(mos[1])) 
                                                )
        qry_reach = models.Reach.objects.all()
        qry_subreach = models.Subreach.objects.all()
        qry_rm_feat = models.FeatureRm.objects.all()

        df_rm = pd.DataFrame.from_records(qry_rm.values())
        df_dry = pd.DataFrame.from_records(qry_dry.values())
        df_flow = pd.DataFrame.from_records(qry_flow.values())
        df_reach = pd.DataFrame.from_records(qry_reach.values())
        df_subreach = pd.DataFrame.from_records(qry_subreach.values())
        df_rm_feat = pd.DataFrame.from_records(qry_rm_feat.values())


        del qry_rm, qry_dry, qry_flow

        ### Drynesss Stuff
        # metadata
        plot_dict = createmetadata(df=df_dry, df_rms=df_rm, yrs=yrs, mos=mos)

        # transform
        arr_all = make_HeatMap(df=df_dry, plot_dict=plot_dict, read=read, write=write)


        ### Flow Stuff
        # metadata
        stations = pd.DataFrame(
                                    {
                                        'usgs_station_name' : pd.unique(df_flow['usgs_station_name']),
                                        'usgs_feature_short_name' : pd.unique(df_flow['usgs_feature_short_name']),
                                        'usgs_feature_display_name' : pd.unique(df_flow['usgs_feature_display_name']),
                                        'rm' : pd.unique(df_flow['rm']).astype(float)
                                    }
                                )
        stations = stations.sort_values(by='rm', ascending=False)
        plot_dict['stations_dict'] = stations


        # transform
        df_flow['Years'] = [d.year for d in df_flow['dat']]
        df_flow['Dates'] = [date(1900,d.month,d.day) for d in df_flow['dat']]
        arr_flow = make_HeatMap(df=df_flow,plot_dict=plot_dict, 
                                    read=read, write=write,
                                    nm='flowgrid')    # dimensions: 0=stations, 1=date_full, 2=years            
        
        # bring it together
        plot_data = {
                    'arr_all' : arr_all, # this is the heatmap of dryness data
                    'Dates' : plot_dict['Dates'], # this is the full range of dates, from 1900
                    'strf_dates' : plot_dict['strf_dates'], # string formulated dates, for custom labels
                    'River Miles' : plot_dict['River Miles'],
                    'Years' : plot_dict['Years'],

                    'arr_flow' : arr_flow, # this is the grid of flows 
                    'usgs_station_name' : plot_dict["stations_dict"]['usgs_station_name'],
                    'usgs_feature_display_name' : plot_dict["stations_dict"]['usgs_feature_display_name'],
                    'Station River Miles' : plot_dict["stations_dict"]['rm'],

                    'df_reach' : df_reach ,
                    'df_subreach' : df_subreach,
                    }

        print('done data')

        ### Return Flow 
        # pass data to and return from plotly app
        target_plot = plotly_app.plotly_dry_usgs_dash_2(plot_data, df_rm_feat, plot_dict, readfig, writefig, nm=nm, plotly_dir=plotly_dir, template_dir=template_dir)

        print(f'done figure {datetime.now()-now}')

    return render(request, 
                "riogrande/dashboarddrylenflow.html",
                {
                 'target_plot_include' : target_plot_include, 
                 'target_plot' : target_plot,
                 'short_plot' : short_plot
                }
                )

# class DashboardDrylenFlow2(TemplateView):
#     template_name = "riogrande/dashboarddrylenflow.html"

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

def featuremap(request):
    return render(request, "riogrande/featuremap.html")

def about(request):
    return render(request, "riogrande/about.html")



def metadata(request):


    '''
    This example is meant to show a simplified version of how we might generate metadata reports from our models
    '''
    import xml.etree.ElementTree as ET 
    import json

    qry = models.RoundedRm.objects.all()
    columns = pd.DataFrame.from_records(qry.values()).columns
    
    with open('riogrande/static/metadata/rosetta_columns.json') as f: 
        metajson = json.load(f)

    # resources: 
        # https://docs.python.org/3/library/json.html
        # https://docs.python.org/3/library/xml.etree.elementtree.html


    # XML Routine: 

        # load an XML snippet (attribute_snippet.xml) for column/attribute with tags 
        # tree = ET.parse('column_template.xml')
        # root = tree.getroot()   
        
        # for each column/attribute

            # lookup field in JSON
            # try: 
            #   metajson[key] 
            # except: 
            #   move forward

            # modify the targets (Element.set()) to be consistent with rosetta columns
            # try: 
            #   


            # append (Element.append()) new attribute to table

            # cache and save filled column/attribute JSON for late


        # load an XML template (table_template.xml) for a table/entity with tags
        # tree = ET.parse('table_template.xml')
        # root = tree.getroot()

        # for each model/table

            # modify the targets (Element.set()) to be consistent with rosetta table 

            # for each model/table:
                # modify entity : tag=JSON
                # modify attributes : tag=JSON

        # save (tree.write()) 
    
    
    ### Pseudo code: 
        # 1. read in query
        # 2. Extract column headers
        # 3. Read column headers from JSON
        # 4. Push to XML Format
        # 5. Push XML Format to 
    return render(request, "riogrande/metadata.html")


# %%
