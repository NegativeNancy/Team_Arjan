class Solution():
    """Class that holds possible solutions and computes their score."""

    def __init__(self, solution_list, station_dict):
        """Initialise class.

        Args:
            solution_list: A list with the routes that make up the solution.
            station_dict: A dctionary that contains the stations with its neighbours. 
        """
        self.solution_list = solution_list
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
        for route in self.solution_list:
            min += route.time()

        # Routes used in solution equals length of solution list
        t = len(self.solution_list)

        # The actual function
        score = p*10000-(t*20+min/10)

        return score


# greedy function die ieder stap kprste spppr kiest
# if niet kan dan gewoon random stap.
