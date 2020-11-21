# -*- coding: utf-8 -*-
"""
@author: shuhui
"""
import math
from geopy.geocoders import Nominatim
import time

def shortest_distance(start,end):
    
    # get lat,lon data
    # start city
    geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36")
    
    time.sleep(1)
    location = geolocator.geocode(start)
    start_lon = location.longitude
    start_lat = location.latitude
    
    # end city
    time.sleep(1)
    location = geolocator.geocode(end)
    end_lon = location.longitude
    end_lat = location.latitude
    
    # calculate distance between two cities over the earth's surface
    lat1 = start_lat * math.pi / 180
    lat2 = end_lat * math.pi / 180
    lon1 = start_lon * math.pi / 180
    lon2 = end_lon * math.pi / 180
    
    # haversine distance formula
    ##a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    ##c = 2 ⋅ atan2( √a, √(1−a) )
    ##d = R ⋅ c
    a = math.pow(math.sin(abs(lat1-lat2)/2),2) + math.cos(lat1)*math.cos(lat2)*pow(math.sin(abs(lon1-lon2)/2),2)
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    d = round(6371 * c,2)
    
    return d

#print(shortest_distance("Boston","Chicago"),"km")