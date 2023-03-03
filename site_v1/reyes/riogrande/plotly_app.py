import pandas as pd
from os import name
from datetime import date

from plotly.offline import plot # plotly.offline.plot
import plotly.express as px
import plotly.graph_objs as go

from dash import dcc 
from dash import html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash

def plotly_drysegsimshow(data, plot_dict, df_rm_feat):

    fig = px.imshow(data, animation_frame=2, 
                    # aspect='equal', 
                    #width=1500,  
                    height=2000, # best way to set dimensions for website rendering?
                    labels={'animation_frame' : 'Year',
                     #       'x' : 'Dates',
                            'y' : 'River Mile', 
                            'color' : 'Dryness (1=True)'},
                    x=plot_dict['Dates'], 
                    y=plot_dict['River Miles'],
                   # title=f'Rio Grande Dry Segments, by Year ', # : {plot_dict[list(plot_dict.keys())[2]]}',
                    color_continuous_scale=['#012E40','#F2E3D5'],
                    origin='lower') # changes imshow default reversal of Y-axis

    # Create and add slider
    steps = []
    for yr in plot_dict['Years']:
        step = dict(label=yr)
        steps.append(step)

    # update color (red, blue), color name (dry, wet), features
    fig.update_layout(xaxis=dict(tickformat='%m-%d'),
                      sliders=[dict(steps=steps)])
    fig.update_coloraxes(showscale=False) # reversescale=True,

    fig.add_hline(y=116, 
                  annotation_text="San Acacia Reach",
                  annotation_position="bottom left", 
                  annotation_font=dict(
                            size=20,
                            color='#F2E3D5',
                       ))    # San Acacia reach US boundary
    fig.add_hline(y=116, 
                  annotation_text="Isleta Reach",
                  annotation_position="top left", 
                  annotation_font=dict(
                            size=20,
                            color='#F2E3D5',
                       ))    # Isleta reach US boundary 

   
    # add the features as a scatterplot
    df_rm_feat = df_rm_feat[df_rm_feat['feature'].notnull()]

    [
    fig.add_trace(
        go.Scatter(
            name=df_rm_feat['feature'].loc[i],
            x=[plot_dict['Dates'][0], plot_dict['Dates'][-1]],
            y=[df_rm_feat['rm_rounded'].loc[i],df_rm_feat['rm_rounded'].loc[i]],
            hovertemplate="(%{y})",
            # mode="lines",
            line=go.scatter.Line(color="black"),
            opacity=0.25,
            showlegend=True,
            visible='legendonly'    # features not visible by default, but can be toggled on
        )
        )
   for i in df_rm_feat.index
    ]

    fig.update_layout(legend=dict(
        yanchor='top',
        y=-0.5,
        xanchor='left',
        x=0.25
    ))

    #Turn graph object into local plotly graph
    plotly_plot_obj = plot({'data': fig }, auto_play=False, output_type='div') # add command to turn animations off

    return plotly_plot_obj

def plotly_seriesusgs(data):

    yrs = pd.unique(data['year'])
    labels = pd.unique(data['usgs_station_name'])

    fig = px.line(data, color='usgs_station_name', #animation_frame='year',
                    labels={'year' : 'Years',
                            'date' : 'Dates',
                            'flow_cfs' : 'Discharge, in Cubic Feet per Second (cfs)', 
                            'usgs_feature_short_name' : 'USGS Feature Name',
                            'usgs_station_name' : 'USGS Station Name'
                            },
                    color_discrete_sequence=[px.colors.qualitative.Bold[i] for i in range(len(labels))],
                    hover_name='usgs_feature_short_name',
                    x='date', 
                    y='flow_cfs',
                    height=700)
                    #title=f'Rio Grande Dry Segments ')# by year : {[yr for yr in yrs]}')

    fig.update_layout(xaxis=dict(tickformat='%m-%d-%y')) 


    #Turn graph object into local plotly graph
    plotly_plot_obj = plot({'data': fig }, output_type='div')

    return plotly_plot_obj


def plotly_plot(result_table):
    """
    This function plots plotly plot
    """      

    #Create graph object Figure object with data
    fig = go.Figure(data = go.Bar(name = 'Plot1', x = result_table['Column1'], y = result_table['Column2']))

    #Update layout for graph object Figure
    fig.update_layout(title_text = 'Plotly_Plot1',
                      xaxis_title = 'X_Axis',
                      yaxis_title = 'Y_Axis')
    
    #Turn graph object into local plotly graph
    plotly_plot_obj = plot({'data': fig}, output_type='div')

    return plotly_plot_obj

def plotly_plot_interactive(dash_plot_table, city):
    
    # create graph object Figure 
    fig = go.Figure(data = go.Bar(name = 'Plot1' + city, x = dash_plot_table['variable1'], y = dash_plot_table['variable2']))

    #Update layout for graph object Figure
    fig.update_layout(barmode='stack', 
                      title_text = 'Variable: ' + city,
                      xaxis_title = 'Variable1',
                      yaxis_title = 'Variable2')

    #Turn graph object into local plotly graph
    plotly_plot_obj = plot({'data': fig}, output_type='div')

    return plotly_plot_obj

def plotly_imshow(img_rgb):


    fig = px.imshow(img_rgb)
    # df = px.data.gapminder()
    # fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
    #         size="pop", color="continent", hover_name="country",
    #         log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])
    # fig["layout"].pop("updatemenus") # optional, drop animation buttons
    # from skimage import io
    # data = io.imread("https://github.com/scikit-image/skimage-tutorials/raw/main/images/cells.tif")
    # img = data[25:40]
    # fig = px.imshow(img, animation_frame=0, binary_string=True, labels=dict(animation_frame="slice"))


    #Turn graph object into local plotly graph
    plotly_plot_obj = plot({'data': fig }, output_type='div')

    return plotly_plot_obj
