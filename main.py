from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
from algorithms import random as ra
from algorithms import greedy_algorithm as ga
import plot_data as pd
import loading_files as load
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
        choices=['random', 'greedy'], required=True, help="specify which algorithm to run")

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

    args = parser.parse_args()

    visual = args.visual
    times = args.times
    store = args.store
    algo = args.algorithm
    score = 0
    outfile = 0

    # Create filename to save scores in.
    folder_output = "./data/scores/"
    filename = datetime.datetime.now().strftime("scores__%Y-%m-%d__%I%M%S.csv")
    outfile = os.path.join(folder_output, filename)

    # Open file and create writer to enter score in to the file.
    with open(outfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|',
            quoting=csv.QUOTE_MINIMAL)

        for i in range(times):
            if (algo == 'greedy'):
                solution,station_dict = greedy_alg(7, 120)
            elif (algo == 'random'):
                solution,station_dict = random_alg(7, 120)
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

def holland_main():
    """ Load stations. """
    load.load_stations()


def random_alg(max_trains, max_minutes):
    """ Random solution.

    Returns:
        A random solution.
    """
    return ra.random(max_trains, max_minutes)


def greedy_alg(max_trains, max_minutes):
    """ Greedy solution.

    Returns:
        A Greedy solution.
    """
    return ga.greedy(max_trains, max_minutes)


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


if __name__ == "__main__":
    main(sys.argv[1:])
