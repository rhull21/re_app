import django_filters
import sys 

sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande import models 


class DryLenFilter(django_filters.FilterSet):
    isleta_sum_len = django_filters.RangeFilter()
    isleta_frac_len = django_filters.RangeFilter()
    acacia_sum_len = django_filters.RangeFilter()
    acacia_frac_len = django_filters.RangeFilter()
    combined_sum_len = django_filters.RangeFilter()
    combined_frac_len = django_filters.RangeFilter()
    thedate = django_filters.DateFromToRangeFilter()

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