from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import random as rd

def greedy(solution):
    """ Greedy algorithm that hopes to fin the perfect solutioinself.

    Args:
        solution: An instance of the solution class, possibly containing routes.

    Returns;
        The solution: a combination of routes.
    """

    connection_archive = set()

    for i in range(solution.max_trains):
        connection_list = []
        route = rt.Route(connection_list)

        # Find best begin station.
        begin_station, end_station, travel_time, best_end_station_index, found_another_station = find_best_begin_station(solution, connection_archive)

        # Quit if no solution was found.
        if not found_another_station:
            return solution

        append_to_connection_archive(connection_archive, begin_station, end_station)
        connection = {"begin": begin_station, "end": end_station, "time": travel_time}

        # Add new step to route.
        connection_list.append(connection)
        route.connection_list = connection_list

        # Look for the best, closest, critical route.
        find_new_connection(begin_station, end_station, solution, connection_archive, route)

        # Add newly created route to route_list.
        solution.route_list.append(route)

    return solution

def find_new_connection(begin_station, end_station, solution, connection_archive, route):
    """ Finds the closest, critical, nonnection.

    Args:
        begin_station: One end of the current connection.
        end_station: The other end of the current connection.
        solution: An instance of the solution class.
        connection_archive: A set containing all visited connections.
        route: An empty instance of a route object.
    """
    while True:
        new_station, neighbor_of_new_station, best_new_station_index, \
        found_new_station = determine_joint_closest_neighbor(begin_station, \
        end_station, solution.station_dict, connection_archive)

        if not found_new_station:
            break

        # Try to add new connection to the front of the route.
        if neighbor_of_new_station == begin_station:
            time_to = solution.station_dict[begin_station].neighbors[best_new_station_index][1]
            if time_to + route.time() > solution.max_minutes:
                break
            append_to_connection_archive(connection_archive, begin_station, new_station)

            route.append_route_front(new_station, begin_station, time_to)
            begin_station = new_station

        # Try to add new connection to the back of the route.
        else:
            time_to = solution.station_dict[end_station].neighbors[best_new_station_index][1]
            if time_to + route.time() > solution.max_minutes:
                break
            append_to_connection_archive(connection_archive, end_station, new_station)

            route.append_route(end_station, new_station, time_to)
            end_station = new_station

def find_best_begin_station(solution, connection_archive):
    """ Finds the best station to begin the route.

    Args:
        solution: An instance of the solution class.
        connection_archive: A set containing all visited connections.

    Returns:
        The best begin station, the best end station,
            the travel time between the two, the index of the end station in
            the neighbor list of the begin station, and a boolean stating whether
            a new beginning was found.
    """
    travel_time = 0
    begin_station = st.Stations("fake_begin",  False)
    end_station = st.Stations("fake_end",  False)
    best_end_station_index = 0
    found_another_station = False

    for station in solution.station_dict_key_list:
        end_station_index = 0
        # Look at neighbors of station.
        for neighbor in solution.station_dict[station].neighbors:
            # Check that connection is critical and not used yet.
            if neighbor[2] and (neighbor[0], station) not in connection_archive and (station, neighbor[0]) not in connection_archive:
                if travel_time == 0 or neighbor[1] < travel_time:
                    begin_station = station
                    end_station = neighbor[0]
                    travel_time = neighbor[1]
                    best_end_station_index = end_station_index
                    found_another_station = True
            end_station_index += 1

    return begin_station, end_station, travel_time, best_end_station_index, \
    found_another_station

def determine_joint_closest_neighbor(begin_station, end_station, station_dict, \
        connection_archive):
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

    # Loop over neighbors of begin_station.
    for neighbor in station_dict[begin_station].neighbors:
        # Check that connection is critical and not used yet.
        if neighbor[2] == True and (neighbor[0], begin_station) not in \
        connection_archive and (begin_station, neighbor[0]) not in connection_archive:
            if travel_time == 0 or neighbor[1] < travel_time:
                travel_time = neighbor[1]
                best_new_station_index = new_station_index
                found_suitable_result = True
        new_station_index += 1

    # Reset index of best new station.
    new_station_index = 0

    # Loop over neighbors of end_station.
    for neighbor in station_dict[end_station].neighbors:
        # Check that connection is critical and not used yet.
        if neighbor[2] == True and (neighbor[0], end_station) not in \
        connection_archive and (end_station, neighbor[0]) not in connection_archive:
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

def closest_neighbor(station, solution, connection_archive):
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
        if neighbor[2] == True and (neighbor[0], station) not in \
        connection_archive and (station, neighbor[0]) not in connection_archive:
            if travel_time == 0 or neighbor[1] < travel_time:
                travel_time = neighbor[1]
                best_end_station_index = new_station_index
        new_station_index += 1

    name_new_station = solution.station_dict[station].neighbors[best_new_station_index][0]
    travel_time = solution.station_dict[station].neighbors[best_new_station_index][1]

    return name_new_station, best_new_station_index, travel_time

def append_to_connection_archive(connection_archive, begin_station, end_station):
    """ Adds a connection the the connection archive set.

    Args:
        connection_archive: A set containing all vistied connections.
        begin_station: One end of the connection.
        end_station: The other end of the connection.
    """
    connection_archive.add((begin_station, end_station))
    connection_archive.add((end_station, begin_station))
