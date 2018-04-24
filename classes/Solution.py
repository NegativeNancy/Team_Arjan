class Solution():
    """Class that holds possible solutions and computes their score."""

    def __init__(self, solution_list, station_dict):
        """Initialise class."""
        self.solution_list = solution_list
        self.station_dict = station_dict

    def score(self, number_of_all_critical_stations):
        """Returns score of solution."""
        self.number_critical_stations = 0
        for key, value in station_dict:
            if value.critical == True and value.been == True:
                self.number_critical_stations += 1

        self.p = self.number_critical_stations / self.number_of_all_critical_stations * 100
        

        # Compute time spent on rails
        self.min = 0
        for traject in self.solution_list:
            self.min += traject.time

        # Routes used in solution equals length of solution list
        self.t = len(self.solution_list)

        # The actual function
        self.s = p*10000-(self.t*20+self.min/10)


# greedy function die ieder stap kprste spppr kiest
# if niet kan dan gewoon random stap.
