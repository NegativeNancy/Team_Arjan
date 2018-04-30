from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
from algorithms import random as ra
import plot_data as pd
import loading_files as load
import random, sys, getopt, csv, os, os.path, datetime, time

def main(argv):
    """ Main function calling all algorithms.

    Args:
        args: Command-line argument that determines which algortihm
            should be called. Can include prompt for visualisation.
    """

    start_time = time.time()
    algo = ''
    visual = False
    score = 0
    times = 0
    outfile = 0
    visual = 0

    try:
        opts, args = getopt.getopt(argv,"ht:a:v",["times=", "algorithm=", "visual="])
    except getopt.GetoptError:
        print ('Use main.py -h to view all possible arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('main.py -t or --times = <times to run>, -a or --algorithm \
                == <algorithm to run>')
            exit(1)
        elif opt in ("-t", "--times"):
            times = int(arg)
        elif opt in ("-a", "--algorithm"):
            algo = arg
        elif opt in ("-v", "--visual"):
            visual = True;

    if times > 0:
        folder_output = "./data/scores/"
        filename = datetime.datetime.now().strftime("scores__%Y-%m-%d__%I%M%S.csv")

        outfile = os.path.join(folder_output, filename)

        with open(outfile, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for i in range(times):
                solution,station_dict = random_alg(7, 120)
                temp = solution.score()
                spamwriter.writerow([temp])

                if score < temp:
                    score = temp
                    print(score)

        run_time = time.time() - start_time

        print_score(run_time, times, score, outfile, visual)
        exit(1)
    else:
        solution,station_dict = random_alg(7, 120)
        run_time = time.time() - start_time
        print_score(run_time, times, score, outfile, visual)
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


def create_visual(filename):
    """ Create plot from data.

    Args:
        filename: Datafile to plot data from.
    """
    pd.plot_data(filename)


def print_score(run_time, times_ran, score, outfile, visual):
    """ Prints score of solution.

    Args:
        run_time: Amount of times algortihm should be run.
        times_run: Times algorithm has ran.
        score: Score of solution.
        outfile: Outfile to write data to.
        visual: Boolean determining whether to visualise the data.
    """
    print("\nTime to run: ", run_time)

    if visual:
        create_visual(outfile)

    print("Times ran: ", times_ran)
    print("Highest score: ", score)


if __name__ == "__main__":
    main(sys.argv[1:])
