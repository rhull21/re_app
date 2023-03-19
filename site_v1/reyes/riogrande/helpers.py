import django
import os
import numpy as np
import pandas as pd
from copy import deepcopy
import pickle
import numpy as np
from datetime import date 


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ] 


class GeoJsonContext():


    def __init__(self):
        '''
        Passes a model object (by default a Django one) for conversion to GeoJSON
        '''
        self.feature_dict = {
                            "type": "Feature",
                            "properties": {
                                "name": None,
                                "pk": None,
                            },
                            "geometry": {
                                "type": "Point",
                                "coordinates": None # [Long, Lat]
                            }
                            }

        self.data = {
                        "type": "FeatureCollection",
                        "crs": {
                            "type": "name",
                            "properties": {
                                "name": "EPSG:4326"
                            }
                        },
                        "features": None #feature_dict
                    }


    def _to_GeoJsonDict(self):

        pk = 1
        feat_list = []
        feat_dict = deepcopy(self.feature_dict)

        for q in self.qs:
            
            if q.feature is not None:
                # print(q.feature)
                
                ''' modify to make more general eventually '''
                feat_dict['properties']['name'] = q.feature # +' \ud83c\uddee\ud83c\uddf9'
                feat_dict['properties']['pk'] = str(pk)
                feat_dict['geometry']['coordinates'] = [q.longitude_rounded, q.latitude_rounded]

                feat_list.append(deepcopy(feat_dict))

                feat_dict = deepcopy(self.feature_dict)
                pk = pk + 1

        self.feat_list = feat_list 
        return self.feat_list 

    def to_GeoJsonDict(self, qs):

        if type(qs) == django.db.models.query.QuerySet: 
            self.qs = qs
        else: 
            print('warning, no queryset passed; no qs set')
            self.qs = None

        self.data['features'] = self._to_GeoJsonDict()

        return self.data
    

def _make_FlowGrid(df_flow, plot_dict):
    '''
    '''
    # create figure
    arr_all = np.zeros((len(plot_dict['stations_dict']['usgs_station_name']), 
                        len(plot_dict['Dates']), 
                        len(plot_dict['Years']))
                        )*np.nan
    i,j,k = 0,0,0 # k = station, j= day, i = year
    for yr in plot_dict['Years']:
        for d in plot_dict['Dates']: 
            for st in plot_dict['stations_dict']['usgs_station_name']:
                f = df_flow['flow_cfs'][
                                    (df_flow['usgs_station_name']==st) &
                                    (df_flow['Dates']==d.date()) & 
                                    (df_flow['Years']==yr)
                                 ]
                if f.empty == False:

                    # if st == plot_dict['stations_dict']['usgs_station_name'][3]:
                    #     print(st, "is not empty")

                    arr_all[k,j,i] = f 
                k= k + 1
                del f
            j = j + 1
            k = 0
        i = i + 1
        j = 0

    return arr_all


def _make_HeatMap(df_dry, plot_dict):

    # create figure
    arr_all = np.zeros((len(plot_dict['River Miles']), len(plot_dict['Dates']), len(plot_dict['Years']))) # , dtype=bool)
    i,j,k = 0,0,0 # k = RM, j= day, i = year
    for yr in plot_dict['Years']:
        # print(yr)
        for d in plot_dict['Dates']: 
            # print(d)
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
                k = 0
            del df_dry_date
            j = j + 1
        i = i + 1
        j = 0

    return arr_all

def make_HeatMap(df, plot_dict, read=True, write=False, dir='riogrande/static/data', nm='heatmap'):
    '''
    name must be flowgrid (flow) or heatmap (dryness)
    '''
    # see if write; write it
    if write:
        try: 
            with open(os.path.join(dir,nm+'.pickle'), 'wb') as f: # os.path.join(dir,nm)
                if nm == 'heatmap':
                    pickle.dump(_make_HeatMap(df_dry=df, plot_dict=plot_dict), f)
                elif nm == 'flowgrid':
                    pickle.dump(_make_FlowGrid(df_flow=df, plot_dict=plot_dict), f)
            with open(os.path.join(dir,nm+'_meta.pickle'), 'wb') as f:
                pickle.dump(plot_dict, f)
        except Exception as e:
            print(f'unable to write, {e}')

    # see if read
    if read:
        # try to read it
        try: 
            print('trying to open')
            with open(os.path.join(dir,nm+'.pickle'), 'rb') as f:
                arr_all = pickle.load(f)

        except:
            print('something happened while reading file; recreating')
            if nm == 'heatmap':
                arr_all = _make_HeatMap(df_dry=df, plot_dict=plot_dict)
            elif nm == 'flowgrid':
                arr_all = _make_FlowGrid(df_flow=df, plot_dict=plot_dict)

    else:
        # just make it again
        if nm == 'heatmap':
            arr_all = _make_HeatMap(df_dry=df, plot_dict=plot_dict)
        elif nm == 'flowgrid':
            arr_all = _make_FlowGrid(df_flow=df, plot_dict=plot_dict)

    # return it
    return arr_all

def createmetadata(df, df_rms, yrs=(None,None), mos=(6,10)):
    # loop through all dates
    if yrs == (None,None): 
        minyr, maxyr = df['dat'].min().year, df['dat'].max().year+1
    else: 
        minyr, maxyr = yrs[0], yrs[1]+1
    
    mindat, maxdat = date(1900,mos[0],1), date(1900,mos[1]+1,1)
    full_date = list(pd.date_range(mindat,maxdat,freq='d'))
    strf_date = [date.strftime(d, '%m-%d') for d in full_date]
    yrs = [yr for yr in range(minyr, maxyr)]
    rms = list(df_rms['rm_rounded'])
    plot_dict = {
            'Dates' : full_date,
            'strf_dates' : strf_date,
            'Years' : yrs,
            'River Miles' : rms
            }
    return plot_dict