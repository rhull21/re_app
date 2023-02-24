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

class FeatureRmTable(tables2.Table):
    class Meta:
        model = models.FeatureRm
        template_name = "django_tables2/semantic.html"
        fields = ("feature", "rm_rounded", "latitude_rounded", "longitude_rounded")

class SummaryUsgsTable(tables2.Table):
    class Meta:
        model = models.UsgsFeatureData
        template_name = "django_tables2/semantic.html"
        fields = ("usgs_station_name", "usgs_feature_short_name", "date", "flow_cfs")


class FeatureTable(tables2.Table):
    class Meta:
        model = models.Feature
        template_name = "django_tables2/semantic.html"
        fields = ("fid", "feature", "rm")

class NameTable(tables2.Table):
    name = tables2.Column()

    # class Meta:
    #     attrs = {"class": "paleblue"}