# -*- coding: utf-8 -*-
"""
web map - flight path

@author: shuhui
"""

import plotly.graph_objects as go

#airport = pd.read_csv('D:\\Brandeis\\Course\\BUS 216\\Web Application - Dash\\GlobalAirportDatabase\\airports_new.csv')
#route = pd.read_csv("D:\\Brandeis\\Course\\BUS 216\\Web Application - Dash\\GlobalAirportDatabase\\route_new.csv")

def create_map(airport,air_route):
    
    fig = go.Figure()
    fig=fig.add_trace(go.Scattergeo(
        locationmode="USA-states",
        lon=airport['Longitude'],
        lat=airport['Latitude'],
        hoverinfo='text',
        text=airport["airport"],
        mode='markers',
        marker=dict(
            size=3,
            color='salmon',
            line=dict(width=3,color='thistle')
            )
        ))
    for i in range(len(air_route)):
        fig.add_trace(
            go.Scattergeo(
                locationmode="USA-states",
                lon=[air_route['lon_s'][i],air_route['lon_e'][i]],
                lat=[air_route['lat_s'][i],air_route['lat_e'][i]],
                mode='lines',
                line=dict(width=0.5,color='lightpink'),
                opacity=0.3
            )
        )
    
    fig.update_layout(
        title_text = 'Flight Paths Map',
        showlegend=False,
        geo=dict(
            scope="usa",
            showland=True,landcolor='rgb(252, 244, 232)',
            showcountries=True,countrycolor='grey',countrywidth=0.7,
            showlakes=True,lakecolor='lightblue',
            showsubunits=True,subunitcolor='lightgrey',subunitwidth=0.7,
            center=dict(lon=-98,lat=38)
            ),
        height=400,margin={"r":0,"t":50,"l":0,"b":0}
        )
    
    return fig