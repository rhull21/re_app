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
    path('dry/filtereddrysegs', views.FilteredDrySegs.as_view(), name='filtered_dry_segments'),
    path('dry/filteredfeatures', views.FilteredFeatures.as_view(), name='filtered_features'),
    path('dry/drylen', views.FilteredDryLen.as_view(), name='dry_length_comparison'),
    path('dry/comp', views.DryCompView.as_view(), name='dry_comp'),
    path('dry/days', views.DryDaysView.as_view(), name='dry_days'),
    path('dry/events', views.DryEventsView.as_view(), name='dry_events'),

    # flow / discharge
    path('flow', views.UsgsView.as_view(), name='usgs'),
    path('flow/summary', views.FilteredSummaryUsgs.as_view(), name='summary_usgs'), 
    path('flow/series', views.usgs_series, name='usgs_series'),

    # Dashboards
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/dryevents', views.DashboardDryEventsView.as_view(), name='dashboard_dry_events'),
    path('dashboard/drysegs', views.DashboardDrySegmentsView.as_view(), name='dashboard_dry_segments'),

    # Miscellaneous
    path('feature/', views.FeatureListView.as_view(), name='feature_list'),
    path('contact_us/',views.contact_us, name='contact_us'),
    path('heatmap/',views.heatmap, name='heatmap'),
    path('about/',views.about, name='about')
    ]
