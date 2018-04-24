class Stations(object):
    def __init__(self, name, critical = False):

        self.name = name
        self.critical = critical
        self.neighbors = []

    def critical_stations(self, station_list):
        """"Loops over stations and returns a list with all critical stations."""

        critical_station_list = []
        for sation in station_list:
            if station.critical:
                critical_station_list.append(station)
        return critical_station_list
