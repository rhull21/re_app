from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    #/riogrande/
    path('', views.index, name='index'),

    # deliverables  
    path('map', views.MapView.as_view(), name='map'),

    path('dry', views.dry, name='dryness'),
    path('dry/deltadry', views.deltadry, name='delta_dryness'),
    path('dry/drysegs', views.drysegments, name='dry_segments'),
    path('dry/drysegs/filtereddrysegs', views.FilteredDrySegs.as_view(), name='filtered_dry_segments'),
    path('dry/drysegs/filteredfeatures', views.FilteredFeatures.as_view(), name='filtered_features'),
    path('dry/drylen', views.FilteredDryLen.as_view(), name='dry length comparison'),
    path('dry/comp', views.drycomp, name='time interval comparison'),
    path('dry/days', views.drydays, name='number of days'),
    path('dry/events', views.dryevents, name='day of dry event'),

    path('flow', views.usgs, name='usgs'),
    path('flow/summary', views.FilteredSummaryUsgs.as_view(), name='summary_usgs'), 
    path('flow/series', views.usgs_series, name='usgs_series'),

    path('dashboard/', views.dashboards, name='dashboards'),
    path('dashboard/dryevents', views.dashdryevents, name='dashboard dry events with flow'),
    path('dashboard/drysegs', views.dashdrysegments, name='dashboard dry segments with flow'),

    path('feature/', views.FeatureListView.as_view(), name='Feature List Test'),
    path('name/', views.name_table, name='test of name table'),
    path('your-name/', views.your_name, name='testing out name loading form'),
    path('contact_us/',views.contact_us, name='testing out contact us page'),
    path('plotly_test_plot/',views.plotly_test_plot, name='testing out plotly plot'),   
    path('plotly_imshow/',views.plotly_imshow, name='testing out plotly image plot'),    
    ]
