from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
from algorithms import random as ra
from algorithms import greedy as ga
from algorithms import genetic as gena
from algorithms import hillclimber as hill
from functions import plot_data as pd
from functions import loading_files as load
from subprocess import call
import random, sys, getopt, csv, os, os.path, datetime, time, argparse


def run_algorithm(algo, station_dict, train, max_time):
    if (algo == 'greedy'):
        solution,station_dict = greedy_alg(station_dict, train, max_time)
    elif (algo == 'random'):
        solution,station_dict = random_alg(station_dict, train, max_time)
    elif algo == 'genetic':
        solution, station_dict = genetic_alg(station_dict, train, max_time)
    elif algo == 'hillclimber':
        solution, station_dict = hillclimber_alg(station_dict, train, max_time)
    else:
        exit()

    return solution, station_dict


def random_alg(station_dict, max_trains, max_minutes):
    """ Random solution.

    Args:
        max_trains: Maximum amount of trains the solution may use.
        max_minutes: Maximum amount of minutes the solution may take.

    Returns:
        A random solution.
    """
    return ra.random(station_dict, max_trains, max_minutes)


def greedy_alg(station_dict, max_trains, max_minutes):
    """ Greedy solution.

    Args:
        max_trains: Maximum amount of trains the solution may use.
        max_minutes: Maximum amount of minutes the solution may take.

    Returns:
        A Greedy solution.
    """
    return ga.greedy(station_dict, max_trains, max_minutes)


def genetic_alg(station_dict, max_trains, max_minutes):
    """ Genetic solution.

    Args:
        max_trains: Maximum amount of trains the solution may use.
        max_minutes: Maximum amount of minutes the solution may take.

    Returns:
        A Genetic solution.
    """
    return gena.genetic(station_dict, max_trains, max_minutes)


def hillclimber_alg(station_dict, max_trains, max_minutes):
    """ Hillclimber solution.

    Args:
        max_trains: Maximum amount of trains the solution may use.
        max_minutes: Maximum amount of minutes the solution may take.

    Returns:
        A Hillclimber solution.
    """
    return hill.hillclimber(station_dict, max_trains, max_minutes)


def print_score(run_time, times_ran, score, outfile, visual, store):
    """ Prints score of solution.

    Args:
        run_time: Amount of times algortihm should be run.
        times_run: Times algorithm has ran.
        score: Score of solution.
        outfile: Outfile to write data to.
        visual: Boolean determining whether to visualise the data.
    """
    print("\nTime to run: ", run_time)
    print("Times ran: ", times_ran)
    print("Highest score: ", score)

    if store:
        print("File stored as: ", outfile)

    if visual:
        create_visual(outfile)


def create_visual(filename):
    """ Create plot from data.

    Args:
        filename: Datafile to plot data from.
    """
    pd.plot_data(filename)


def load_scenario(scenario):
    """ Specify which scenario to load.

    Args:
        scenario: Name of scenario to load.
    """

    trains_netherlands = 20
    time_netherlands = 180
    trains_holland = 7
    time_holland = 120

    if (scenario == 'netherlands'):
        station_dict = load_file(True, True)
        train = trains_netherlands
        max_time = time_netherlands
    elif (scenario == 'netherlands-simple'):
        station_dict = load_file(True, False)
        train = trains_netherlands
        max_time = time_netherlands
    elif (scenario == 'holland'):
        station_dict = load_file(False, True)
        train = trains_holland
        max_time = time_holland
    elif (scenario == 'holland-simple'):
        station_dict = load_file(False, False)
        train = trains_holland
        max_time = time_holland
    return station_dict, train, max_time


def load_file(file, critical):
    """ Specify which files to load.

    Args:
        file: Boolean detemining 
        critical: 
    
    """

    if (file == True and critical == True):
        print("Netherlands Loaded")
        station_dict = load.load_stations(True, True)
        return station_dict
    elif (file == True and critical == False):
        print("Netherlands Simple Loaded")
        station_dict = load.load_stations(True, False)
        return station_dict
    elif (file == False and critical == True):
        print("Holland Loaded")
        station_dict = load.load_stations(False, True)
        return station_dict
    elif (file == False and critical == False):
        print("Holland Simple Loaded")
        station_dict = load.load_stations(False, False)
        return station_dict
