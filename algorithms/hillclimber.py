from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
from functions import helper
import random as rd

def hillclimber(solution, route_iterations = 10000, connection_iterations = 0):
    """ This implementation of a hillclimber contains two different iterations,
    one based on replacing routes and one based on replacing only the begin and
    end of a route.

    Args:
        solution: An instance of the solution class, possibly containing routes.
        route_iterations: The number of route iterations, default is 10000.
        connection_iterations: the number of connection iterations, dfault is 0.

    Returns:
        solution: An instance of the solution class.
    """
    # Fill solution with empty routes if the route_list is empty.
    if solution.route_list == []:
        for i in range(solution.max_trains):
            route = rt.Route([])
            solution.route_list.append(route)

    score = solution.score()

    # perform te iterations
    for _ in range(route_iterations):
        route_index, new_route = iteration_routes(solution)
        score, solution = check_for_improvement(score, solution, route_index, new_route)

    for _ in range(connection_iterations):
        route_index, new_route = iteration_connections(solution)
        score, solution = check_for_improvement(score, solution, route_index, new_route)

    return solution


def iteration_routes(solution):
    """ An iteration of the hillclimber. A random new route is created, then a
    random route is chosen, and replaced by the new route. If the score improves
    we hold on to the change.

    Args:
        old_score: Double representing the score of the solution.
        solution: An instnace of the solution class.
    Returns:
        The score of the old or new solution as double.
    """
    # Choose route to swap out.
    route_index = rd.randint(0, solution.max_trains - 1)

    # create route to replace it with
    route = helper.create_random_route(solution)

    return route_index, route

def iteration_connections(solution):
    """ An iteration of the hillclimber. A random route is chosen, then with
    certain probability we remove either the first or final connection and with
    certain probability we place a new connection on the first or final
    connection. This happens independentely. If the score improves we hold on to
    the change.

    Args:
        solution: An instance of the solution class.
        old_score: The score of the solution
    Returns:
        A solution and it's score.
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
    score improves, if it does not, we revert the change.

    Args:
        old_score: double that holds the value the old score.
        solution: the solution as a solution object.
        route_index: integer for which route to swap with.
        new_route: a route to swap into the solution

    Returns:
        The score of the solution we end up with.
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
    """ Cut the begin or end of a route off, with certain probability.

    Args:
        route: The route to change.

    Returns:
        route: The route with it's end's 'changed'.
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
    limit. There is a 1/3 chance to not add a new endpoint.

    Args:
        route: A string, containing the name of the station.
        soluiton: An instance of the solution classs.

    Returns:
        route: The route with it's new endpoint.
    """

    random_choice = 3 * rd.random()

    # Add random new begin.
    if random_choice < 1:
        # Choose first connection, or a random station if there is none.
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
        # Choose last connection, or a random station if there is none.
        if route.connection_list != []:
            begin_station = route.connection_list[len(route.connection_list)-1]["end"]
        else:
            begin_station = rd.choice(solution.station_dict_key_list)
        end_station = rd.choice(solution.station_dict[begin_station].neighbors)
        # Add new connection to route, if this doens't exceed the time limit.
        if route.time() + end_station[1] < solution.max_minutes:
            route.append_route(begin_station, end_station[0], end_station[1])

    return route
