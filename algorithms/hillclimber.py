from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
from functions import helper
import random as rd
import numpy as np
import matplotlib.pyplot as plt

def hillclimber(solution, route_iterations = 10000, connection_iterations = 0):
    """ Hillclimber algortihm that tries to find the optimal set of routes,
    A.K.A. an optimal solution.

    This implementation of a hillclimber contains two different iterations,
    one based on replacing routes and one based on replacing only the beginning and
    ending of a route.

    Args:
        solution: An instance of the solution class, possibly containing routes.
        route_iterations: The number of route iterations, default is 10000.
        connection_iterations: The number of connection iterations, default is 0.

    Returns:
        The solution.
    """
    # Fill solution with empty routes if the route list is empty.
    if solution.route_list == []:
        for i in range(solution.max_trains):
            route = rt.Route([])
            solution.route_list.append(route)

    score = solution.score()

    scores_array = []

    # Perform the route iteration the specified amount of times.
    for _ in range(int(route_iterations / 100)):
        for _ in range(100):
            route_index, new_route = iteration_routes(solution)
            score, solution = check_for_improvement(score, solution, route_index, new_route)
        scores_array.append(solution.score())

    # Perform the connection iteration the specified amount of times.
    for _ in range(int(connection_iterations / 100)):
        for _ in range(100):
            route_index, new_route = iteration_connections(solution)
            score, solution = check_for_improvement(score, solution, route_index, new_route)
        scores_array.append(solution.score())

    return solution, scores_array


def iteration_routes(solution):
    """ Iteration of the hillclimber that swithces out routes.

    A random new route is created, then a random route is chosen, and replaced
    by the new route. If the score improves we hold on to the change.

    Args:
        solution: An instnace of the solution class.

    Returns:
        The index of the route, and the route itself.
    """
    # Choose route to swap out.
    route_index = rd.randint(0, solution.max_trains - 1)

    # Create route to replace it with.
    route = helper.create_random_route(solution)

    return route_index, route


def iteration_connections(solution):
    """ Iteration of the hillclimber that swithces out connections within routes.

    A random route is chosen, then with a certain probability either the first
    or last connection is removed. With a certain probability a new connection
    is placed at the location of the first or last connection. This happens
    independently. If the score improves, the change is accepted.

    Args:
        solution: An instance of the solution class.
        old_score: The score of the solution

    Returns:
        The index of the new route, and the new route itself.
    """
    # Choose random route.
    route_index = rd.randint(0, solution.max_trains - 1)
    old_route = solution.route_list[route_index]

    new_route = rt.Route(list(old_route.connection_list))

    # Determine which end is cut of, if any.
    new_route = cut_route_ends(new_route)

    new_route = add_new_endpoint(new_route, solution)

    # Return proposed changes.
    return route_index, new_route


def check_for_improvement(old_score, solution, route_index, new_route):
    """Inserts a new route at certain place in a solution and checks if the
    score improves. If it does not, we revert the change.

    Args:
        old_score: Double that holds the value the old score.
        solution: The solution as a solution object.
        route_index: Integer for which route to swap with.
        new_route: A route to swap into the solution.

    Returns:
        The solution and the (new) score.
    """
    # Store old route, then replace it with the new route.
    old_route = solution.route_list[route_index]
    solution.route_list[route_index]= new_route
    new_score = solution.score()

    # Check if this improves the score, otherwise revert changes.
    if old_score < new_score:
        return new_score, solution
    else:
        solution.route_list[route_index] = old_route
        return old_score, solution


def cut_route_ends(route):
    """ Cut the begin or end off of a route, with a certain probability.

    Args:
        route: The route to change.

    Returns:
        The route with its ends 'changed'.
    """
    # Check if route is not empty.
    if route.connection_list != []:
        # Random variable to choose what case is chosen.
        random_choice = 3 * rd.random()
        if random_choice < 1:
            route.connection_list = route.connection_list[1:]
        elif random_choice < 2:
            route.connection_list.pop()
    return route


def add_new_endpoint(route, solution):
    """ Randomly add a new endpoint to a route, if this does not exceed the time
    limit.

    There is a 1/3 chance to not add a new endpoint.

    Args:
        route: A string, containing the name of the station.
        soluiton: An instance of the solution classs.

    Returns:
        The route with its new endpoint.
    """

    random_choice = 3 * rd.random()

    # Add random new beginning.
    if random_choice < 1:
        # Choose first connection, or a random station if there is no first connection.
        if route.connection_list != []:
            end_station = route.connection_list[0]["begin"]
        else:
            end_station = rd.choice(solution.station_dict_key_list)

        begin_station = rd.choice(solution.station_dict[end_station].neighbors)

        # Add new connection to route, if this doens't exceed the time limit.
        if route.time() + begin_station[1] < solution.max_minutes:
            route.append_route_front(begin_station[0], end_station, begin_station[1])

    # Add random new end.
    elif random_choice < 2:
        # Choose last connection, or a random station if there is no last connection.
        if route.connection_list != []:
            begin_station = route.connection_list[len(route.connection_list)-1]["end"]
        else:
            begin_station = rd.choice(solution.station_dict_key_list)

        end_station = rd.choice(solution.station_dict[begin_station].neighbors)

        # Add new connection to route, if this doens't exceed the time limit.
        if route.time() + end_station[1] < solution.max_minutes:
            route.append_route(begin_station, end_station[0], end_station[1])

    return route
