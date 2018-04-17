from classes import Stations as st
from classes import Connections as cs
from classes import Route as rt
from classes import Solution as sn
import random

connections = list()
def holland_main():
    load_connections()
    load_stations()

def load_connections():
    """Loads the connections into the designated object."""
    connection_list = []
    connections_file = open("original_files/ConnectiesHolland.csv")
    # Split line on comma and load in class
    for line in connections_file:
        obj = line.split(',')
        connection = cs.Connections(obj[0], obj[1], obj[2])
        connections.append(connection)

def load_stations():
    """Loads the stations from the CSV file into the designated object."""
    station_list = []
    station_file = open("original_files/StationsHolland.csv")
    # Determine cirtical stations and add to class
    for line in station_file:
        obj = line.split(',')
        if obj[3] == "Kritiek\n":
            station = st.Stations(obj[0], obj[1], obj[2], True)
            # Make list of critical stations
            station_list.append(station)
        else:
            station = st.Stations(obj[0], obj[1], obj[2])
    a_solution(station_list)
        # Adding variabels to dictionary so it can be used in quick visualisation.
        #station_dict = list()
        # station_dict.append({"name": obj[0]})
        # station_dict.append({"longitude": obj[1]})
        # station_dict.append({"latitude": obj[2]})

def a_solution(station_list):
    """Finds a set of connections"""
    #print(random_int)
    #print(station_list[random_int].name)
    # zoek naam stations connections
    # pak de eerste die je tegen komt
    # Einde traject
    end_time = 0
    for station in station_list:
        attempt = sn.Solution
        for connection in connections:
            if connection.begin == station.name or connection.end == station.name:
                print(connection.begin)
                route = [connection.begin, connection.end]
                duration = connection.time
                route = rt.Route(route)
                print(route.time)
                end_time += int(duration)
                attempt.append(route, end_time)
                print(end_time)

                break






holland_main()
