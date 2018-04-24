"""RailNL optimal route finder"""

from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import loading_files as lf
import random


def main():
    connections = list()
    holland_main()
    exit(0)


def holland_main():
    lf.load_stations()
