# -*- coding: utf-8 -*-
"""
web dash

@author: Shuhui
"""
# install and import library
# pip install dash
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from geopy.geocoders import Nominatim
import time
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc 
from Layouts import navbar
from get_path import read_network_from_file
from algorithms.shortest_path import Dijkstra
from graph.network import Network
from geopy.distance import great_circle
from Layouts.flight_map import create_map, line_map
import base64

city_pop = pd.read_csv('.\\GlobalAirportDatabase\\MetroAreas.csv')
city_pop['2019 estimate'] = city_pop['2019 estimate'].apply(lambda x:x.replace(',',''))
airport = pd.read_csv('.\\GlobalAirportDatabase\\airports_new.csv')
route = pd.read_csv(".\\GlobalAirportDatabase\\route_new.csv")
city = ["Seattle","San Francisco","Las Vegas","Denver","Minneapolis","Dallas",
        "Chicago","Washington","Boston","New York","Los Angeles","Miami"]

# merge datasets
air_route = pd.merge(route,airport,how='left',
                         left_on=['source'],right_on=['IATA'])
del air_route['Unnamed: 0_y']
del air_route['Unnamed: 0_x']
air_route.rename(columns={'airport':'airport_s','city':'city_s','IATA':'IATA_s',
                          'Latitude':'lat_s','Longitude':'lon_s',
                          'Altitude':'alt_s','timezone':'timezone_s',
                          'tz database':'tz_s'},inplace=True)
air_route = pd.merge(air_route,airport,how='left',
                     left_on=['dest'],right_on=['IATA'])
del air_route['Unnamed: 0']
del air_route['country_y']
air_route.rename(columns={'airport':'airport_e','city':'city_e','IATA':'IATA_e',
                          'Latitude':'lat_e','Longitude':'lon_e',
                          'Altitude':'alt_e','timezone':'timezone_e',
                          'tz database':'tz_e'},inplace=True)
air_route['name_s'] = air_route['IATA_s']+' - '+air_route['airport_s']
air_route['name_e'] = air_route['IATA_e']+' - '+air_route['airport_e']

