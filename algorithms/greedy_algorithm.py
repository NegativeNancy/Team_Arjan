"""
Algortihm that finds the shortest path to the next critical station.
If a critcial station cannot directly be reached, choose a random next step.

Begin on a node with one critical connection.
Do not go back to the previous station

Create a random solution where the starting station is different each time
"""
import loading_files as load
from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import random as rd

def greedy(max_trains, max_minutes):
    """ Greedy algorithm that hopes to fin the perfect solutioinself.
    Args:
        max_trains: Maximum amount of trains allowed in solution.
        max_minutes: Maximum amount of minutes the solution may take.

    Returns;
        The solution: a combination of routes.
    """
    station_dict = load.load_stations()
    route_list = []
    station_dict_key_list = []

    for key in station_dict:
        station_dict_key_list.append(key)

    for i in range(max_trains): # might be interesting to randomize the ammount of trains
        travel_time = 0
        begin_station = st.Stations("fake_begin",  False)
        end_station = st.Stations("fake_end",  False)
        end_station_index = 0
        best_end_station_index = 0

        # Variables for greedy algorithm
        connection_list = []
        route = rt.Route(connection_list)

        # Arbitrarally chosen time, might need improvement
        best_time = 1000

        # Find best begin station
        # Loop over station dict
        for station in station_dict_key_list:
            end_station_index = 0
            # Loop over neighbors of station
            for neighbor in station_dict[station].neighbors:
                end_station_index += 1
                # Check that connection is critical and not used yet
                if neighbor[2] == True and neighbor[3] == False:
                    if travel_time == 0 or neighbor[1] < travel_time:
                        begin_station = station
                        end_station = neighbor[0]
                        travel_time = neighbor[1]
                        best_end_station_index = end_station_index

        station_dict[begin_station].neighbors[best_end_station_index - 1][3] = True
        for neighbor in station_dict[end_station].neighbors:
            if neighbor[0] == begin_station:
                neighbor[3] = True
        print(begin_station)
        print(end_station)

        index = 0
        best_index = 0
        been = False
        current_station = begin_station
        next_station = end_station
        for neighbor in station_dict[current_station].neighbors:
            # Determine closest critical neighbor that has not been explored
            if neighbor[1] < best_time and neighbor[2] and not neighbor[3]:
                best_time = neighbor[1]

                # Remember index where best neighbor is
                best_index = index
                been = True

            index += 1
            if been:
                next_station =  station_dict[current_station].neighbors[best_index]
            else:
                print("new route up next")
                break



            connection = {"begin": station_dict[current_station].name, "end": next_station[0], "time": next_station[1]}
            print(connection)
            current_station = next_station[0]

            # Add new step to route
            connection_list.append(connection)
            route.connection_list = connection_list
