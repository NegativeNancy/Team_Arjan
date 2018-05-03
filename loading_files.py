from classes import Stations as st


def load_stations(netherland, all_critical):
    """ Loads data from files and makes objects out of the data.

    Args:
        netherland: Boolean that is true if want to load netherland,
                    otherwise is false.
        all_critical: Boolean that is true if we want all stations to be
                      critical, is false otherwise.
    Returns:
        A dictionary with the station as key and the neighbours as properties.
    """

    station_dict = {}
    if netherland:
        station_file = open("data/StationsNationaal.csv")
    else:
        station_file = open("data/StationsHolland.csv")

    # Determine cirtical stations and add to class
    for line in station_file:
        obj = line.split(',')

        # Make list of stations and specify if station is critical
        if all_critical or obj[3] == "Kritiek\n" or obj[3] == "Kritiek\r\n":
            station = st.Stations(obj[0], True)
        else:
            station = st.Stations(obj[0])

        station_dict[obj[0]] = station

    station_file.close()

    if netherland:
        connections_file = open("data/ConnectiesNationaal.csv")
    else:
        connections_file = open("data/ConnectiesHolland.csv")
        
    for line in connections_file:
        obj = line.split(',')
        obj[2] = int(obj[2])

        # Distinguish between critical neighbours and non-critical neighbours
        if (station_dict[obj[0]].critical is True
                or station_dict[obj[1]].critical is True):
            station_dict[obj[0]].append_neighbor(obj[1], obj[2], True)
            station_dict[obj[1]].append_neighbor(obj[0], obj[2], True)
        else:
            station_dict[obj[0]].append_neighbor(obj[1], obj[2])
            station_dict[obj[1]].append_neighbor(obj[0], obj[2])

    connections_file.close()
    return station_dict
