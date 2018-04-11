import Stations as st
import Connections as cs
def holland_main():
    load_connections()
    load_stations()

def load_connections():
    connection_list = []
    connections_file = open("files/ConnectiesHolland.csv")
    for line in connections_file:
        obj = line.split(',')
        connection = cs.Connections(obj[0], obj[1], obj[2])

def load_stations():
    station_list = []
    station_file = open("files/StationsHolland.csv")
    for line in station_file:
        obj = line.split(',')
        if obj[3] == "Kritiek\n":
            station = st.Stations(obj[0], obj[1], obj[2], True)
            # Is dit wel een goed idee?
            station_list.append(station)
        else:
            station = st.Stations(obj[0], obj[1], obj[2])




holland_main()
