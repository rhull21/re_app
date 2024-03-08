from plotly.offline import plot
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd 
import numpy as np

def frame_args(duration):
    return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        } 

def addscatter(plot_data, colors, i, k=0, stylized=True):
    if stylized: 
        if plot_data['usgs_feature_display_name'].iloc[i] == "USGS 08332010 Bernardo":
            visible=True
        else:
            visible="legendonly"
        return go.Scatter(
                        x=plot_data['Dates'],
                        y=plot_data['arr_flow'][i,:,k],
                        customdata=plot_data['strf_dates'],
                        name=plot_data['usgs_feature_display_name'].iloc[i],
                        legendgroup=plot_data['usgs_feature_display_name'].iloc[i],
                        showlegend=True,
                        hovertemplate=f"Gage: {plot_data['usgs_feature_display_name'].iloc[i]} \n"+"Date: %{customdata} <extra> Streamflow, cfs %{y}</extra>",    
                        hoverlabel = dict(
                        bgcolor = "#012E40",
                        bordercolor = '#F2E3D5',
                        ),
                        hoverlabel_font = dict(
                            color = '#F2E3D5',
                            size = 16,
                        ),
                        line=go.scatter.Line(color=colors[i]),
                        visible=visible,
                    )
    else: 
        return go.Scatter(
                        x=plot_data['Dates'],
                        y=plot_data['arr_flow'][i,:,k],
                    )

def addimshow(plot_data, k=0, stylized=True):
    if stylized: 
        return go.Heatmap(
                    z=plot_data['arr_all'][:,:,k], 
                    x=plot_data['Dates'], 
                    y=plot_data['River Miles'],
                    customdata=np.stack([plot_data['strf_dates'] for i in range(len(plot_data['River Miles']))]),
                    # origin='lower',
                    name="Dry River Miles",
                    showlegend=False,
                    hovertemplate="Date: %{customdata} <extra> River Mile: %{y}</extra>",    
                    hoverlabel = dict(
                    bgcolor = "#012E40",
                    bordercolor = '#F2E3D5',
                    ),
                    hoverlabel_font = dict(
                        color = '#F2E3D5',
                        size = 16,
                    ) 
                    ) 
    else:
        return go.Heatmap(
                    z=plot_data['arr_all'][:,:,k], 
                    x=plot_data['Dates'], 
                    y=plot_data['River Miles'], 
                    ) 

def addgagescatters(plot_data, colors, i, stylized=True):
    if stylized: 
        if plot_data['usgs_feature_display_name'].iloc[i] == "USGS 08332010 Bernardo":
            visible=True
        else:
            visible="legendonly"
        return go.Scatter(
                    x=plot_data['Dates'],
                    y=[plot_data["Station River Miles"].iloc[i]]*len(plot_data['Dates']),
                    name=plot_data['usgs_feature_display_name'].iloc[i],
                    legendgroup=plot_data['usgs_feature_display_name'].iloc[i],
                    showlegend=False,
                    customdata=[plot_data['usgs_feature_display_name'].iloc[i]]*len(plot_data['Dates']),
                    hovertemplate="Gage: %{customdata} <extra> River Mile: %{y}</extra>",
                    hoverinfo='skip',
                    line=go.scatter.Line(color=colors[i]),
                    opacity=0.9,
                    visible=visible
                ) 
    else: 
        return go.Scatter(
                    x=plot_data['Dates'],
                    y=np.ones(len(plot_data['Dates']))*plot_data["Station River Miles"].iloc[i],
                ) 
