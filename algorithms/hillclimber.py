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

def hillclimber(station_dict, max_trains, max_minutes, number_of_iterations = 10000):

    route_list = []
    station_dict_key_list = []
    solution = sn.Solution(route_list, station_dict)

    for key in station_dict:
        station_dict_key_list.append(key)

    # make an 'empty' connection_list
    connection_list = []
    connection_list.append({"begin": None, "end": None, "time": 0})


    # make a solution of empty routes
    for i in range(max_trains):
        route = rt.Route(connection_list)
        solution.route_list.append(route)

    score = solution.score()

    for i in range(number_of_iterations):
        score = iteration(station_dict, station_dict_key_list, max_trains, max_minutes, score, solution, i)

    return solution, station_dict

def iteration(station_dict, station_dict_key_list, max_trains, max_minutes, old_score,  solution, i):
    connection_list = []
    route = rt.Route(connection_list)
    route_index = rd.randint(0, max_trains - 1)

    begin_station = rd.choice(station_dict_key_list)

    #  create a new route
    while True:
        route_time = route.time()

        weight = 0.1 * route_time/ max_minutes
        if 0.05 + weight >   rd.random():
            break

        end_station = rd.choice(station_dict[begin_station].neighbors)

        if route_time + end_station[1] < max_minutes:
            route.append_route(begin_station, end_station[0], end_station[1])
            begin_station = end_station[0]
        else:
            break

    old_route = solution.route_list[route_index]
    solution.route_list[route_index] = route
    new_score = solution.score()

    if old_score < new_score:
        print (new_score, "iteratie", i)
        return new_score
    else:
        solution.route_list[route_index] = old_route
        return old_score
