from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    #/riogrande/
    path('', views.index, name='index'),

    # geospatial
    path('map', views.MapView.as_view(), name='map'),

    # dryness
    path('dry', views.DryView.as_view(), name='dry'),
    path('dry/deltadry', views.deltadry, name='delta_dryness'),
    path('dry/drysegs', views.drysegments, name='dry_segments'),
    path('dry/drysegs/filtereddrysegs', views.FilteredDrySegs.as_view(), name='filtered_dry_segments'),
    path('dry/drysegs/filteredfeatures', views.FilteredFeatures.as_view(), name='filtered_features'),
    path('dry/drylen', views.FilteredDryLen.as_view(), name='dry_length_comparison'),
    path('dry/comp', views.drycomp, name='dry_comp'),
    path('dry/days', views.drydays, name='dry_days'),
    path('dry/events', views.dryevents, name='dry_events'),

    # flow / discharge
    path('flow', views.UsgsView.as_view(), name='usgs'),
    path('flow/summary', views.FilteredSummaryUsgs.as_view(), name='summary_usgs'), 
    path('flow/series', views.usgs_series, name='usgs_series'),

    # dashboards
    path('dashboard/', views.dashboards, name='dashboards'),
    path('dashboard/dryevents', views.dashdryevents, name='dashboard dry events with flow'),
    path('dashboard/drysegs', views.dashdrysegments, name='dashboard dry segments with flow'),

    # Miscellaneous
    path('feature/', views.FeatureListView.as_view(), name='feature_list'),
    path('contact_us/',views.contact_us, name='contact_us'), 
    ]
