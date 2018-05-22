"""
Algortihm that finds the shortest path to the next critical station.
If a critcial station cannot directly be reached, choose a random next step.

Begin on a node with one critical connection.
Do not go back to the previous station

Create a random solution where the starting station is different each time
"""
from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import random as rd

def greedy(solution):
    """ Greedy algorithm that hopes to fin the perfect solutioinself.
    Args:
        max_trains: Maximum amount of trains allowed in solution.
        max_minutes: Maximum amount of minutes the solution may take.

    Returns;
        The solution: a combination of routes.
    """

    route_list = []

    for i in range(solution.max_trains): # might be interesting to randomize the ammount of trains, or proof this is never the case
        travel_time = 0
        begin_station = st.Stations("fake_begin",  False)
        end_station = st.Stations("fake_end",  False)
        end_station_index = 0
        best_end_station_index = 0
        found_another_station = False
        # Variables for greedy algorithm
        connection_list = []
        route = rt.Route(connection_list)

        # Find best begin station
        # Loop over station dict
        for station in solution.station_dict_key_list:
            end_station_index = 0
            # Loop over neighbors of station
            for neighbor in solution.station_dict[station].neighbors:
                # Check that connection is critical and not used yet
                if neighbor[2] and not neighbor[3]:
                    if travel_time == 0 or neighbor[1] < travel_time:
                        begin_station = station
                        end_station = neighbor[0]
                        travel_time = neighbor[1]
                        best_end_station_index = end_station_index
                        found_another_station = True
                end_station_index += 1

        if not found_another_station:
            solution.route_list = route_list
            solution.print_solution()
            return solution
            break

        set_been_to_true(solution, begin_station, end_station, best_end_station_index)
        connection = {"begin": begin_station, "end": end_station, "time": neighbor[1]}

        # Add new step to route
        connection_list.append(connection)
        route.connection_list = connection_list

        while True:
            result = determine_joint_closest_neighbor(begin_station, end_station, solution.station_dict)
            new_station = result[0]
            neighbor_of_new_station = result[1]
            found_new_station = result[2]

            if not found_new_station:
                break

            if neighbor_of_new_station == begin_station:

                time_to = solution.station_dict[begin_station].neighbors[result[2]][1]
                if time_to + route.time() > solution.max_minutes:
                    break
                set_been_to_true(solution.station_dict, begin_station, new_station, result[2])

                connection = {"begin": begin_station, "end": new_station, "time": time_to}
                begin_station = new_station

            elif neighbor_of_new_station == end_station:

                time_to = solution.station_dict[end_station].neighbors[result[2]][1]
                if time_to + route.time() > solution.max_minutes:
                    break
                set_been_to_true(solution.station_dict, end_station, new_station, result[2])

                connection = {"begin": end_station, "end": new_station, "time": time_to}
                end_staion = new_station

            else:
                print ("Something went wrong!")
                break

            # Add new step to route

            connection_list.append(connection)
            route.connection_list = connection_list

        # Add newly created route to route_list
        route_list.append(route)

    solution = sn.Solution(route_list, solution)

    solution.print_solution()

    return solution



def determine_joint_closest_neighbor(begin_station, end_station, solution):
    """ Finds the closest unused, critical neighbor of two stations.

    Args:
        begin_station, end_station: Station names as strings.

    Returns:
        Name of the closest neighbor and to which station it's a neighbor.
    """

    travel_time = 0
    new_station_index = 0
    best_new_station_index = 0
    neighbor_of_begin_station = True
    found_suitable_result = False

    # Loop over neighbors of begin_station
    for neighbor in solution.station_dict[begin_station].neighbors:
        # Check that connection is critical and not used yet
        if neighbor[2] == True and neighbor[3] == False:
            if travel_time == 0 or neighbor[1] < travel_time:
                travel_time = neighbor[1]
                best_new_station_index = new_station_index
                found_suitable_result = True
        new_station_index += 1

    # Reset index of best new station
    new_station_index = 0

    # Loop over neighbors of end_station
    for neighbor in solution.station_dict[end_station].neighbors:
        # Check that connection is critical and not used yet
        if neighbor[2] == True and neighbor[3] == False:
            if travel_time == 0 or neighbor[1] < travel_time:
                travel_time = neighbor[1]
                best_new_station_index = new_station_index
                neighbor_of_begin_station = False
                found_suitable_result = True
        new_station_index += 1

    if neighbor_of_begin_station:
        name_new_station = station_dict[begin_station].neighbors[best_new_station_index][0]
        return name_new_station, begin_station, best_new_station_index, found_suitable_result


    name_new_station = station_dict[end_station].neighbors[best_new_station_index][0]
    return name_new_station, end_station, best_new_station_index, found_suitable_result



def set_been_to_true(solution, begin_station, end_station, best_end_station_index):
    """ Sets been property of station to true.

    Args:
        begin_station: Station where connection begins.
        end_station: Station where connection ends.
        best_end_station_index: index of best station found.
    """
    solution.station_dict[begin_station].neighbors[best_end_station_index][3] = True
    for neighbor in station_dict[end_station].neighbors:
        if neighbor[0] == begin_station:
            neighbor[3] = True
            break

def closest_neighbor(station, solution):
    """ Find closest not used, critical neighbor for a station.

    Args:
        station: Name of station whose neighbor we seek.
        station_dict: Current station dict.

    Returns:
        name of closest neighbor
        index of neighbor in neighbor_list of station
        time to travel to neighbor from station
    """

    travel_time = 0
    new_station_index = 0
    best_new_station_index = 0
    # Loop over neighbors of begin_station
    for neighbor in solution.station_dict[station].neighbors:
        # Check that connection is critical and not used yet
        if neighbor[2] == True and neighbor[3] == False:
            if travel_time == 0 or neighbor[1] < travel_time:
                travel_time = neighbor[1]
                best_end_station_index = new_station_index
        new_station_index += 1

    name_new_station = solution.station_dict[station].neighbors[best_new_station_index][0]
    travel_time = solution.station_dict[station].neighbors[best_new_station_index][1]
    return name_new_station, best_new_station_index, travel_time
