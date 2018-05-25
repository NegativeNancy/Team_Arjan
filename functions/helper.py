from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
from algorithms import random as ra
from algorithms import greedy as ga
from algorithms import genetic as gena
from algorithms import hillclimber as hill
from algorithms import simulated_annealing as an
from functions import plot_data as pd
from functions import loading_files as load
from subprocess import call
import random as rd
import csv, datetime, os, sys


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


def init_best_solution(solution, station_dict, train, max_minutes):
    """ Initialize the best solution

    Args:
        solution: The current solution to be stored as the best solution.
        station_dict: Station dict of the stations that can be used.
        train: Number of trains that can be used.
        max_minutes: Maximum ammount of time a route can take.

    Return:
        Current best solution with the current best score.
    """
    best_solution = sn.Solution([], solution.station_dict, \
        solution.max_trains, solution.max_minutes, solution.station_dict_key_list)
    best_score = best_solution.score()

    return best_solution, best_score


def file_location_score():
    """ Create filename to save scores in.

    Return:
        Filelocation to save the score in.
    """
    folder_output = "./data/scores/"
    filename = datetime.datetime.now().strftime("scores__%Y-%m-%d__%I%M%S.csv")
    outfile = os.path.join(folder_output, filename)

    return outfile


def store_solution(solution):
    """ Create filename to save the route in.

    Return:
        Filelocation to save the route in.
    """
    outfile = "./data/temp/displayroute.csv"

    with open(outfile, 'w', newline="") as csvfile:
        fieldnames = [ 'begin_station', 'end_station', 'critical']
        routewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for route in solution.route_list:
            for connection in route.connection_list:
                routewriter.writerow({'begin_station': connection["begin"],
                    'end_station': connection["end"], 'critical': ''})

    return outfile


def run_demo(scenario):
    """ Start a Flask instance with local variables to be display the visualization.

    Args:
        scenario: The scenario that was used to run the algorithm.
    """
    os.environ["FLASK_APP"] = "run_demo.py"
    os.environ["API_KEY"] = "AIzaSyBp387L8lSCBXL_sQlrJHs1hdTiShlD29Y"
    os.environ["RAILNL_SCENARIO"] = scenario
    call(['flask', 'run'])


def run_times(times, algo, solution, best_solution, best_score, temperature, \
    cooling, start_algorithm, route_iterations, connection_iterations):
    """ Runs the specified algorithm <times>, with specified input solution.

    Args:
        times:
        alo:
        solution:
        best_solution:
        best_score:
        steps:
        temperature:
        cooling:
        start_algorithm:
        route_iterations:
        connection_iterations:

    Return:
        Returns the best solution, best score, location of score file and the score.
    """
    score = 0

    outfile = file_location_score()

    with open(outfile, "w", newline="") as csvfile:
        scorewriter = csv.writer(csvfile, delimiter=" ", quotechar="|",
            quoting=csv.QUOTE_MINIMAL)

        for _ in range(times):
            solution.route_list = []

            solution = run_algorithm(algo, solution, temperature, cooling, \
                start_algorithm, route_iterations, connection_iterations)

            temp = solution.score()
            scorewriter.writerow([temp])

            if score <= temp:
                score = temp
                print(score)

            best_solution, best_score = keep_best_solution(solution, \
                best_solution, best_score)
            store_solution(best_solution)

    return best_solution, best_score, outfile, score


def run_algorithm(algo, solution, temperature, cooling, start_algorithm, \
    route_iterations, connection_iterations):
    """ Determine which algorithm to run.

    Args:
        algo: Name of the algorithm to run.
        solution: Empty instance of solution object.

    """
    # Make correct start solution.
    if start_algorithm == 1:
        solution = ga.greedy(solution)
    elif start_algorithm == 2:
        solution = ra.random(solution)

    if (algo == "greedy"):
        solution = greedy_alg(solution)
    elif (algo == "random"):
        solution = random_alg(solution)
    elif algo == "genetic":
        solution = genetic_alg(solution)
    elif algo == "hillclimber":
        # Set default if none specified.
        if route_iterations == 0 and connection_iterations == 0:
            route_iterations = 10000
        solution = hillclimber_alg(solution, route_iterations, connection_iterations)
    elif algo == "annealing":
        # Set default if none specified.
        if route_iterations == 0 and connection_iterations == 0:
            connection_iterations = 10000
        solution == annealing_alg(solution, cooling, temperature, \
            route_iterations, connection_iterations)
    else:
        exit()

    return solution


def keep_best_solution(solution, best_solution, best_score):
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

    return best_solution, best_score


def annealing_alg(solution, cooling, temperature, route_iterations, connection_iterations):
    """ Simulated Annealing solution.

    Args:
        solution: Empty instance of solution object.
        cooling: Integer representing the cooling scheme chosen.
        temperature: Integer representing the start temperature of the algorithm.
        route_iterations: The number of route iterations to do.
        connection_iterations: The number of connection iterations to do.

    Returns:
        A Greedy solution.
    """
    return an.simulated_annealing(solution, cooling, temperature, \
        route_iterations, connection_iterations)


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


def hillclimber_alg(solution, route_iterations, connection_iterations):
    """ Hillclimber solution.

    Args:
        solution: Empty instance of solution object.
        route_iterations: Number of route iterations to do.
        connection_iterations: Number of connection iterations to do.

    Returns:
        A Hillclimber solution.
    """
    return hill.hillclimber(solution, route_iterations, connection_iterations)


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


def load_scenario(scenario, ignore = ""):
    """ Specify which scenario to load.

    Args:
        scenario: Name of scenario to load.
    """

    trains_netherlands = 20
    time_netherlands = 180
    trains_holland = 7
    time_holland = 120

    if (scenario == "netherlands"):
        station_dict = load.load_stations(True, True, ignore)
        print("Netherlands Loaded")
        train = trains_netherlands
        max_time = time_netherlands
    elif (scenario == "netherlands-simple"):
        station_dict = load.load_stations(True, False, ignore)
        print("Netherlands Simple Loaded")
        train = trains_netherlands
        max_time = time_netherlands
    elif (scenario == "holland"):
        station_dict = load.load_stations(False, True, ignore)
        print("Holland Loaded")
        train = trains_holland
        max_time = time_holland
    elif (scenario == "holland-simple"):
        station_dict = load.load_stations(False, False, ignore)
        print("Holland Simple Loaded")
        train = trains_holland
        max_time = time_holland
    return station_dict, train, max_time


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
