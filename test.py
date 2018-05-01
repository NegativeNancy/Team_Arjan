import loading_files as load
from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import random as rd

def test(max_trains, max_minutes):
    station_dict = load.load_stations()
    route_list = []
    station_dict_key_list = []

    for key in station_dict:
        station_dict_key_list.append(key)

    begin_station = rd.choice(station_dict_key_list)

    for i in range(max_trains):
        connection_list = []
        route = rt.Route(connection_list)

    for key, value in station_dict.items():
        
        for n in value.neighbors:
            print(key)
            print(n)
            if key

test(7, 120)
