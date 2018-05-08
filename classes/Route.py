class Route():
    """Class that holds single route objects."""

    def __init__(self, connection_list):
        """Initialise class."""
        self.connection_list = connection_list

    def time(self):
        """ Computes time it takes to finish routes.

        Returns:
            An integer with the amount of time spent driving. Time in minutes.
        """
        time = 0
        for connection in self.connection_list:
            time += connection["time"]
        return time

    def append_route(self, begin_station, end_station, time):
        self.connection_list.append({"begin": begin_station, "end": end_station, "time": time})
