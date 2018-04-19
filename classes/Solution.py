class Solution():
    """Class that holds possible solutions and computes their score."""

    def __init__(self, solution_list):
        """Initialise class."""
        self.solution_list = solution_list

    def socre(self, p):
        """Compute score of solution."""
        # Compute time spent on rails
        self.min = 0
        for traject in self.solution_list:
            self.min += traject.time

        # Routes used in solution equals length of solution list
        self.t = len(self.solution_list)

        # The actual function
        self.s = p*10000-(self.t*20+self.min/10)