##################################  dashboard page  #################################
BS = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/flatly/bootstrap.min.css"
app = dash.Dash(__name__, external_stylesheets=[BS])
sercer = app.server
app.layout = html.Div([
    navbar.Navbar(),
    dbc.Row(dbc.Col(html.H2("Kartemap Web"),width={"offset":1})),
    dbc.Row(dbc.Col(html.P("This dashboard will display the shortest \
                           distance and path between two cities you've\
                           selected."),width={"offset":1})),
    dbc.Row(dbc.Col(html.Hr())),
    dbc.Row([dbc.Col([
                html.Div(
                    id='dropdown_headerS',
                    children=[
                        html.H4(children='Start City selection'),
                        html.P(
                            id='dropdown_descriptionS',
                            children="Here you can select start city \
                            in the following dropdown lists."                    
                            )]
                ),
                dcc.Dropdown(
                    id='city_dropdownS',
                    options=[{'label':i,'value':i} for i in city],
                    value='city',
                    clearable=True,
                    placeholder='Select a city',
                    style={'width':'200px'}
                ),
                html.Br(),
                html.Div(id='city_valueS'),
                html.Br(),
            ],width={"offset":1}),
            dbc.Col([
                html.Div(
                id='dropdown_headerE',
                children=[
                    html.H4(children='End City selection'),
                    html.P(
                        id='dropdown_descriptionE',
                        children="Here you can select end city \
                        in the following dropdown lists.")
                        ]),
                dcc.Dropdown(
                    id='city_dropdownE',
                    options=[{'label':i,'value':i} for i in city],
                    value='city',
                    clearable=True,
                    placeholder='Select a city',
                    style={'width':'200px'}
                ),
                html.Br(),
                html.Div(id='city_valueE'),
                html.Br(),
            ],width={"offset":1})]),
    dbc.Row(dbc.Col(html.H4("Path Design"),width={"offset":1})),
    dbc.Row(dbc.Col(html.Br())),
    dbc.Row(dbc.Col(html.Div(id='distance'),width={"offset":1})),
    dbc.Row(dbc.Col(html.Br())),
    dbc.Row(dbc.Col(html.I('Following is the shortest design path with total driving distance.'),width={"offset":1})),
    dbc.Row(dbc.Col(html.Br())),
    dbc.Row(dbc.Col(html.B(id='path',style={'color':'DarkSlateBlue','fontSize':16}),width={"offset":1})),
    dbc.Row(dbc.Col(html.Br())),
    dbc.Row(dbc.Col(html.H4("Flight Design"),width={"offset":1})),
    dbc.Row(dbc.Col(html.Br())),
    dbc.Row([
            dbc.Col([
                    html.I('Here you can choose available airports in each city.',
                           style={'color':'LightSlateGrey'}),
                    html.Br(),
                    html.I("If no path shown on map, there's no airline between"
                           "two cities.",style={'color':'LightSlateGrey'}),
                    html.Br(),
                    html.Div('Start city airport(s):'),
                    dcc.RadioItems(id='airport_s',
                                   labelStyle={'display': 'block'},
                                   style={'width':'220px'}),
                    html.Div('------------------------------------------------------'
                             ,style={'color':'#D1B894'}),
                    html.Div('End city airport(s):'),
                    dcc.RadioItems(id='airport_e',
                                   labelStyle={'display': 'block'},
                                   style={'width':'220px'}),
                    html.Button("Submit", id="submit",n_clicks=0,
                                style={'border-radius':'8px'}),
                    html.Hr(),
                    ],width={"offset":1}),
            dbc.Col(html.Div(dcc.Graph(id='map',figure = create_map(air_route),
                                       style={'width':'800px','height':'400px'}))),
            ]),
    dbc.Row(dbc.Col(html.Br())),
    dbc.Row(dbc.Col(html.H4("City Info"),width={"offset":1})),
    dbc.Row(dbc.Col(html.Br())),
    dbc.Row([dbc.Col(dbc.Card([
                        dbc.CardHeader("Start City"),
                        dbc.CardBody([
                                html.Div(id='city_popS'),
                                html.Br(),
                                html.Div(id='lat_longS',style={'color':'DarkCyan'}),
                                html.Br(),
                                html.Div(id='tz_s'),
                                html.Br(),
                                html.Img(id='s_fig')
                                ]),
                    ],style={"width": "25rem"}),width={"offset":1}),
            dbc.Col(dbc.Card([
                        dbc.CardHeader("End City"),
                        dbc.CardBody([
                                html.Div(id='city_popE'),
                                html.Br(),
                                html.Div(id='lat_longE',style={'color':'DarkCyan'}),
                                html.Br(),
                                html.Div(id='tz_e'),
                                html.Br(),
                                html.Img(id='e_fig')
                                ]),
                    ],style={"width": "25rem"})),
            dbc.Col(dbc.Card([
                        dbc.CardHeader("Tips"),
                        dbc.CardBody(
                                html.Div(id='tip'))
                    ],style={"width": "20rem"}))
            ]),
    dbc.Row(dbc.Col(html.Br())),
    dbc.Row(dbc.Col(html.Br())),
    dbc.Row(dbc.Col(html.Br())),
    dbc.Row(dbc.Col(html.Br())),
    ])
# 
################################  callback  #########################################
# print city dropdown results
@app.callback(
        [Output('city_valueS','children'),
         Output('city_valueE','children')],
        [Input('city_dropdownS','value'),
         Input('city_dropdownE','value')]
        )
def update_output(value_s,value_e):
    return 'You have selected "{}"'.format(value_s),'You have selected "{}"'.format(value_e)
 
# get path
@app.callback(
        Output('path','children'),
        [Input('city_dropdownS','value'),
         Input('city_dropdownE','value')]
        )
def get_path(start_city,end_city):
    
    # read network from file
    file_name = 'data/network_description.csv'
    cities, distances = read_network_from_file(file_name)

    # build the network
    network = Network()
    network.add_nodes(cities)
    for connection in distances.items():
        frm = cities[connection[0]]
        for connection_to in connection[1].items():
            network.add_edge(frm, cities[connection_to[0]], connection_to[1])

    # using Dijkstra's algorithm, compute least cost (distance)
    # from start city to all other cities
    Dijkstra.compute(network, network.get_node(start_city))
    
    
    # show the shortest path(s) from start city to the end city
    target_city = network.get_node(end_city)
    path = [target_city.get_name()]
    Dijkstra.compute_shortest_path(target_city, path)
    str_path = (f'{start_city} -> {end_city} = {path[::-1]} : {target_city.get_weight()} km')
    return str_path

# airports dropdown
@app.callback(
        [Output('airport_s','options'),
         Output('airport_e','options')],
        [Input('city_dropdownS','value'),
         Input('city_dropdownE','value')]
        )
