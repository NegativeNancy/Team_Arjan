class Stations(object):
    def __init__(self, name, x, y, critical = False, connection_list):
        self.neighbor_list = []
        for connection in connection_list:
            if connection[0] == name:
                self.neighbor_list.append((connection[1], connection[2]))
            elif connection[1] == name:
                self.neighbor_list.append((connection[0], connection[2]))

        self.name = name
        self.x = x
        self.y = y
        self.critical = critical
        self.neighbors = neighbor_list # de root van een linked list van neighbors

    def critical_stations(self, station_list):
        """"Loops over stations and returns a list with all critical stations."""

        critical_station_list = []
        for sation in station_list:
            if station.critical:
                critical_station_list.append(station)
        return critical_station_list
