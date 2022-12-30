import pandas as pd
from os import name

from plotly.offline import plot
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash

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