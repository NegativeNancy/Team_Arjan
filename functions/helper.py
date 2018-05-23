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
import random as rd
import random, sys, getopt, csv, os, os.path, datetime, time, argparse


def init_solution(station_dict, max_trains, max_minutes):
    """ Initialize a new solluiton.

    Args:
        station_dict: Station dict of the stations that can be used.
        max_trains: Number of trains that can be used.
        max_minutes: Maximum ammount of time a route can take.

    Return:
        Start solution with empty route list.
    """
    key_list = []
    for station in station_dict:
        key_list.append(station)

    solution = sn.Solution([], station_dict, max_trains, max_minutes, key_list)

    return solution


def best_solution(solution, best_solution, best_score):
    """ Save new solition as best solution if better than previous solution.

    Args:
        solution: New solution that has been found.
        best_solution: Current best solution.
        best_score: Current best score.

    Return:
        Returns the currnt best solution and the current best score.

    """
    current_score = solution.score()

    # Update the best_solution if needed.
    if current_score > best_score:
        best_score = current_score
        best_solution.route_list = solution.route_list

    # Reset our route_list for next iteration.
    solution.route_list = []

    return best_solution, best_score


def run_algorithm(algo, solution):
    """ Determine which algorithm to run.

    Args:
        algo: Name of the algorithm to run.
        solution: Empty instance of solution object.

    """
    if (algo == 'greedy'):
        solution = greedy_alg(solution)
    elif (algo == 'random'):
        solution = random_alg(solution)
    elif algo == 'genetic':
        solution = genetic_alg(solution)
    elif algo == 'hillclimber':
        solution = hillclimber_alg(ra.create_random_solution(solution))
    else:
        exit()

    return solution


def random_alg(solution, random_number_trains = True):
    """ Random solution.

    Args:
        solution: Empty instance of solution object.
        random_number_trains: Boolean to determine if random trains is enabled.

    Returns:
        A random solution.
    """
    return ra.random(solution, random_number_trains)


def greedy_alg(solution):
    """ Greedy solution.

    Args:
        solution: Empty instance of solution object.

    Returns:
        A Greedy solution.
    """
    return ga.greedy(solution)


def genetic_alg(solution):
    """ Genetic solution.

    Args:
        solution: Empty instance of solution object.

    Returns:
        A Genetic solution.
    """
    return gena.genetic(solution)


def hillclimber_alg(solution):
    """ Hillclimber solution.

    Args:
        solution: Empty instance of solution object.

    Returns:
        A Hillclimber solution.
    """
    return hill.hillclimber(solution)


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

def create_random_route(solution):
    """ Create a random route.

    Args:
        solution: An instance of the solution class.

    Returns:
        The route that we created.
    """
    connection_list = []
    route = rt.Route(connection_list)

    # Choose begin station.
    begin_station = rd.choice(solution.station_dict_key_list)

    #  Create a new route.
    while True:
        route_time = route.time()

        weight = 0.1 * route_time / solution.max_minutes
        if 0.05 + weight > rd.random():
            break

        end_station = rd.choice(solution.station_dict[begin_station].neighbors)

        if route_time + end_station[1] < solution.max_minutes:
            route.append_route(begin_station, end_station[0], end_station[1])
            begin_station = end_station[0]
        else:
            break

    return route
