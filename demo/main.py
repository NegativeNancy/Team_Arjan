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
    station_dict = list()
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

        # Adding variabels to dictionary so it can be used in visualisation.
        station_dict.append({"name": obj[0]})
        station_dict.append({"longitude": obj[1]})
        station_dict.append({"latitude": obj[2]})
        print(station_dict[0]["longitude"])


holland_main()
