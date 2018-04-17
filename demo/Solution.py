class Solution():

    def __init__(self, solution_list):
        self.solution_list = solution_list

    def socre(self, p, t, min):
        self.s = p*10000-(t*20+min/10)
