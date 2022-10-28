import django_filters
import sys 

sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande.models import * 


class DryLenFilter(django_filters.FilterSet):
    isleta_sum_len = django_filters.RangeFilter()
    isleta_frac_len = django_filters.RangeFilter()
    acacia_sum_len = django_filters.RangeFilter()
    acacia_frac_len = django_filters.RangeFilter()
    combined_sum_len = django_filters.RangeFilter()
    combined_frac_len = django_filters.RangeFilter()
    thedate = django_filters.DateFromToRangeFilter()

    class Meta:
        model = AllLen
        fields = ["thedate"]