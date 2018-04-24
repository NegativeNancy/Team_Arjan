from classes import Stations as st

def load_stations():
    """Loads the stations from the CSV file into the designated object.
    Also load in the connections ad neighbors to each station."""


    station_dict = {}
    station_file = open("Data/StationsHolland.csv")
    # Determine cirtical stations and add to class
    for line in station_file:
        obj = line.split(',')
        if obj[3] == "Kritiek\n":
            station = st.Stations(obj[0],  True)
            # Make list of critical stations
        else:
            station = st.Stations(obj[0])

        station_dict[obj[0]] = station

    connections_file = open("Data/ConnectiesHolland.csv")
    for line in connections_file:
        obj = line.split(',')

        if (station_dict[obj[0]].critical == True or station_dict[obj[1]].critical == True):
            station_dict[obj[0]].neighbors.append((obj[1], obj[2], True, False))
            station_dict[obj[1]].neighbors.append((obj[0], obj[2], True, False))


        else:
            station_dict[obj[0]].neighbors.append((obj[1], obj[2], False, False))
            station_dict[obj[1]].neighbors.append((obj[0], obj[2], False, False))

    for key,value in station_dict.items():
        print(value.name, value.critical, value.neighbors)









        # Adding variabels to dictionary so it can be used in quick visualisation.
        #station_dict = list()
        # station_dict.append({"name": obj[0]})
        # station_dict.append({"longitude": obj[1]})
        # station_dict.append({"latitude": obj[2]})
