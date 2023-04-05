import django_tables2 as tables2
import sys

# sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande import models 

class DayColumn(tables2.Column): 
    def render(self, value):
        return '{:0.0f}'.format(value)

class PercentColumn(tables2.Column):
    def render(self, value):
        return '{:0.0f}%'.format(value)

class ShortDateColumn(tables2.Column):
    def render(self, value):
        return '{:%b %e}'.format(value)

class DryLenTable(tables2.Table):
    isleta_frac_len = PercentColumn()
    acacia_frac_len = PercentColumn()
    angostura_frac_len = PercentColumn()
    combined_frac_len = PercentColumn()
    class Meta:
        model = models.AllLen
        template_name = "django_tables2/semantic.html" 


class DeltaDryTable(tables2.Table):

    def __init__(self, data, grp_type,*args, **kwargs):

        # print(help(tables2.Column))

        self.base_columns['len'] = tables2.Column(verbose_name='Maximum Dry Length (River Miles)')
        self.base_columns['diff'] = tables2.Column(verbose_name='Difference Previous Dry Length (River Miles)')
        self.base_columns['domain'] = tables2.Column(verbose_name='Reach Name')
        self.base_columns['rm_up'] = tables2.Column(verbose_name='Maximum Upstream Dry Extent')
        self.base_columns['rm_down'] = tables2.Column(verbose_name='Minimum Downstream Dry Extent')

        self.base_columns['YEAR(`dat`)'] = tables2.Column(verbose_name='Year')
        seq  = ['YEAR(`dat`)', 'len', 'diff', 'rm_up', 'rm_down', 'domain', ]
        if (grp_type == "MONTH") or (grp_type == "DATE"):
            self.base_columns['MONTHNAME(`dat`)'] = tables2.Column(verbose_name='Month')
            seq  = ['MONTHNAME(`dat`)'] + seq 
            if (grp_type == "DATE"):
                self.base_columns['DAYOFMONTH(`dat`)'] = DayColumn(verbose_name='Day')
                seq = ['DAYOFMONTH(`dat`)'] + seq 

        super(DeltaDryTable, self).__init__(data, grp_type, *args, **kwargs)
        self.sequence  = seq 
        self.template_name = "django_tables2/semantic.html" 
        # self.orderable = False

class DrySegsTable(tables2.Table):
    class Meta:
        model = models.DryLengthAgg
        template_name = "django_tables2/semantic.html"
        fields = ("dat", "dry_length", "rm_down", "rm_up")

class DryCompTable(tables2.Table):
    first_dry_date = ShortDateColumn()
    last_dry_date = ShortDateColumn()
    date_max_dry_length = ShortDateColumn()
    class Meta:
        model = models.DryCompAgg
        template_name = "django_tables2/semantic.html"

class DryDaysTable(tables2.Table):

    def __init__(self, data, grp_type, *args, **kwargs):

        self.base_columns['dry_days'] = tables2.Column(verbose_name='Total Number of Intermittent Days')
        self.base_columns['max_len'] = tables2.Column(verbose_name='Maximum Dry Length (River Miles)')
        self.base_columns['ave_len'] = tables2.Column(verbose_name='Average Dry Length (River Miles)')
        self.base_columns['domain'] = tables2.Column(verbose_name='Reach Name')
        self.base_columns['rm_up'] = tables2.Column(verbose_name='Maximum Upstream Dry Extent')
        self.base_columns['rm_down'] = tables2.Column(verbose_name='Minimum Downstream Dry Extent')

        self.base_columns['YEAR(`dat`)'] = tables2.Column(verbose_name='Year')
        seq  = ['YEAR(`dat`)', 'dry_days', 'max_len', 'ave_len', 'rm_up', 'rm_down', 'domain', ]
        if (grp_type == "MONTH") or (grp_type == "DATE"):
            self.base_columns['MONTHNAME(`dat`)'] = tables2.Column(verbose_name='Month')
            seq  = ['MONTHNAME(`dat`)'] + seq 
            if (grp_type == "DATE"):
                self.base_columns['DAYOFMONTH(`dat`)'] = DayColumn(verbose_name='Day')
                seq = ['DAYOFMONTH(`dat`)'] + seq 

        super(DryDaysTable, self).__init__(data, grp_type, *args, **kwargs)
        self.sequence  = seq 
        self.template_name = "django_tables2/semantic.html" 
        # self.orderable = False



class FeatureRmTable(tables2.Table):
    class Meta:
        model = models.FeatureRm
        template_name = "django_tables2/semantic.html"
        fields = ("feature", "rm", "latitude", "longitude")

class SummaryUsgsTable(tables2.Table):
    class Meta:
        model = models.UsgsFeatureData
        template_name = "django_tables2/semantic.html"
        fields = ("dat", "usgs_station_name", "usgs_feature_short_name", "flow_cfs", "prov_flag")


class FeatureTable(tables2.Table):
    class Meta:
        model = models.Feature
        template_name = "django_tables2/semantic.html"
        fields = ("fid", "feature", "rm")

class DryLengthAggUsgsDataTable(tables2.Table):
    class Meta:
        model = models.DryLengthAggUsgsData
        template_name = "django_tables2/semantic.html"
        fields = ("dat", "rm_up", "dry_length", "usgs_feature_short_name", "flow_cfs", 'prov_flag')

