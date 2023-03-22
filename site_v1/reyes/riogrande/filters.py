import django_filters
import sys 
from django_filters.widgets import RangeWidget

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
    feature = django_filters.CharFilter(lookup_expr='icontains')
    rm = django_filters.RangeFilter(label='River Mile Range')
    
    class Meta:
        model = models.FeatureRm
        fields = ("feature", "rm" , "latitude", "longitude")

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
    year = django_filters.NumberFilter(default=2022)

    class Meta: 
        model = models.DryCompAgg
        fields = ['reach', 'year']

class SummaryUsgsFilter(django_filters.FilterSet):
    usgs_station_name = django_filters.MultipleChoiceFilter(choices=models.UsgsGages.objects.values_list('usgs_station_name','usgs_station_name'),
                                                    )
    date = django_filters.DateFromToRangeFilter(label='Date Range')
    flow_cfs = django_filters.RangeFilter()
    prov_flag = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.UsgsFeatureData
        fields = ('usgs_station_name', 'date', 'flow_cfs', 'prov_flag')

class DryLengthAggUsgsDataFilter(django_filters.FilterSet):
    usgs_id = django_filters.MultipleChoiceFilter(choices=models.UsgsGages.objects.values_list('usgs_id','usgs_station_name'))
                                                    
    date = django_filters.DateFromToRangeFilter(label='Date Range')
    flow_cfs = django_filters.RangeFilter(label='Flow Range')
    rm_up = django_filters.RangeFilter(label='River Miles Range')
    dry_length = django_filters.RangeFilter(label='Dry Length Range')
    prov_flag =  django_filters.CharFilter(lookup_expr='icontains')


    class Meta:
        model = models.DryLengthAggUsgsData
        fields = ('usgs_id', 'rm_up', 'dry_length','date', 'flow_cfs', 'prov_flag')

