class Solution():
    """Class that holds possible solutions and computes their score."""

    def __init__(self, solution_list, station_dict):
        """Initialise class.

        Args:
            solution_list: A list with the routes that make up the solution.
            station_dict: A dctionary that contains the stations with its neighbours.
        """
        self.solution_list = solution_list # dit moet route_list worden!
        self.station_dict = station_dict

    def score(self):
        """ Computes score of solution.

        Returns:
            An integer repereseting the score of the solution.
        """

        number_critical_stations = 0
        number_of_all_critical_stations = 0
        for key in self.station_dict:
            for route in self.station_dict[key].neighbors:
                if route[2] == True and route[3] == True:
                    number_critical_stations += 1
                if route[2] == True:
                    number_of_all_critical_stations += 1

        p = number_critical_stations / number_of_all_critical_stations

        # Compute time spent on rails
        min = 0
        t = 0
        for route in self.solution_list:
            if route.connection_list[0]["begin"] != None:
                min += route.time()
                # Routes used in solution
                t += 1

        # The actual function
        score = p*10000-(t*20+min/10)

        return score

    def print_solution(self):
        for route in self.solution_list:
            for connection in route.connection_list:
                print ("begin:", connection["begin"], "end:", connection["end"] )
