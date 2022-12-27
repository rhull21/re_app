from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    #/riogrande/
    path('', views.index, name='index'),

    # deliverables  
    path('geospatial', views.geospatial, name='landing page for geospatial'),

    path('dry', views.dry, name='landing page for dryness'),
    path('dry/deltadry', views.deltadry, name='change in dryness'),
    path('dry/drysegs', views.drysegments, name='dry segments'),
    path('dry/drylen', views.FilteredDryLen.as_view(), name='dry length comparison'),
    path('dry/comp', views.drycomp, name='time interval comparison'),
    path('dry/days', views.drydays, name='number of days'),
    path('dry/events', views.dryevents, name='day of dry event'),

    path('flow', views.flow, name='landing page for flow'),
    path('flow/summary', views.usgs, name='average flow'),
    path('flow/series', views.usgs_series, name='time-series'),

    path('dashboard/', views.dashboards, name='landing page for dashboards'),
    path('dashboard/dryevents', views.dashdryevents, name='dashboard dry events with flow'),
    path('dashboard/drysegs', views.dashdrysegments, name='dashboard dry segments with flow')
    
    ]

# urlpatterns += staticfiles_urlpatterns()