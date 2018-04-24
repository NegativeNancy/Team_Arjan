"""Algortihm that finds the shortest path to the next critical station.
If a critcial station cannot directly be reached, choose a random next step.

Begin on a node with one critical connection.
"""

from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import loading_files as lf

def greedy():
    station_dict = loading_files.load_stations()

    # Find station with one critical unused connection.
    for key, value in station_dict.items():
        
