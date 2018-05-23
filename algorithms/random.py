from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import random as rd

def random(solution, random_number_trains = True, times = 1000):
    """ Creates a number of random route list (1000 by default) and returns the
    route list that results in the highest score.

    Args:
        solution: An instance of the solution class, with empty route list.

    Returns:
        best_solution: An instance of the solution class, with filled route list.
    """
    solution.route_list = []
    # Initialse our best solution thus far.
    best_solution = sn.Solution([], solution.station_dict, \
    solution.max_trains, solution.max_minutes, solution.station_dict_key_list)
    best_score = best_solution.score()

    # Create random solutions and update our best_solution if needed.
    for time in range(times):
        solution = create_random_solution(solution, random_number_trains)
        if solution.score() > best_score:
            best_score = solution.score()
            best_solution.route_list = solution.route_list

        # Reset our route_list for next iteration.
        solution.route_list = []

    return best_solution

def create_random_solution(solution, random_number_trains):
    """ Finds a set of random routes.

    Args:
        solution: An instance of the solution class, with empty route list.

    Returns:
        solution: An instance of the solution class, with filled route list.
    """

    # Determine how many trains can travel.
    if random_number_trains:
        number_of_trains = rd.choice(range(int(solution.max_trains / 2), \
        solution.max_trains + 1))

        # Ensure our solution will contain 7 trains.
        for empty_trains in range(solution.max_trains - number_of_trains):
            solution.route_list.append(rt.Route([]))
    else:
        number_of_trains = solution.max_trains

    # Create routes that trains will travel.
    for i in range(number_of_trains):
        route = create_random_route(solution)
        solution.route_list.append(route)

    return solution


def create_random_route(solution):
    """Create a random route.

    Args:
        solution: An instance of the solution class.

    Returns:
        route: A randomly generated route.
    """
    connection_list = []
    route = rt.Route(connection_list)
    current_station = rd.choice(solution.station_dict_key_list)
    time_of_route = 0

    while True:
        next_station = rd.choice(solution.station_dict[current_station].neighbors)

        # Check whether route won't be longer than allowed.
        if next_station[1] + route.time() < solution.max_minutes:
            route.append_route(current_station, next_station[0], next_station[1])
            current_station = next_station[0]
        else:
            break
    return route
