from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import loading_files as load
import random as rd

def random(max_trains, max_minutes):
    """ Finds a set of random routes.

    Args:
        max_trains: Maximum amount of trains allowed.
        max_minutes: Maximum amount of minutes the trains can run forself

    Returns:
        solution: A set of routes, which are a list of connections.
        station_dict: Dictionary of made connections.
    """
    station_dict = load.load_stations()
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

            # Check whether route won't be longer than allowed
            if next_station[1] + route.time() < max_minutes:
                for neighbor in station_dict[current_station].neighbors :
                    if neighbor[0] == next_station[0]:
                        neighbor[3] = True
                for neighbor in station_dict[next_station[0]].neighbors:
                    if neighbor[0] == current_station:
                        neighbor[3] = True


                connection = {"begin": current_station, "end":next_station[0], "time":next_station[1]}

                current_station = next_station[0]

                # Add new step to route
                connection_list.append(connection)
                route.connection_list = connection_list

            # If route is too long, break
            else:
                break

        # Add route to our list of routes
        route_list.append(route)

    solution = sn.Solution(route_list, station_dict)
    solution.print_solution()

    # for i in range(max_trains):
    #     print(solution.solution_list[i].connection_list)
    #     print("\n")

    return solution, station_dict
