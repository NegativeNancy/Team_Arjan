"""
Algortihm that finds the shortest path to the next critical station.
If a critcial station cannot directly be reached, route stops.

Begin on a node with one critical connection.
Do not go back to the previous station

Create a random solution where the starting station is different each time
"""
from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import random as rd

def hillclimber(station_dict, max_trains, max_minutes, number_of_iterations_a = 1000, number_of_iterations_b = 0 ):

    route_list = []
    station_dict_key_list = []
    solution = sn.Solution(route_list, station_dict)

    for key in station_dict:
        station_dict_key_list.append(key)

    # make an 'empty' connection_list
    connection_list = []
    # connection_list.append({"begin": None, "end": None, "time": 0})


    # make a solution of empty routes
    for i in range(max_trains):
        route = rt.Route(connection_list)
        solution.route_list.append(route)


    score = solution.score()

    for i in range(number_of_iterations_a):
        score = iteration_routes(station_dict, station_dict_key_list, max_trains, max_minutes, score, solution, i)
    print ("Loop 1:")
    print(score)
    for j in range(number_of_iterations_b):
        score = iteration_connections(station_dict, station_dict_key_list, max_trains, max_minutes, score, solution, j)
    print ("Loop 2:")
    print(score)
    return solution, station_dict


def iteration_routes(station_dict, station_dict_key_list, max_trains, max_minutes, old_score,  solution, i):
    """ An iteration of the hillclimber. A random new route is created, then a
    random route is chosen, and replaced by the new route. If the score improves
    we hold on to the change.

    Args:
        station_dict: The station dict, holding the graph.
        station_dict_key_list: List of keys of the station dict.
        max_trains: Integer representing the maximum number of trains allowed.
        max_minutes: Integer representing the maximum ammount of minutes traveled by a train.
        old_score: double representing the score of the solution.
        solution: input solution.
        i: integer to keep trac of the number of iteration.
    Returns:
        old_score, new_score: the score of the old or new solution is
        as integer.
    """
    connection_list = []
    route = rt.Route(connection_list)
    route_index = rd.randint(0, max_trains - 1)

    begin_station = rd.choice(station_dict_key_list)

    #  create a new route
    while True:
        route_time = route.time()

        weight = 0.1 * route_time/ max_minutes
        if 0.05 + weight > rd.random():
            break

        end_station = rd.choice(station_dict[begin_station].neighbors)

        if route_time + end_station[1] < max_minutes:
            route.append_route(begin_station, end_station[0], end_station[1])
            begin_station = end_station[0]
        else:
            break

    old_route = solution.route_list[route_index]
    solution.route_list[route_index] = route
    new_score = solution.score()

    if old_score < new_score:
        return new_score
    else:
        solution.route_list[route_index] = old_route
        return old_score

def iteration_connections(station_dict, station_dict_key_list, max_trains, max_minutes, old_score, solution, j):
    """ An iteration of the hillclimber. A random route is chosen, then with
    certain probability we remove either the first or final connection and with
    certain probability we place a new connection on the first or final
    connection. This happens independentely. If the score improves we hold on to
    the change.

    Args:
        station_dict: The station dict, holding the graph.
        station_dict_key_list: List of keys of the station dict.
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
    route_index = rd.randint(0, max_trains - 1)
    old_route = solution.route_list[route_index]

    # copy route
    new_route = rt.Route(list(old_route.connection_list))

    # remove the begin or end of route with certain probability, if possible
    if new_route.connection_list != []:
        random_int = 3 * rd.random()
        if random_int < 1:
            # remove begin
            new_route.connection_list = new_route.connection_list[1:]
        elif random_int < 2:
            new_route.connection_list.pop()

    random_int2 = 3 * rd.random()
    if random_int2 < 1:
        # add random new begin
        if new_route.connection_list != []:
            end_station = new_route.connection_list[0]["begin"]
        else:
            end_station = rd.choice(station_dict_key_list)
        begin_station = rd.choice(station_dict[end_station].neighbors)
        if new_route.time() + begin_station[1] < max_minutes:
            new_route.append_route_front(begin_station[0], end_station, begin_station[1])

    elif random_int2 < 2:
        if new_route.connection_list != []:
            begin_station = new_route.connection_list[len(new_route.connection_list)-1]["end"]
        else:
            begin_station = rd.choice(station_dict_key_list)
        end_station = rd.choice(station_dict[begin_station].neighbors)
        if new_route.time() + end_station[1] < max_minutes:
            new_route.append_route(begin_station, end_station[0], end_station[1])


    # check if new route is better, otherwise revert changes
    solution.route_list[route_index]= new_route # put all of this in a function later?
    new_score = solution.score()

    if old_score < new_score:
        print ("score updated to:")
        print (new_score)
        print ("in iteration: ", j)
        return new_score
    else:
        solution.route_list[route_index] = old_route
        return old_score

# implement a cleanup function that removes stupidities from solutions.
