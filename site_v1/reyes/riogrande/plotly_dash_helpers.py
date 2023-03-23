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
        return go.Scatter(
                        x=plot_data['Dates'],
                        y=plot_data['arr_flow'][i,:,k],
                        customdata=plot_data['strf_dates'],
                        name=plot_data['usgs_station_name'][i],
                        legendgroup=plot_data['usgs_station_name'][i],
                        showlegend=True,
                        hovertemplate="Date: %{customdata} <extra> Flow, cfs %{y}</extra>",    
                        hoverlabel = dict(
                        bgcolor = "#012E40",
                        bordercolor = '#F2E3D5',
                        ),
                        hoverlabel_font = dict(
                            color = '#F2E3D5',
                            size = 16,
                        ),
                        line=go.scatter.Line(color=colors[i]),
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
        return go.Scatter(
                    x=plot_data['Dates'],
                    y=np.ones(len(plot_data['Dates']))*plot_data["Station River Miles"][i],
                    name=plot_data['usgs_station_name'][i],
                    legendgroup=plot_data['usgs_station_name'][i],
                    showlegend=False,
                    hoverinfo='skip',
                    line=go.scatter.Line(color=colors[i]),
                    opacity=0.25,
                ) 
    else: 
        return go.Scatter(
                    x=plot_data['Dates'],
                    y=np.ones(len(plot_data['Dates']))*plot_data["Station River Miles"][i],
                ) 
