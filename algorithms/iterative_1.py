"""
Algortihm that finds the shortest path to the next critical station.
If a critcial station cannot directly be reached, route stops.

Begin on a node with one critical connection.
Do not go back to the previous station

Create a random solution where the starting station is different each time
"""
import loading_files as load
from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import random as rd

def iterative_1(station_dict, max_trains, max_minutes):

    route_list = []
    station_dict_key_list = []
    solution = sn.Solution(route_list, station_dict)

    for key in station_dict:
        station_dict_key_list.append(key)

    # make an 'empty' connection_list
    connection_list = []
    connection_list.append("begin": None, "end": None, "time": 0)

    # make a solution of empty routes
    for i in range(max_minutes):
        route = rt.Route(connection_list)
        solution.solution_list.append(route)
