import loading_files as load
from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import random as rd

def test(max_trains, max_minutes):
    station_dict = load.load_stations()
    route_list = []
    station_dict_key_list = []

    for key in station_dict:
        station_dict_key_list.append(key)

    for i in range(max_trains):
        connection_list = []
        route = rt.Route(connection_list)
        current_station = rd.choice(station_dict_key_list)

        best_time = 1000
        while True:
            index = 0
            best_index = 0
            been = False
            next_station = current_station
            #print("new iter")
            for neighbor in station_dict[current_station].neighbors:
            #    print("New neighbour")
                # Determine closest critical neighbor that has not been explored
                if neighbor[1] < best_time and neighbor[2] and not neighbor[3]:
                    best_time = neighbor[1]

                    # Remember index where best neighbor is
                    best_index = index
                    been = True

                #print(best_index)
                index += 1
                #print(station_dict[current_station].name)
                #print(best_time)
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


            break


    # for key, value in station_dict.items():
    #     if key == current_station:
    #         for n in value.neighbors:
    #             print(key)
    #             print(n)
    #             if n[1]

test(7, 120)
