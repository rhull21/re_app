import django_filters
import sys 
from django_filters.widgets import RangeWidget
from datetime import date, datetime

# sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande import models 

labels = { 
        'dat' : 
            {
                'gt' : 'Min, Date <YYYY-MM-DD>', 
                'lt' : 'Max, Date  <YYYY-MM-DD>'
            },
        'rm' : 
            {
                'gt' : 'Min, River Mile', 
                'lt' : 'Max, River Mile',
            },
        'sum_len' : 
            {
                'gt' : 'Min, Percent Dry', 
                'lt' : 'Max, Percent Dry',
            }, 
        'frac_len' : 
            {
                'gt' : 'Min, Dry Length (River Miles)', 
                'lt' : 'Max, Dry Length (River Miles)',
            }, 
        'dry_len' :
            {
                'gt' : 'Min, Dry Length (River Miles)', 
                'lt' : 'Max, Dry Length (River Miles)',
            }, 
        'flow_cfs' :
            {
                'gt' : 'Min, Flow (cfs)', 
                'lt' : 'Max, Flow (cfs)',
            }, 
        'latitude' : 
            {
                'gt' : 'Ymin (Latitude)', 
                'lt' : 'Ymax (Latitude)',
            }, 
        'longitude' : 
            {
                'gt' : 'Xmin (Longitude)', 
                'lt' : 'Xmax (Longitude)',
            }, 

}


class DrySegFilter(django_filters.FilterSet):
    dat__gt = django_filters.DateFilter(field_name='dat', lookup_expr='gt', label=labels['dat']['gt'])
    dat__lt = django_filters.DateFilter(field_name='dat', lookup_expr='gt', label=labels['dat']['lt'])
    dry_length__gt = django_filters.NumberFilter(label='Dry Length, Min', field_name='dry_length', lookup_expr='gt')
    dry_length__lt = django_filters.NumberFilter(label='Dry Length, Max', field_name='dry_length', lookup_expr='lt')
    rm_down__gt = django_filters.NumberFilter(field_name='rm_down', lookup_expr='gt', label=labels['rm']['gt'])
    rm_up__lt = django_filters.NumberFilter(field_name='rm_up', lookup_expr='lt', label=labels['rm']['lt'])

    class Meta:
        model = models.DryLengthAgg
        fields = ("dat__gt", "dat__lt", "dry_length__gt", "dry_length__lt", "rm_down__gt", "rm_up__lt") 

class FeatureFilter(django_filters.FilterSet):
    feature = django_filters.CharFilter(label='Feature Name Contains', lookup_expr='icontains')

    rm_down__gt = django_filters.NumberFilter(field_name='rm_down', lookup_expr='gt', label=labels['rm']['gt'])
    rm_up__lt = django_filters.NumberFilter(field_name='rm_up', lookup_expr='lt', label=labels['rm']['lt'])
    
    latitude__gt = django_filters.NumberFilter(field_name='latitude', lookup_expr='gt', label=labels['latitude']['gt'])
    latitude__lt = django_filters.NumberFilter(field_name='latitude', lookup_expr='gt', label=labels['latitude']['lt'])
    longitude__gt = django_filters.NumberFilter(field_name='longitude', lookup_expr='gt', label=labels['longitude']['gt'])
    longitude__lt = django_filters.NumberFilter(field_name='longitude', lookup_expr='gt', label=labels['longitude']['lt'])


    class Meta:
        model = models.FeatureRm
        fields = ("latitude__gt", "latitude__lt", "longitude__gt", "longitude__lt", "rm_down__gt" , "rm_up__lt", "feature",)

