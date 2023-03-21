import django_filters
import sys 
from django_filters.widgets import RangeWidget

# sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande import models 

class DrySegFilter(django_filters.FilterSet):
    dat = django_filters.DateFromToRangeFilter(label='Date Range', widget=RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}))
    dry_length = django_filters.RangeFilter(label='Dry Length Range')
    rm_up = django_filters.RangeFilter(label='River Miles Range')
    
    class Meta:
        model = models.DryLengthAgg
        fields = ("dat", "dry_length", "rm_up") 

class FeatureFilter(django_filters.FilterSet):
    feature = django_filters.CharFilter(lookup_expr='icontains')
    rm = django_filters.RangeFilter(label='River Mile Range')
    
    class Meta:
        model = models.FeatureRm
        fields = ("feature", "rm" , "latitude", "longitude")

class DryLenFilter(django_filters.FilterSet):
    isleta_sum_len = django_filters.RangeFilter(label='Example Label')
    isleta_frac_len = django_filters.RangeFilter()
    acacia_sum_len = django_filters.RangeFilter()
    acacia_frac_len = django_filters.RangeFilter()
    combined_sum_len = django_filters.RangeFilter()
    combined_frac_len = django_filters.RangeFilter()
    thedate = django_filters.DateFromToRangeFilter(label='Date Range', widget=RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}))

    class Meta:
        model = models.AllLen
        fields = ["thedate"]

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

