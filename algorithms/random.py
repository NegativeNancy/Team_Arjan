from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
from functions import helper as helper
import random as rd


def random(solution, random_number_trains = True, times = 1000):
    """ Creates a number of random route list (1000 by default) and returns the
    route list that results in the highest score.

    Args:
        solution: An instance of the solution class, with empty route list.
        times: The number of times random is ran internally.

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

def create_random_solution(solution, random_number_trains = True):
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
        route = helper.create_random_route(solution)
        solution.route_list.append(route)

    return solution
