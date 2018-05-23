
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
    for i in range(route_iterations):
        _, score = iteration_routes(score, solution)
    for j in range(connection_iterations):
        _, score = iteration_connections(score, solution)

    return solution


def iteration_routes(old_score, solution):
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

    return solution, check_for_improvement(old_score, solution, route_index, route)

def iteration_connections(old_score, solution):
    """ An iteration of the hillclimber. A random route is chosen, then with
    certain probability we remove either the first or final connection and with
    certain probability we place a new connection on the first or final
    connection. This happens independentely. If the score improves we hold on to
    the change.

    Args:
        max_trains: Integer representing the maximum number of trains allowed.
        max_minutes: Integer representing the maximum ammount of minutes traveled by a train.
        old_score: double representing the score of the solution.
        solution: input solution.
        i: integer to keep trac of the number of iteration.
    Returns:
        old_score, new_score: the score of the old or new solution is
        as integer.
    """
    # choose random route
    route_index = rd.randint(0, solution.max_trains - 1)
    old_route = solution.route_list[route_index]

    # copy route
    new_route = rt.Route(list(old_route.connection_list))

    # remove the start or end of route with certain probability, if possible
    if new_route.connection_list != []:
        random_int = 3 * rd.random()
        if random_int < 1:
            new_route.connection_list = new_route.connection_list[1:]
        elif random_int < 2:
            new_route.connection_list.pop()

    random_int2 = 3 * rd.random()
    if random_int2 < 1:
        # add random new begin, if it doesn't exceed the time
        if new_route.connection_list != []:
            end_station = new_route.connection_list[0]["begin"]
        else:
            end_station = rd.choice(solution.station_dict_key_list)
        begin_station = rd.choice(solution.station_dict[end_station].neighbors)
        if new_route.time() + begin_station[1] < solution.max_minutes:
            new_route.append_route_front(begin_station[0], end_station, begin_station[1])

    elif random_int2 < 2:
        # add random new end, if it doesn't exceed the time
        if new_route.connection_list != []:
            begin_station = new_route.connection_list[len(new_route.connection_list)-1]["end"]
        else:
            begin_station = rd.choice(solution.station_dict_key_list)
        end_station = rd.choice(solution.station_dict[begin_station].neighbors)
        if new_route.time() + end_station[1] < solution.max_minutes:
            new_route.append_route(begin_station, end_station[0], end_station[1])

    # check if score will improve
    return solution, check_for_improvement(old_score, solution, route_index, new_route)


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
        return new_score
    else:
        solution.route_list[route_index] = old_route
        return old_score
