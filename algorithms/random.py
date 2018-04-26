"""
Create a random sollution.
"""

from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import loading_files as lf
import random as rd


max_trains = 7
max_minutes = 120


def random():
    station_dict = lf.load_stations()
    route_list = []
    station_dict_key_list = []

    for key in station_dict:
        station_dict_key_list.append(key)

    for i in range(max_trains):
        connection_list = []
        route = rt.Route(connection_list)
        current_station = rd.choice(station_dict_key_list)

        while True:
            next_station = rd.choice(station_dict[current_station].neighbors)

            # check wheter route won't be longer then allowed
            if next_station[1] + route.time() < max_minutes:
                for neighbor in station_dict[current_station].neighbors :
                    if neighbor[0] == next_station:
                        neighbor[3] = True
                for neighbor in station_dict[next_station].neighbors:
                    if neighbor[0] == current_station:
                        neighbor[3] = True


                connection = {"begin": current_station, "end":next_station[0], "time":next_station[1]}

                current_station = next_station[0]
                # add new step to route
                connection_list.append(connection)
                route.connection_list = connection_list
            # if so, break out of loop
            else:
                break

        # add route to our list of routes
        route_list.append(route)

    solution = sn.Solution(route_list, station_dict)

    for i in range(max_trains):
        print(solution.solution_list[i].connection_list)

    return solution, station_dict
