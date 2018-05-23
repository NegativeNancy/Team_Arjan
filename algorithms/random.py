from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import random as rd

def random(solution, random_number_trains = True):
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

    # Create list of keys to choose from.
    for key in solution.station_dict:
        station_dict_key_list.append(key)

    random_solution = sn.Solution(route_list, solution.station_dict, solution.max_trains, solution.max_minutes, solution.station_dict_key_list)


    # fix 7 trains is we want to
    if random_number_trains:
        number_of_trains = 1 + rd.choice(range(int(solution.max_trains / 2), solution.max_trains))
    else:
        number_of_trains = solution.max_trains

    for i in range(number_of_trains):
        # Add route to our list of routes.
        route = create_random_route(solution.station_dict_key_list, random_solution, solution.max_minutes)
        random_solution.route_list.append(route)

    return random_solution


def create_random_route(station_dict_key_list, solution, max_minutes):
    """Create a random route.

    Args:
        station_dict_key_list: list of keys in station_dict.
        max_minutes: the maximum time a train can travel.

    Returns:
        A randomly generated route.
    """
    connection_list = []
    route = rt.Route(connection_list)
    current_station = rd.choice(station_dict_key_list)
    time_of_route = 0

    while True:
        next_station = rd.choice(solution.station_dict[current_station].neighbors)

        # Check whether route won't be longer than allowed.
        if next_station[1] + route.time() < max_minutes:
            route.append_route(current_station, next_station[0], next_station[1])
            current_station = next_station[0]

        # Route is too long.
        else:
            break
    return route
