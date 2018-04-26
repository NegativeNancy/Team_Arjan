from classes import Stations as st


def load_stations():
    """Loads the stations from the CSV file into the designated object.
    Also load in the connections ad neighbors to each station."""

    station_dict = {}
    station_file = open("data/StationsHolland.csv")
    # Determine cirtical stations and add to class
    for line in station_file:
        obj = line.split(',')

        # Make list of stations and specify if station is critical
        if obj[3] == "Kritiek\n" or obj[3] == "Kritiek\r\n":
            station = st.Stations(obj[0],  True)
        else:
            station = st.Stations(obj[0])

        station_dict[obj[0]] = station

    connections_file = open("Data/ConnectiesHolland.csv")
    for line in connections_file:
        obj = line.split(',')
        obj[2] = int(obj[2])

        # Distinguish between critical neighbours and non-critical neighbours
        if (station_dict[obj[0]].critical is True
                or station_dict[obj[1]].critical is True):
            station_dict[obj[0]].neighbors.append([obj[1], obj[2], True, False])
            station_dict[obj[1]].neighbors.append([obj[0], obj[2], True, False])
        else:
            station_dict[obj[0]].neighbors.append([obj[1], obj[2], False, False])
            station_dict[obj[1]].neighbors.append([obj[0], obj[2], False, False])

    return station_dict
