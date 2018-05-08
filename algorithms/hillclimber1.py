"""
Algortihm that finds the shortest path to the next critical station.
If a critcial station cannot directly be reached, route stops.

Begin on a node with one critical connection.
Do not go back to the previous station

Create a random solution where the starting station is different each time
"""
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

    score = solution.score()

    while (score < 8500):
        iteration(station_dict, station_dict_key_list, max_trains, max_minutes, score, solution)

def iteration(station_dict, station_dict_key_list, max_trains, max_minutes, old_score,  solution):

    route = rt.Route(connection_list)
    route_index = rd.randint(0, max_trains - 1)

    begin_station = rd.choice(station_dict_key_list)

    #  create a new route
    while True:
        begin_station = rd.choice(station_dict_key_list)
        route_time = route.time()

        weight = 0.1 * route_time/ max_minutes
        if 0.1 + weight < rd.random():
            break

        end_station = rd.choice(station_dict[begin_station].neighbors)

        if route_time + end_station[2] < max_minutes:
            rt.append_route(begin_station, end_station[0], end_station[2])
            begin_station = end_station[0]
        else:
            break

    old_route = solution.solution_list[route_index]
    so--lution.solution_list[route_index] = route
    new_score = solution.score()

    if old_score < new_score:
        return new_score
    else:
        solution.solution_list[route_index] = old_route
        return old_score
