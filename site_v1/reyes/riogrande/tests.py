# %%
import plotly.express as px

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
from datetime import datetime, date, timedelta 


import mysql.connector as cnctr

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.db import connection
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse

from django_filters.views import FilterView

from plotly.offline import plot
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objs as go


#  globals
config = {
  'user': 'root',
  'password': '300667',
  'host': '127.0.0.1',
  'raise_on_warnings' : True
  }

db_name = "rivereyes" 

cnx = cnctr.connect(**config)
crsr = cnx.cursor()
# createDB(db_name, crsr)
cnx.database = db_name

def executeSQL(sqlcommand,crsr):
    try:
        crsr.execute(sqlcommand)
    except cnctr.Error as err:
        print(err.msg)
    else:
        print("OK")

# %%
# read in data
qry_dry = f'''SELECT * FROM dry_length_agg'''
qry_rm_feat = f'''	SELECT * FROM feature_rm;'''
df_dry = pd.read_sql_query(qry_dry,con=cnx)
df_rm_feat = pd.read_sql_query(qry_rm_feat,con=cnx)

# %%

# loop through all dates
minyr, maxyr = df_dry['dat'].min().year, df_dry['dat'].max().year+1
mindat, maxdat = date(1900,6,1), date(1900,11,1)
full_date = list(pd.date_range(mindat,maxdat,freq='d'))
strf_date = [date.strftime(d, '%m-%d') for d in full_date]
yrs = [yr for yr in range(minyr, maxyr)]
rms = list(df_rm_feat['rm-rounded'])
plot_dict = {
        'Dates' : full_date,
        'strf_dates' : strf_date,
        'Years' : yrs,
        'River Miles' : rms
        }
del full_date, strf_date, yrs, rms, minyr, maxyr, mindat, maxdat


# create figure
arr_all = np.zeros((len(plot_dict['River Miles']), len(plot_dict['Dates']), len(plot_dict['Years']))) # , dtype=bool)
i,j = 0,0
for yr in plot_dict['Years']:
    for d in plot_dict['Dates']: 
        df_dry_date = df_dry[['rm_down_rd', 'rm_up_rd']][df_dry['dat']==date(yr,d.month,d.day)]
        if df_dry_date.empty == False: 
            for k in range(len(df_dry_date)):
                dry_date = df_dry_date.iloc[k]
                # print(dry_date)
                k_down, k_up = plot_dict['River Miles'].index(dry_date['rm_down_rd']), plot_dict['River Miles'].index(dry_date['rm_up_rd'])
                # print(j, k_down, k_up)
                arr_all[k_down:k_up+1,j,i] = 1
                # print(arr_all[i,j,k_down:k_up+1])
                del dry_date, k_down, k_up 
        del df_dry_date
        j = j + 1
    i =i + 1

# %%
def plotly_drysegsimshow(data, plot_dict, df_rm_feat):

    fig = px.imshow(data, animation_frame=2, 
                    # color=['red', 'blue'],
                    aspect='equal', 
                    labels={'animation_frame' : 'Years',
                            'x' : 'Dates',
                            'y' : 'River Miles'},
                    x=plot_dict['Dates'], 
                    y=plot_dict['River Miles'],
                    title=f'Rio Grande Dry Segments, by Year : {plot_dict[list(plot_dict.keys())[2]]}',
                    color_continuous_scale='RdBu')

    # Create and add slider
    steps = []
    for yr in plot_dict['Years']:
        step = dict(label=yr)
        steps.append(step)

    # update color (red, blue), color name (dry, wet), features
    fig.update_layout(xaxis=dict(tickformat='%m-%d'),
                      sliders=[dict(steps=steps)])

    fig.update_coloraxes(reversescale=True,showscale=False)

    # df_rm_feat['x_0'], df_rm_feat['x_1'] = plot_dict['Dates'][0], plot_dict['Dates'][-1]
    df_rm_feat = df_rm_feat[df_rm_feat['feature'].notnull()]

    # fig.show()

    # fig.add_trace(px.scatter(df_rm_feat, x='x', y='rm-rounded'))# , color='feature'))

    # fig = px.scatter(df_rm_feat, x='x', y='rm-rounded')# , color='feature'))

    # fig.add_trace(
    #     go.Scatter(
    #         x=df_rm_feat['x_1'],#np.array((df_rm_feat['x_0'],df_rm_feat['x_1'])).T,#[2, 4],
    #         y=df_rm_feat['rm-rounded'],#[4, 8],
    #         # mode="lines",
    #         # line=go.scatter.Line(color="black"),
    #         fill=df_rm_feat['feature'],
    #         showlegend=False)
    # )
    [
    fig.add_trace(
        go.Scatter(
            name=df_rm_feat['feature'].loc[i],
            x=[plot_dict['Dates'][0], plot_dict['Dates'][-1]], #df_rm_feat['x_1'],#np.array((df_rm_feat['x_0'],df_rm_feat['x_1'])).T,#[2, 4],
            y=[df_rm_feat['rm-rounded'].loc[i],df_rm_feat['rm-rounded'].loc[i]],#[4, 8],
            # mode="lines",
            line=go.scatter.Line(color="black"),
            opacity=0.25,
            showlegend=False)
        )
   for i in df_rm_feat.index
    ]

    # # #Turn graph object into local plotly graph
    # # plotly_plot_obj = plot({'data': fig }, output_type='div')

    # return plotly_plot_obj

    fig.show()


target_plot = plotly_drysegsimshow(arr_all, plot_dict, df_rm_feat)

# %%
import plotly.express as px
fig = px.imshow([[1,2],[2,1]])
print(fig)
help(fig.update_layout)

# %%
# y = (lambda dates: datetime.strptime(dates, '%d-%mT%H:%M:%S')) 
# %%
li = [date.strftime(d, '%m-%d') for d in dates]
# date.strftime(date(1900,11,1), '%m-%d')
# date(1900,11,1)
# %%
import plotly.express as px
import plotly.graph_objects as go

df = px.data.iris()

fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species",
                 title="Using The add_trace() method With A Plotly Express Figure")

fig.add_trace(
    go.Scatter(
        x=[2, 4],
        y=[4, 8],
        mode="lines",
        line=go.scatter.Line(color="gray"),
        showlegend=False)
)
fig.show()

# %%
data = pd.DataFrame({'dates' : [date(1999,2,3), date(2300,4,5)]})
data['year'] = [d.year for d in data['dates']]
print(data)

# %%
# print(data['dates'].year)
data['dates'].iloc[0].year
# %%
