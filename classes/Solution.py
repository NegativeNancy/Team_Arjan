class Solution():
    """Class that holds possible solutions and computes their score."""

    def __init__(self, route_list, station_dict, max_trains, max_minutes, station_dict_key_list):
        """Initialise class.

        Args:
            route_list: A list with the routes that make up the solution.
            station_dict: A dctionary that contains the stations with its neighbours.
        """

        self.route_list = route_list
        self.station_dict = station_dict
        self.max_trains = max_trains
        self.max_minutes = max_minutes
        self.station_dict_key_list = station_dict_key_list

    def score(self):
        """ Computes score of solution.

        Returns:
            An integer repereseting the score of the solution.
        """

        p = self.compute_p()

        # Compute time spent on rails
        min = 0
        t = 0
        for route in self.route_list:
            if route.connection_list == []:
                t += 0
            else:
                min += route.time()
                # Routes used in solution
                t += 1

        # The actual function
        score = p*10000-(t*20+min/10)

        return score

    def print_solution(self):
        for route in self.route_list:
            for connection in route.connection_list:
                print ("begin:", connection["begin"], "end:", connection["end"] )
            print("End of route")

    def route_used(self, begin_station, end_station):
        """Determines wheterer a connection is in the solution.

        Args:
            begin_station, end_station: Strings containing the names of the
            stations.

        Returns:
            1 if the connection is in the solution, 0 otherwise.
        """
        for route in self.route_list:
            for connection in route.connection_list:
                if (connection["begin"] == begin_station and connection["end"] \
                == end_station) or (connection["end"] == begin_station and \
                connection["begin"] == end_station):
                    return 1
        return 0

    def compute_p(self):
        number_used_critical_routes = 0
        number_of_all_critical_routes = 0
        for station in self.station_dict:
            for neighbor in self.station_dict[station].neighbors:
                if neighbor[2] == True:
                    number_of_all_critical_routes += 1
                    number_used_critical_routes += self.route_used(station, neighbor[0])

        p = number_used_critical_routes / number_of_all_critical_routes

        return p 
