from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    #/riogrande/
    path('', views.index, name='index'),

    # geospatial
    path('map', views.MapView.as_view(), name='map'),

    # dryness
    path('dry/deltadry', views.deltadry, name='delta_dryness'),
    path('dry/drysegs', views.drysegments, name='dry_segments'),
    path('dry/filtereddrysegs', views.FilteredDrySegs.as_view(), name='filtered_dry_segments'),
    path('dry/filteredfeatures', views.FilteredFeatures.as_view(), name='filtered_features'),
    path('dry/drylen', views.FilteredDryLen.as_view(), name='dry_length_comparison'),
    path('dry/comp', views.DryCompView.as_view(), name='dry_comp'),
    path('dry/days', views.drydays, name='dry_days'),
    path('dry/events', views.dryevents, name='dry_events'),

    # flow / discharge
    path('flow/summary', views.FilteredSummaryUsgs.as_view(), name='summary_usgs'), 
    path('flow/series', views.usgs_series, name='usgs_series'),

    # Dashboards
    path('dashboard/dryflow', views.DryLengthAggUsgsDataView.as_view(), name='dashboard_dry_length_flow_table'),
    path('dashboard/dryevents', views.DashboardDryEventsView.as_view(), name='dashboard_dry_events'),
    path('dashboard/drysegs', views.dashdrylenflow1, name='dash_drylen_aggusgsdata_view1'),
    path('dashboard/dashdryflow', views.dashdrylenflow2, name='dash_drylen_aggusgsdata_view2'),

    # Miscellaneous
    path('feature/', views.FeatureListView.as_view(), name='feature_list'),
    path('heatmap/',views.heatmap, name='heatmap'),
    path('featuremap/',views.featuremap, name='featuremap'),
    path('about/',views.about, name='about'), 
    path('metadata/', views.metadata, name='metadata')
    ]
