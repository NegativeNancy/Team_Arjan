def load_connections():
    """Loads the connections into the designated object."""
    connection_list = []
    connections_file = open("Data/ConnectiesHolland.csv")
    # Split line on comma and load in class
    for line in connections_file:
        obj = line.split(',')
        connection = cs.Connections(obj[0], obj[1], obj[2])
        connections.append(connection)

def load_stations():
    """Loads the stations from the CSV file into the designated object."""
    .................0000
    connection_list = load_connections()
    station_list = []
    station_file = open("Data/StationsHolland.csv")
    # Determine cirtical stations and add to class
    for line in station_file:
        obj = line.split(',')
        if obj[3] == "Kritiek\n":
            station = st.Stations(obj[0], obj[1], obj[2], True, connection_list)
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
