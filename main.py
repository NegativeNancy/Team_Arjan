from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
from algorithms import random as ra
from algorithms import greedy_algorithm as ga
from algorithms import genetic as gena
from algorithms import hillclimber as hill
from functions import plot_data as pd
from functions import loading_files as load
import random, sys, getopt, csv, os, os.path, datetime, time, argparse

class MyParser(argparse.ArgumentParser):
    """ Class that allows us to run help message when no arguments are given"""
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def main(argv):
    """ Main function calling all algorithms.
    Args:
        args: Command-line argument that determines which algortihm
            should be called. Can include prompt for visualisation and to
            store the results.
    """

    # Store start time of program.
    start_time = time.time()

    parser = MyParser(description='RailNL Discription!', add_help=False)

    required = parser.add_argument_group('Required argument')
    required.add_argument('-a', '--algorithm', action='store', dest="algorithm",
        choices=['random', 'greedy', 'genetic', 'hillclimber'], required=True, 
        help="specify which algorithm to run")

    optional = parser.add_argument_group('Optional arguments')

    optional.add_argument("-h", "--help", action="help",
        help="show this help message and exit")
    optional.add_argument('-s', '--store', action='store_true',
        help="store the results in a .scv file - default: false")
    optional.add_argument('-t', '--times', action='store', type=int, nargs='?',
        const=0, default=1, help="specify how many times to run - default: 1", )
    optional.add_argument('-v', '--visual', action='store_true',
        help="create visual of the results - default: false")
    optional.add_argument('--version', action='version', version='%(prog)s 0.1')
    optional.add_argument('-l', '--load', action='store', default='nederland',
        choices=['nederland', 'nederland-simple', 'holland', 'holland-simple'],
        help='specify which stationfiles needs to be loaded - default: nederland')

    args = parser.parse_args()

    visual = args.visual
    times = args.times
    store = args.store
    algo = args.algorithm
    load = args.load

    trains_netherlands = 20
    time_netherlands = 180
    trains_holland = 7
    time_holland = 120

    if (load == 'nederland'):
        station_dict = load_file(True, True)
        train = trains_netherlands
        max_time = time_netherlands
    elif (load == 'nederland-simple'):
        station_dict = load_file(True, False)
        train = trains_netherlands
        max_time = time_netherlands
    elif (load == 'holland'):
        station_dict = load_file(False, True)
        train = trains_holland
        max_time = time_holland
    elif (load == 'holland-simple'):
        station_dict = load_file(False, False)
        train = trains_holland
        max_time = time_holland

    # Create filename to save scores in.
    folder_output = "./data/scores/"
    filename = datetime.datetime.now().strftime("scores__%Y-%m-%d__%I%M%S.csv")
    outfile = os.path.join(folder_output, filename)

    score = 0

    # Open file and create writer to enter score in to the file.
    with open(outfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|',
            quoting=csv.QUOTE_MINIMAL)

        for i in range(times):
            if (algo == 'greedy'):
                solution,station_dict = greedy_alg(station_dict, train, max_time)
            elif (algo == 'random'):
                solution,station_dict = random_alg(station_dict, train, max_time)
            elif algo == 'genetic':
                solution, station_dict = genetic_alg(station_dict, train, max_time)
            elif algo == 'hillclimber':
                    solution, station_dict = hillclimber_alg(station_dict, train, max_time)
            else:
                print("You mother forker")
                exit()

            temp = solution.score()
            spamwriter.writerow([temp])

            if score < temp:
                score = temp
                print(score)

    run_time = time.time() - start_time

    print_score(run_time, times, score, outfile, visual, store)

    if (store != True):
        os.remove(outfile)

    exit(1)


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


def create_visual(filename):
    """ Create plot from data.

    Args:
        filename: Datafile to plot data from.
    """
    pd.plot_data(filename)


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


def load_file(file, critical):
    if (file == True and critical == True):
        print("Nederland Loaded")
        station_dict = load.load_stations(True, True)
        return station_dict
    elif (file == True and critical == False):
        print("Nederland Simple Loaded")
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


if __name__ == "__main__":
    main(sys.argv[1:])
