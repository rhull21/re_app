import django_tables2 as tables2
import sys

sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande import models 

class DryLenTable(tables2.Table):
    class Meta:
        model = models.AllLen
        template_name = "django_tables2/semantic.html" 

class DeltaDryTable(tables2.Table):

    def __init__(self, data, grp_type,*args, **kwargs):

        self.base_columns['len'] = tables2.Column(verbose_name='Dry Length')
        self.base_columns['diff'] = tables2.Column(verbose_name='Difference Preious Dry Length')
        self.base_columns['domain'] = tables2.Column(verbose_name='Reach Name')

        if (grp_type == "YEAR") or (grp_type == "MONTH"):
            self.base_columns['YEAR(`dat`)'] = tables2.Column(verbose_name='Year')
            if grp_type == "MONTH":
                self.base_columns['MONTH(`dat`)'] = tables2.Column(verbose_name='Month')
        else:
            self.base_columns['dat'] = tables2.DateColumn(verbose_name='Date')

        super(DeltaDryTable, self).__init__(data, *args, **kwargs)
        self.sequence  = ['...'] 
        # self.template_name = "django_tables2/semantic.html" 


    # class Meta:
    #     template_name = "django_tables2/semantic.html" 

    # def get_groupby(self, grp_type):
    #     if (grp_type == "YEAR") or (grp_type == "MONTH"):
    #         self.year = tables2.Column( verbose_name = 'Year') 
    #         if grp_type == "MONTH":
    #             self.month = tables2.Column( verbose_name = 'Month')
    #     else:
    #         self.date = tables2.DateColumn( verbose_name = 'Date')

class FeatureTable(tables2.Table):
    class Meta:
        model = models.Feature
        template_name = "django_tables2/bootstrap.html"
        fields = ("fid", "feature", "rm")

class NameTable(tables2.Table):
    name = tables2.Column()
    class Meta:
        attrs = {"class": "paleblue"}