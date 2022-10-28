import django_tables2 as tables
import sys

sys.path.append('''c/Users/QuinnHull/OneDrive/Workspace/Work/05_GSA/03_projects/2218_RiverEyes/re_app/site_v1/reyes/riogrande''')
from riogrande.models import * 

class DryLenTable(tables.Table):
    class Meta:
        model = AllLen
        template_name = "django_tables2/semantic.html"