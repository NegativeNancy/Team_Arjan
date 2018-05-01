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

    for i in range(max_trains): # might be interesting to randomize the ammount of trains
        travel_time = 0
        begin_station = st.Stations("fake_begin",  False)
        end_station = st.Stations("fake_end",  False)
        end_station_index = 0
        best_end_station_index = 0

        # Loop over station dict
        for station in station_dict_key_list:
            end_station_index = 0
            # Loop over neighbors of station
            for neighbor in station_dict[station].neighbors:
                end_station_index += 1
                # Check that connection is critical and not used yet
                if neighbor[2] == True and neighbor[3] == False:
                    # if neighbor[0] == "Rotterdam Centraal" or neighbor[0] == "Schiedam Centrum":
                    #     print(neighbor)
                    # # Check if the connection is faster than the current one
                    if travel_time == 0 or neighbor[1] < travel_time:
                        begin_station = station
                        end_station = neighbor[0]
                        travel_time = neighbor[1]
                        best_end_station_index = end_station_index

        station_dict[begin_station].neighbors[best_end_station_index - 1][3] = True
        for neighbor in station_dict[end_station].neighbors:
            if neighbor[0] == begin_station:
                neighbor[3] = True
        #print(station_dict[begin_station].neighbors[best_end_station_index - 1])
        print(begin_station)
        print(end_station)



test(7, 120)

# kies korste pad als begin
