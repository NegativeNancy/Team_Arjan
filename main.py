"""RailNL optimal route finder"""

from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
from algorithms import random as ra
import loading_files as lf
import random



def main():
    # connections = list()
    # station_list = holland_main()
    solution,station_dict = random_alg()
    print(solution.score())


def holland_main():
    lf.load_stations()


def random_alg():
    return ra.random()

if __name__ == "__main__":
    main()
