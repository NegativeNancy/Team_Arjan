from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
from functions import helper as helper
import math
import random as rd


def random(solution, times = 500):
    """ Creates a number of random route lists (500 by default) and returns the
    solution, with the route list that has in the highest score.

    Args:
        solution: An instance of the solution class, with empty route list.
        times: The number of times random is ran internally.

    Returns:
        best_solution: An instance of the solution class, with filled route list.
    """
    # Initialse our best solution thus far.
    best_solution = sn.Solution([], solution.station_dict, \
        solution.max_trains, solution.max_minutes, solution.station_dict_key_list)
    best_score = best_solution.score()

    # Create random solutions and update our best solution if needed.
    for time in range(times):
        # Set up our route list with an empty list.
        solution.route_list = []

        # Make a new random solution and check for improvement.
        solution = create_random_solution(solution)
        if solution.score() > best_score:
            best_score = solution.score()
            best_solution.route_list = solution.route_list

    return best_solution

def create_random_solution(solution):
    """ Finds a set of random routes.

    Args:
        solution: An instance of the solution class, with empty route list.

    Returns:
        A randomly egenerated solution.
    """

    # Determine how many trains can travel.
    number_of_trains = rd.randint(int(solution.max_trains - \
    math.sqrt(solution.max_trains)), solution.max_trains)

    # Ensure our solution will contain maximum ammount of trains.
    for _ in range(solution.max_trains - number_of_trains):
        solution.route_list.append(rt.Route([]))

    # Create random routes.
    for _ in range(number_of_trains):
        route = helper.create_random_route(solution)
        solution.route_list.append(route)

    return solution