class DryLenFilter(django_filters.FilterSet):
    dat__gt = django_filters.DateFilter(field_name='dat', lookup_expr='gt', label=labels['dat']['gt'])
    dat__lt = django_filters.DateFilter(field_name='dat', lookup_expr='gt', label=labels['dat']['lt'])

    isleta_sum_len__gt = django_filters.NumberFilter(field_name='isleta_sum_len', lookup_expr='gt', label='Isleta: '+labels['sum_len']['gt'])
    isleta_sum_len__lt = django_filters.NumberFilter(field_name='isleta_sum_len', lookup_expr='lt', label='Isleta: '+labels['sum_len']['lt'])
    isleta_frac_len__gt = django_filters.NumberFilter(field_name='isleta_frac_len', lookup_expr='gt', label='Isleta: '+labels['frac_len']['gt'])
    isleta_frac_len__lt = django_filters.NumberFilter(field_name='isleta_frac_len', lookup_expr='lt', label='Isleta: '+labels['frac_len']['lt'])

    acacia_sum_len__gt = django_filters.NumberFilter(field_name='acacia_sum_len', lookup_expr='gt', label='Acacia: '+labels['sum_len']['gt'])
    acacia_sum_len__lt = django_filters.NumberFilter(field_name='acacia_sum_len', lookup_expr='lt', label='Acacia: '+labels['sum_len']['lt'])
    acacia_frac_len__gt = django_filters.NumberFilter(field_name='acacia_frac_len', lookup_expr='gt', label='Acacia: '+labels['frac_len']['gt'])
    acacia_frac_len__lt = django_filters.NumberFilter(field_name='acacia_frac_len', lookup_expr='lt', label='Acacia: '+labels['frac_len']['lt'])

    angostura_sum_len__gt = django_filters.NumberFilter(field_name='angostura_sum_len', lookup_expr='gt', label='Angostura: '+labels['sum_len']['gt'])
    angostura_sum_len__lt = django_filters.NumberFilter(field_name='angostura_sum_len', lookup_expr='lt', label='Angostura: '+labels['sum_len']['lt'])
    angostura_frac_len__gt = django_filters.NumberFilter(field_name='angostura_frac_len', lookup_expr='gt', label='Angostura: '+labels['frac_len']['gt'])
    angostura_frac_len__lt = django_filters.NumberFilter(field_name='angostura_frac_len', lookup_expr='lt', label='Angostura: '+labels['frac_len']['lt'])

    combined_sum_len__gt = django_filters.NumberFilter(field_name='combined_sum_len', lookup_expr='gt', label='Middle Rio Grande: '+labels['sum_len']['gt'])
    combined_sum_len__lt = django_filters.NumberFilter(field_name='combined_sum_len', lookup_expr='lt', label='Middle Rio Grande: '+labels['sum_len']['lt'])
    combined_frac_len__gt = django_filters.NumberFilter(field_name='combined_frac_len', lookup_expr='gt', label='Middle Rio Grande: '+labels['frac_len']['gt'])
    combined_frac_len__lt = django_filters.NumberFilter(field_name='combined_frac_len', lookup_expr='lt', label='Middle Rio Grande: '+labels['frac_len']['lt'])


    class Meta:
        model = models.AllLen
        fields = ['dat__gt', 'dat__lt']

class DeltaDryFilter(django_filters.FilterSet):
    None
    # len = django_filters.NumberFilter()
    # len__gt = django_filters.NumberFilter(field_name='Len', lookup_expr='gt')
    # len__lt = django_filters.NumberFilter(field_name='Len', lookup_expr='lt')
    # # len = django_filters.RangeFilter()
    # # diff = django_filters.RangeFilter()
    # # diff = django_filters.RangeFilter()
    # class Meta:
    #     fields = ['...'] # , 'Diff', 'Domain', 'Date']

class DryCompFilter(django_filters.FilterSet):
    reach = django_filters.MultipleChoiceFilter(choices=models.Reach.objects.values_list('reach','reach'), )
    year = django_filters.NumberFilter()

    class Meta: 
        model = models.DryCompAgg
        fields = ['reach', 'year']

class SummaryUsgsFilter(django_filters.FilterSet):
    usgs_id = django_filters.MultipleChoiceFilter(choices=models.UsgsFeatureGages.objects.values_list('usgs_id', 'usgs_feature_display_name'),
                                                    )
    dat__gt = django_filters.DateFilter(field_name='dat', lookup_expr='gt', label=labels['dat']['gt'])
    dat__lt = django_filters.DateFilter(field_name='dat', lookup_expr='gt', label=labels['dat']['lt'])



    flow_cfs__gt = django_filters.NumberFilter(field_name='flow_cfs', lookup_expr='gt', label=labels['flow_cfs']['gt'])
    flow_cfs__lt = django_filters.NumberFilter(field_name='flow_cfs', lookup_expr='gt', label=labels['flow_cfs']['lt'])

    prov_flag = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.UsgsFeatureData
        fields = ('dat__gt', 'dat__lt', 'flow_cfs__gt', 'flow_cfs__lt', 'prov_flag', 'usgs_id')

class DryLengthAggUsgsDataFilter(django_filters.FilterSet):
    usgs_id = django_filters.MultipleChoiceFilter(choices=models.UsgsFeatureGages.objects.values_list('usgs_id', 'usgs_feature_display_name'),
                                                    )
                                                    
    dat__gt = django_filters.DateFilter(field_name='dat', lookup_expr='gt', label=labels['dat']['gt'])
    dat__lt = django_filters.DateFilter(field_name='dat', lookup_expr='gt', label=labels['dat']['lt'])

    flow_cfs__gt = django_filters.DateFilter(field_name='flow_cfs', lookup_expr='gt', label=labels['flow_cfs']['gt'])
    flow_cfs__lt = django_filters.DateFilter(field_name='flow_cfs', lookup_expr='gt', label=labels['flow_cfs']['lt'])

    rm_down__gt = django_filters.NumberFilter(field_name='rm_down', lookup_expr='gt', label=labels['rm']['gt'])
    rm_up__lt = django_filters.NumberFilter(field_name='rm_up', lookup_expr='lt', label=labels['rm']['lt'])

    dry_length__gt = django_filters.NumberFilter(label='Dry Length, Min', field_name='dry_length', lookup_expr='gt')
    dry_length__lt = django_filters.NumberFilter(label='Dry Length, Max', field_name='dry_length', lookup_expr='lt')

    prov_flag =  django_filters.CharFilter(lookup_expr='icontains')


    class Meta:
        model = models.DryLengthAggUsgsData
        fields = ('dat__gt', 'dat__lt', 'flow_cfs__gt', 'flow_cfs__lt', "dry_length__gt", "dry_length__lt", "rm_down__gt", "rm_up__lt", 'prov_flag', 'usgs_id') 