def city_airport(city_s,city_e):
    ap_s = air_route.loc[air_route['city_s']==city_s,'name_s'].drop_duplicates()
    options_s = [{'label': i, 'value': i} for i in ap_s]
    ap_e = air_route.loc[air_route['city_e']==city_e,'name_e'].drop_duplicates()
    options_e = [{'label': i, 'value': i} for i in ap_e]
    return options_s,options_e

# filter map
@app.callback(
        Output('map','figure'),
        [Input('submit','n_clicks')],
        [State('airport_s','value'),
         State('airport_e','value')]
        )
def filter_map(n_clicks,airport_s,airport_e):
    df = air_route.copy()
    fig = line_map(airport_s,airport_e,df)
    return fig

# print city population
@app.callback(
        [Output('city_popS','children'),
         Output('city_popE','children')],
        [Input('city_dropdownS','value'),
         Input('city_dropdownE','value')]
        )
def city_info(value_s,value_e):
    pop_s = int(city_pop[city_pop['Metropolitan_Statistical_Area'].str.contains(value_s)]['2019 estimate'])
    pop_e = int(city_pop[city_pop['Metropolitan_Statistical_Area'].str.contains(value_e)]['2019 estimate'])
    return "{} has {:.0f} population estimated in 2019.".format(value_s,pop_s),"{} has {:.0f} population estimated in 2019.".format(value_e,pop_e)

# print city latitude, longitude 
@app.callback(
        [Output('lat_longS','children'),
         Output('lat_longE','children'),
         Output('distance','children')],
        [Input('city_dropdownS','value'),
         Input('city_dropdownE','value')]
        )
def city_loc(value_s,value_e):
     geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36")
     time.sleep(1)
     location_s = geolocator.geocode(value_s)
     lon_s = location_s.longitude
     lat_s = location_s.latitude
     start = (lat_s,lon_s)
     str_s = "{} Longititude: {} Latitude: {}".format(value_s,lon_s,lat_s)
     time.sleep(1)
     location_e = geolocator.geocode(value_e)
     lon_e = location_e.longitude
     lat_e = location_e.latitude
     end = (lat_e,lon_e)
     str_e = "{} Longititude: {} Latitude: {}".format(value_e,lon_e,lat_e)
     d = great_circle(start, end).miles
     d = round(d/0.62137,2)
     str_dis = "[{} -> {}]  Surface Distance: {}".format(value_s,value_e,d)
     return str_s,str_e,str_dis
 
# timezome info
@app.callback(
        [Output('tz_s','children'),
        Output('tz_e','children')],
        [Input('city_dropdownS','value'),
         Input('city_dropdownE','value')]
        )
def timezone(city_s,city_e):
    tz_s = air_route.loc[air_route['city_s']==city_s,'tz_s'].unique()
    tz_e = air_route.loc[air_route['city_s']==city_e,'tz_s'].unique()
    str_s = "{} timezone: {}".format(city_s,tz_s)
    str_e = "{} timezone: {}".format(city_e,tz_e)
    return str_s,str_e

# city figures
@app.callback(
        [Output('s_fig','src'),
         Output('e_fig','src')],
        [Input('city_dropdownS','value'),
         Input('city_dropdownE','value')]
        )
def show_fig(city_s,city_e):
    image_filename = '.\\Layouts\\'+str(city_s)+'.jpg'
    s_source = base64.b64encode(open(image_filename, 'rb').read())
    
    image_filename = '.\\Layouts\\'+str(city_e)+'.jpg'
    e_source = base64.b64encode(open(image_filename, 'rb').read())
    
#    s_source = '.\\Layouts\\'+str(city_s)+'.jpg'
#    e_source = '.\\Layouts\\'+str(city_e)+'.jpg'
    return 'data:image/png;base64,{}'.format(s_source),'data:image/png;base64,{}'.format(e_source)
    

# travelling tips
@app.callback(
        Output('tip','children'),
        [Input('city_dropdownS','value'),
         Input('city_dropdownE','value')]
        )
def tip(city_s,city_e):
    tz_s = air_route.loc[air_route['city_s']==city_s,'timezone_s'].unique()
    tz_e = air_route.loc[air_route['city_s']==city_e,'timezone_s'].unique()
    if tz_e < tz_s:
        return "{} is {} hour(s) later than {}.".format(city_e,int(tz_s-tz_e),city_s)
    elif tz_e > tz_s:
        return "{} is {} hour(s) earlier than {}.".format(city_e,int(tz_e-tz_s),city_s)
    else:
        return "{} and {} are in the same timezone.".format(city_e,city_s)



if __name__ =='__main__':
    app.run_server(debug=False)