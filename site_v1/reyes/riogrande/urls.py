from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:yr>/usgs', views.usgs, name='usgs_data'),
    path('<int:yr>/drylen', views.alldrylen, name='dryness_summary'),
    path('<int:yr>/drysegs', views.drysegments, name='dryness_detail')
]

# urlpatterns += staticfiles_urlpatterns()