import django_tables2 as tables2
import sys

# sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande import models 

class DryLenTable(tables2.Table):
    class Meta:
        model = models.AllLen
        template_name = "django_tables2/semantic.html" 

class DeltaDryTable(tables2.Table):

    def __init__(self, data, grp_type,*args, **kwargs):

        self.base_columns['len'] = tables2.Column(verbose_name='Dry Length (miles)')
        self.base_columns['diff'] = tables2.Column(verbose_name='Difference Previous Dry Length (miles)')
        self.base_columns['domain'] = tables2.Column(verbose_name='Reach Name')

        if (grp_type == "YEAR") or (grp_type == "MONTH"):
            self.base_columns['YEAR(`dat`)'] = tables2.Column(verbose_name='Year')
            seq  = ['YEAR(`dat`)', 'len', 'diff', 'domain']
            if grp_type == "MONTH":
                self.base_columns['MONTH(`dat`)'] = tables2.Column(verbose_name='Month')
                seq  = ['MONTH(`dat`)', 'YEAR(`dat`)', 'len', 'diff', 'domain']
        else:
            self.base_columns['dat'] = tables2.DateColumn(verbose_name='Date')
            seq = ['dat', 'len', 'diff', 'domain']


        super(DeltaDryTable, self).__init__(data, *args, **kwargs)
        self.sequence  = seq 
        self.template_name = "django_tables2/semantic.html" 

class DrySegsTable(tables2.Table):
    class Meta:
        model = models.DryLengthAgg
        template_name = "django_tables2/semantic.html"
        fields = ("dat", "dry_length", "rm_up", "rm_down")

class DryCompTable(tables2.Table):
    class Meta:
        model = models.DryCompAgg
        template_name = "django_tables2/semantic.html"

class DryDaysTable(tables2.Table):

    def __init__(self, data, grp_type,*args, **kwargs):

        self.base_columns['dry_days'] = tables2.Column(verbose_name='Total Number of Intermittent Days')
        self.base_columns['max_len'] = tables2.Column(verbose_name='Maximum Length (RMs)')
        self.base_columns['ave_len'] = tables2.Column(verbose_name='Average Length (RMs)')
        self.base_columns['domain'] = tables2.Column(verbose_name='Reach Name')

        if (grp_type == "YEAR") or (grp_type == "MONTH"):
            self.base_columns['YEAR(`dat`)'] = tables2.Column(verbose_name='Year')
            seq  = ['YEAR(`dat`)', 'dry_days', 'max_len', 'ave_len', 'domain']
            if grp_type == "MONTH":
                self.base_columns['MONTH(`dat`)'] = tables2.Column(verbose_name='Month')
                seq  = ['MONTH(`dat`)', 'YEAR(`dat`)', 'dry_days', 'max_len', 'ave_len', 'domain']
        else:
            self.base_columns['dat'] = tables2.DateColumn(verbose_name='Date')
            seq = ['dat', 'dry_days', 'max_len', 'ave_len', 'domain']

        super(DryDaysTable, self).__init__(data, *args, **kwargs)
        self.sequence  = seq 
        self.template_name = "django_tables2/semantic.html" 

class FeatureRmTable(tables2.Table):
    class Meta:
        model = models.FeatureRm
        template_name = "django_tables2/semantic.html"
        fields = ("feature", "rm", "latitude", "longitude")

class SummaryUsgsTable(tables2.Table):
    class Meta:
        model = models.UsgsFeatureData
        template_name = "django_tables2/semantic.html"
        fields = ("usgs_station_name", "usgs_feature_short_name", "date", "flow_cfs", "prov_flag")


class FeatureTable(tables2.Table):
    class Meta:
        model = models.Feature
        template_name = "django_tables2/semantic.html"
        fields = ("fid", "feature", "rm")

class DryLengthAggUsgsDataTable(tables2.Table):
    class Meta:
        model = models.DryLengthAggUsgsData
        template_name = "django_tables2/semantic.html"
        fields = ("date", "rm_up", "dry_length", "usgs_station_name", "usgs_feature_short_name", "flow_cfs", 'prov_flag')

