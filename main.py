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

from functions import helper

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

    optional.add_argument('--demo', action='store_true',
        help='run demo site with routes - default: false')
    optional.add_argument("-h", "--help", action="help",
        help="show this help message and exit")
    optional.add_argument('-s', '--store', action='store_true',
        help="store the results in a .scv file - default: false")
    optional.add_argument('-t', '--times', action='store', type=int, nargs='?',
        const=0, default=1, help="specify how many times to run - default: 1", )
    optional.add_argument('-v', '--visual', action='store_true',
        help="create visual of the results - default: false")
    optional.add_argument('--version', action='version', version='%(prog)s 0.1')
    optional.add_argument('-l', '--load', action='store', default='netherlands',
        choices=['netherlands', 'netherlands-simple', 'holland', 'holland-simple'],
        help='specify which scenario needs to be loaded - default: netherlands')

    args = parser.parse_args()

    algo = args.algorithm
    demo = args.demo
    scenario = args.load
    store = args.store
    times = args.times
    visual = args.visual

    station_dict, train, max_time = helper.load_scenario(scenario)
    solution = helper.init_solution(station_dict, train, max_time)

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
            solution = helper.run_algorithm(algo, solution)

            temp = solution.score()
            spamwriter.writerow([temp])

            if score < temp:
                score = temp
                print(score)

    run_time = time.time() - start_time

    solution.print_solution()
    helper.print_score(run_time, times, score, outfile, visual, store)

    if (store != True):
        os.remove(outfile)
    if (demo):
        call(['flask', 'run'])

    exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
