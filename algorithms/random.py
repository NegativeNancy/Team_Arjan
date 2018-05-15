from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import random as rd

def random(station_dict, max_trains, max_minutes):
    """ Finds a set of random routes.

    Args:
        max_trains: Maximum amount of trains allowed.
        max_minutes: Maximum amount of minutes the trains can run forself

    Returns:
        solution: A set of routes, which are a list of connections.
        station_dict: Dictionary of made connections.
    """

    route_list = []
    station_dict_key_list = []

    for key in station_dict:
        station_dict_key_list.append(key)

    number_of_trains = 1 + rd.choice(range(int(max_trains / 2), max_trains))
    for i in range(number_of_trains):
        connection_list = []
        route = rt.Route(connection_list)
        current_station = rd.choice(station_dict_key_list)
        time_of_route = 0

        while True:
            next_station = rd.choice(station_dict[current_station].neighbors)

            # Check whether route won't be longer than allowed.
            if next_station[1] + route.time() < max_minutes:
                route.append_route(current_station, next_station[0], next_station[1])/
                current_station = next_station[0]
                
            # Route is too long.
            else:
                break

        # Add route to our list of routes.

        route_list.append(route)

    solution = sn.Solution(route_list, station_dict)
    return solution, station_dict
