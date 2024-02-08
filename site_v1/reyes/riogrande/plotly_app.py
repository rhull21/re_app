import pandas as pd
import os 
from datetime import date
import numpy as np
import pickle

from plotly.offline import plot # plotly.offline.plot
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as io

from riogrande.plotly_dash_helpers import addscatter, addimshow, addgagescatters, frame_args


def plotly_drysegsimshow(data, plot_dict, df_rm_feat, df_reach, df_subreach, writefig, readfig, nm='plotly_drysegsimshow', dir="riogrande/static/figs/"):

    if writefig: 
        fig = px.imshow(data, animation_frame=2, 
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

        # add hover line
        for reach in df_reach['reach']:
            if reach != "Angostura": # some weirdness about this hoverline negatively affecting rendering of y limits
                fig.add_hline(y=(df_reach['upstream_rm_id'][df_reach['reach']==reach].iloc[0]), 
                            line = dict(
                                color = "#F2E3D5",
                                dash = "dot",
                            ),
                            opacity = 0.5,
                            annotation_text=f"{reach} Reach",
                            annotation_position="bottom left", 
                            annotation_font=dict(
                                        size=20,
                                        color='#F2E3D5',
                                ))    
            fig.add_hline(y=(df_reach['downstream_rm'][df_reach['reach']==reach].iloc[0]), 
                        visible = False,  #only displays text annotation
                        annotation_text=f"{reach} Reach",
                        annotation_position="top left", 
                        annotation_font=dict(
                                    size=20,
                                    color='#F2E3D5',
                            ))    


        # update color (red, blue), color name (dry, wet), features, update tick/label formatting
        fig.update_layout(
                        xaxis=dict(
                            tickformat='%b %e',
                            ticks="outside",
                            tickwidth=1.5,
                            ticklen=15,
                            tickangle=315,
                            tickmode="linear",
                            tick0 = "2002-06-01",
                            dtick = "M1",
                            minor = dict(
                                ticklen=7,
                                tick0 = "2002-06-15",
                                dtick = "M1"
                                ),
                            side='top'
                            ),
                        yaxis = dict(
                            range = [min(plot_dict['River Miles']), max(plot_dict['River Miles'])],
                            title_font = dict(
                                size = 20,
                                color = '#012E40'
                            ),
                            ticks="outside",
                            tickwidth = 2,
                            ticklen = 10,
                            minor = dict(
                                tick0 = 60,
                                dtick = 5,
                                ticklen = 5,
                                tickwidth = 0.75
                                ),
                            ),
                        sliders=[dict(
                            steps=steps,
                            bgcolor = '#012E40',
                            activebgcolor = '#F2E3D5',
                            borderwidth = 0,
                            currentvalue = dict(
                                font = dict(
                                    size = 20,
                                    color = '#012E40'),
                                offset = 15,
                                prefix = 'Selected Year: ',
                                xanchor = 'center'
                                ),
                            x = 0.5,
                            xanchor="center",
                            y = 1.3,
                            yanchor="top"
                                )],
                        margin = dict(
                                l=0, r=0,t=0,b=0
                        ),
                )
        
        fig.update_traces(
                    hovertemplate="%{x} <extra>RM %{y}</extra>",    #displays date in one box, and RM in another
                    hoverlabel = dict(
                        bgcolor = "#012E40",
                        bordercolor = '#F2E3D5',
                    ),
                    hoverlabel_font = dict(
                        color = '#F2E3D5',
                        size = 16,
                    )
        )


        # Add dropdown (reomve existing one first)
        fig["layout"].pop("updatemenus")
        fig.update_layout(
            updatemenus=[
                dict( # reaches
                    buttons=list([ 
                        dict(
                            args=["yaxis.range", [min(plot_dict['River Miles']), max(plot_dict['River Miles'])]], 
                            label="All Middle Rio Grande Reaches",
                            method="relayout"
                        )
                        ] + 
                        [
                        dict(
                            args=["yaxis.range", [df_reach['downstream_rm'].iloc[i], df_reach['upstream_rm_id'].iloc[i]]], # for some reason labeled with `id` here
                            label=df_reach['reach'].iloc[i],
                            method="relayout"
                        )
                        for i in range(len(df_reach))
                    ] 
                    ),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=-0.001,
                    xanchor="left",
                    y=1.3,
                    yanchor="top"
                ),
            dict( # subreaches
                    buttons=list( [
                        dict(
                            args=["yaxis.range", [min(plot_dict['River Miles']), max(plot_dict['River Miles'])]], 
                            label="All Middle Rio Grande Subreaches",
                            method="relayout"
                        )
                        ] + 
                        [
                        dict(
                            args=["yaxis.range", [df_subreach['downstream_rm'].iloc[i], df_subreach['upstream_rm_id'].iloc[i]]], # for some reason labeled with `id` here
                            label=df_subreach['subreach'].iloc[i],
                            method="relayout"
                        )
                        for i in range(len(df_subreach))
                    ]
                    
                    ),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.001,
                    xanchor="right",
                    y=1.3,
                    yanchor="top"
                ),
            ]
        )


        fig.update_coloraxes(showscale=False) # reversescale=True,



        ### traces for features and gages ###

        # add the features as a scatterplot (note the inline ternary conditional operator syntax)
        dict_rm_feat = {'Features' : df_rm_feat[df_rm_feat['usgs_station_name'].isnull()],
                        'Stream Gages' : df_rm_feat[df_rm_feat['usgs_station_name'].notnull()],
                        }

        for key in dict_rm_feat:

            df = dict_rm_feat[key]

            if key == 'Features': 
                color = 'black'
            else: 
                color = 'red'

            fig.add_trace( # A backhanded way of labeling things in groups without Lambda
                    go.Scatter(
                        name=key,
                        x=[plot_dict['Dates'][int(len(plot_dict['Dates'])/2)]],
                        y=[plot_dict['River Miles'][int(len(plot_dict['River Miles'])/2)]],
                        opacity=0.25,
                        visible='legendonly',    # features not visible by default, but can be toggled on
                        hoverinfo="skip",
                        legendgroup=key,
                        line=go.scatter.Line(color=color),
                        showlegend=True,
                )
                )

            for i in df.index:

                fig.add_trace(
                    go.Scatter(
                        name=df['feature'].loc[i],
                        x=plot_dict['Dates'],
                        y=np.ones(len(plot_dict['Dates']))*df['rm'].loc[i],
                        opacity=0.25,
                        visible='legendonly',    # features not visible by default, but can be toggled on
                        hovertemplate=key, 
                        legendgroup=key,
                        line=go.scatter.Line(color=color),
                        showlegend=False,
                )
                )

        fig.update_layout(autosize=True)

        print('start figure conversion')
        plotly_plot_obj = plot({'data': fig }, auto_play=False, output_type='div', include_plotlyjs=False, config={'responsive': True})
        print('end figure converstion')

        with open(os.path.join(dir,nm+'.pickle'), 'wb') as f: 
            pickle.dump(plotly_plot_obj, f)
        print('done figure write')
        
    if readfig:
        print('start figure read')
        with open(os.path.join(dir,nm+'.pickle'), 'rb') as f:
            plotly_plot_obj = pickle.load(f)
        print('end figure read')


    return plotly_plot_obj

def plotly_seriesusgs(data, writefig, readfig, nm='plotly_seriesusgs', dir="riogrande/static/figs/"):

    if writefig: 
        yrs = pd.unique(data['year'])
        labels = pd.unique(data['usgs_station_name'])

        fig = px.line(data, color='usgs_station_name', #animation_frame='year',
                        labels={'year' : 'Years',
                                'date' : '',    #hide X-axis title
                                'flow_cfs' : 'Streamflow, in Cubic Feet per Second (cfs)', 
                                'usgs_feature_short_name' : 'USGS Feature Name',
                                'usgs_station_name' : 'USGS Station Name'
                                },
                        color_discrete_sequence=[px.colors.qualitative.Bold[i] for i in range(len(labels))],
                        hover_name='usgs_feature_short_name',
                        x='date', 
                        y='flow_cfs',
                        render_mode = 'webg1')  # necessary for rangeslider to display >500 rows
                        #title=f'Rio Grande Dry Segments ')# by year : {[yr for yr in yrs]}')

        fig.update_traces(
                    visible="legendonly"
        )
        fig.update_layout(xaxis=dict(
                                tickformat='%m-%d-%y',
                                #visible = False,
                                #showticklabels = True,
                                minor = dict(
                                    showgrid = True
                                ),
                                rangeslider = dict(
                                    visible = True,
                                    thickness = 0.07,
                                    bgcolor = 'White',
                                    bordercolor = "#012E40",
                                    borderwidth = 2,
                                    yaxis = dict(
                                        range = [0,4000]
                                )),
                                rangeselector = dict(
                                    buttons = list([
                                        dict(count=1,
                                            label = "Year To Date",
                                            step = 'year',
                                            stepmode = 'todate'),
                                        dict(step = 'all',
                                            label = 'Full Time Series')
                                ])
                            )),
                            yaxis = dict(
                                #visible = False
                            ),
                            margin = dict(
                            #    b = 50
                            ),    
                            legend = dict(
                                orientation = 'h',
                                x = 0.1,
                                borderwidth = 2,
                                bordercolor = "#012E40",
                                font = dict(
                                    size = 16
                                ),
                                title = dict(
                                    text = None
                                )
                                ))

        fig.update_layout(autosize=True)

        print('start figure conversion')
        plotly_plot_obj = plot({'data': fig }, config={'responsive': True}, auto_play=False, output_type='div', include_plotlyjs=False) 
        print('end figure converstion')

        with open(os.path.join(dir,nm+'.pickle'), 'wb') as f: 
            pickle.dump(plotly_plot_obj, f)
        print('done figure write')
        
    if readfig:
        print('start figure read')
        with open(os.path.join(dir,nm+'.pickle'), 'rb') as f:
            plotly_plot_obj = pickle.load(f)
        print('end figure read')
                        
    return plotly_plot_obj

def plotly_dry_usgs_dash_1(data):

    # make plot
    yrs = pd.unique(data['year'])
    labels = pd.unique(data['usgs_station_name'])

    fig = px.scatter_matrix(data,
                            dimensions=["flow_cfs", "dry_length"], 
                            color='usgs_station_name', symbol='year',
                            labels={'year' : 'Years',
                                    'date' : 'Dates',
                                    'flow_cfs' : 'Streamflow, in cubic feet per second \n (cfs)', 
                                    'usgs_feature_short_name' : 'USGS Feature Name',
                                    'usgs_station_name' : 'USGS Station Name',
                                    'rm_up' : "River Mile",
                                    'dry_length' : 'Dry Length \n (RMs)',
                                    },
                            color_discrete_sequence=[px.colors.qualitative.Bold[i] for i in range(len(labels))],
                            )
    
    fig.update_traces(diagonal_visible=False)


    plotly_plot_obj = plot({'data': fig }, config={'responsive': True}, auto_play=False, output_type='div', include_plotlyjs=False) 

    return plotly_plot_obj

def plotly_dry_usgs_dash_2(plot_data, readfig, writefig, nm='plotly_dry_usgs_dash_2', dir="riogrande/static/figs/"):
    '''
    '''
    
    if writefig: 
        print('start figure write')
        ### data
        # indexed by rows, 
        plot_labels = { 
                    1 : 
                        {
                            'plot' : 'imshow',
                            'x_label' : 'Date',
                            'y_label' : 'Dry River Miles', 
                        },
                    2 : 
                        {
                            'plot' : 'scatter',
                            'x_label' : 'Date',
                            'y_label' : 'Streamflow, \n in cubic feet per second (cfs)', 
                        }
                    }
        colors = [px.colors.qualitative.Bold[i] for i in range(len(plot_data['usgs_feature_display_name']))]
        height = 400
        round = 100
        

        ### plots
        fig = make_subplots(
                            rows=2,
                            row_heights=[height, height],
                            cols = 1,
                            shared_xaxes=True,
                            vertical_spacing = 0.05
                            )

        fig.add_trace(addimshow(plot_data, k=0),                
                        row=1, col=1
                    )

        for i, station in enumerate(plot_data['usgs_feature_display_name'],start=0):
            fig.add_trace( addscatter(plot_data, colors, i, k=0),                
                            row=2, col=1, 
                        )  
            
        for i, station in enumerate(plot_data['usgs_feature_display_name'],start=0):
            fig.add_trace( addgagescatters(plot_data, colors, i),                
                            row=1, col=1
                        )  

        ### frames
        frames=[
                    go.Frame(
                        data=[addimshow(plot_data,k, stylized=False)]+[addscatter(plot_data,colors,i,k, stylized=False) for i in range(len(plot_data['usgs_feature_display_name']))],
                        name=f"{plot_data['Years'][k]}",
                        traces=[i for i in range(len(plot_data['usgs_feature_display_name'])+1)]
                            ) for k in range(plot_data['arr_flow'].shape[2])
                ]
        
        fig.update(frames=frames)
        fr_duration=50
        sliders = [
                    {
                        "pad": {"b": 10, "t": 50},
                        "len": 0.9,
                        "x": 0.1,
                        "y": 0,
                        "steps": [
                            {
                                "args": [[f.name], frame_args(fr_duration)],
                                "label": f"{plot_data['Years'][k]}",
                                "method": "animate",
                            }
                            for k, f in enumerate(fig.frames)
                        ],
                        "bgcolor" : '#012E40',
                        "activebgcolor" : '#F2E3D5',
                        "borderwidth" : 0,

                        "currentvalue" : dict(
                            font = dict(
                                size = 20,
                                color = '#012E40'),
                            offset = 15,
                            prefix = 'Selected Year: ',
                            xanchor = 'center'
                            ),
                        "y" : 1.4,    
                        "x" : 0.5,
                        'xanchor' : 'center'                
                    }
                    ]
        


        ### hoverline
        # add hover line
        for reach in plot_data['df_reach']['reach']:
            if reach != "Angostura": # some weirdness about this hoverline negatively affecting rendering of y limits
                fig.add_hline(y=(plot_data['df_reach']['upstream_rm_id'][plot_data['df_reach']['reach']==reach].iloc[0]), 
                            line = dict(
                                color = "#F2E3D5",
                                dash = "dot",
                            ),
                            opacity = 0.5,
                            annotation_text=f"{reach} Reach",
                            annotation_position="bottom left", 
                            annotation_font=dict(
                                        size=14,
                                        color='#F2E3D5',
                                ),
                            row=1
                            )    
            fig.add_hline(y=(plot_data['df_reach']['downstream_rm'][plot_data['df_reach']['reach']==reach].iloc[0]), 
                        visible = False,  #only displays text annotation
                        annotation_text=f"{reach} Reach",
                        annotation_position="top left", 
                        annotation_font=dict(
                                    size=14,
                                    color='#F2E3D5',
                            ),
                        row=1
                        )    


        ### layout
        fig.update_layout(sliders=sliders, 
                          xaxis1_showticklabels=True,
                          xaxis2_showticklabels=False,
                          height=height*2,
                          margin=dict(l=20, r=20, t=20, b=20),
                          legend=dict(
                            title=dict(
                                text='USGS Stream Gages', 
                                font=dict(
                                    size=14,
                                    color = '#012E40')
                            )
                            )
                        )

        fig.update_xaxes(
                        tickformat='%b %e',
                        ticks="outside",
                        tickwidth=1.5,
                        ticklen=15,
                        tickangle=315,
                        tickmode="linear",
                        tick0 = "2002-06-01",
                        dtick = "M1",
                        minor = dict(
                            ticklen=7,
                            tick0 = "2002-06-15",
                            dtick = "M1"
                            ),
                        side = 'top',
                        )
        fig.update_yaxes(
                        dict(
                            title_font = dict(
                                size = 16,
                                color = '#012E40'
                            ),
                        ticks="outside",
                        tickwidth = 2,
                        ticklen = 10,
                        ),
                )
    
        for row in range(2):
            fig.update_yaxes(title_text=plot_labels[row+1]['y_label'], 
                            row=row+1, col=1, 
                            side='left')

        fig.update_traces(
                            dict(showscale=False, 
                            coloraxis=None, 
                            colorscale=['#012E40','#F2E3D5']), selector={'type':'heatmap'})     

        # fig.write_json(f"riogrande/static/figs/{nm}.json")

        print('start figure conversion')
        plotly_plot_obj = plot({'data': fig }, auto_play=False, output_type='div') 
        print('end figure converstion')

        with open(os.path.join(dir,nm+'.pickle'), 'wb') as f: 
            pickle.dump(plotly_plot_obj, f)
        print('done figure write')
        fig.write_html(os.path.join(dir,nm+".html"))
        
    if readfig:
        print('start figure read')
        with open(os.path.join(dir,nm+'.pickle'), 'rb') as f:
            plotly_plot_obj = pickle.load(f)
        print('end figure read')

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
