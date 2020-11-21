# -*- coding: utf-8 -*-
"""
map layers

@author: XSH70
"""
#import pandas as pd
import random

#df=pd.read_csv("D:\\Brandeis\\Course\\BUS 216\\Web Application - Dash\\GlobalAirportDatabase\\air_route.csv")


def txt_add(lst1,lst2):
    add_lst = []
    for i in range(len(lst1)):
        add_lst.append(lst1[i]+" - "+lst2[i])
    return add_lst

def create_map(df):
    IATA = ['LAS','LAX','BOS','DCA','DEN','IAD','JFK',
            'LGA','MIA','MSP','ORD','SEA','SFO','MDW','DAL']
    data=[]
    vis = [[True,False,False,False,False,False,False,False,
            False,False,False,False,False,False,False,False]]
    for a in IATA:
        temp = [True]
        for i in range(len(IATA)):
            temp.append(a==IATA[i])
        vis.append(temp)
    
    color_lst = []
    for i in range(15):
        temp = random.randint(-255,256)
        color_lst.append(temp)
    marker_layer = {
        'mode':'markers',
        'type':'scattermapbox',
        'lat':df['lat_s'].drop_duplicates().to_list(),
        'lon':df['lon_s'].drop_duplicates().to_list(),
        'marker':{'size':8,'color':color_lst,
                  'allowoverlap':True,'autocolorscale':True},
        'showlegend':False,
        'hoverinfo':'text',
        'text':txt_add(df["source"].drop_duplicates().to_list(),
                       df["airport_s"].drop_duplicates().to_list())
    }   
    data.append(marker_layer)
       
    key = 'pk.eyJ1IjoieHNoNzA1IiwiYSI6ImNraDU5azB2ZjAwNXQydW8zcnZ0ZWMwdmgifQ.iYefltL-qx159AoEfhrtAw'
    
    layout = dict(
            title = 'Flight Paths Map',
            height=400,margin={"r":0,"t":50,"l":0,"b":0},
            mapbox = dict(
                accesstoken = key,
                bearing = 0,
                center=dict(lon=-98,lat=38),
                pitch = 0,
                zoom = 3,
                style = 'carto-positron'
                )
            ) 

    figure = dict(data=data,layout=layout)
    
    return figure

def line_map(s_air,d_air,df):
    
    data=[]
    color_lst = ['#bd1e24','#e97600','#f6c700','#FFA07A','#745d46',
                 '#0067a7','#964f8e','#00A591','#7284b7','#964f8e',
                 '#F7CAC9','#F08080','#20B2AA','#778899','#FF69B4']
    marker_layer = {
        'mode':'markers',
        'type':'scattermapbox',
        'lat':df['lat_s'].drop_duplicates().to_list(),
        'lon':df['lon_s'].drop_duplicates().to_list(),
        'marker':{'size':9,'color':color_lst,
                  'allowoverlap':True,'autocolorscale':True},
        'showlegend':False,
        'hoverinfo':'text',
        'text':txt_add(df["source"].drop_duplicates().to_list(),
                       df["airport_s"].drop_duplicates().to_list())
    }
    data.append(marker_layer)
    
    df_new = df.loc[(df['name_s']==s_air)&(df['name_e']==d_air)].copy()
    lat_s = df_new['lat_s'].drop_duplicates().to_list()
    lat_e = df_new['lat_e'].drop_duplicates().to_list()
    lon_s = df_new['lon_s'].drop_duplicates().to_list()
    lon_e = df_new['lon_e'].drop_duplicates().to_list()
    lat_lst = []
    lon_lst = []
    for i in range(len(lat_s)):
        lat_lst.append(lat_s[i])
        lat_lst.append(lat_e[i])
        lon_lst.append(lon_s[i])
        lon_lst.append(lon_e[i])
    line_dt = {
            'marker':{'color':'#A9754F','width':1},
            'mode':'lines',
            'type':'scattermapbox',
            'showlegend':False,
            'lat':lat_lst,
            'lon':lon_lst,
            }
    data.append(line_dt)
    
    key = 'pk.eyJ1IjoieHNoNzA1IiwiYSI6ImNraDU5azB2ZjAwNXQydW8zcnZ0ZWMwdmgifQ.iYefltL-qx159AoEfhrtAw'
    layout = dict(
            title = 'Flight Paths Map',
            height=400,margin={"r":0,"t":50,"l":0,"b":0},
            mapbox = dict(
                accesstoken = key,
                bearing = 0,
                center=dict(lon=-98,lat=38),
                pitch = 0,
                zoom = 3,
                style = 'carto-positron'
                )
            )

    figure = dict(data=data,layout=layout)
    
    return figure