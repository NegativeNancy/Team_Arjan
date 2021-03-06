from functions import helper
from classes import Solution
import sys, os, time, argparse, pickle


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
        choices=['random', 'greedy', 'genetic', 'hillclimber', 'annealing'], required=True,
        help="specify which algorithm to run")

    optional = parser.add_argument_group('Optional arguments')

    optional.add_argument('--demo', action='store_true',
        help='run demo site with routes - default: false')
    optional.add_argument("-h", "--help", action="help",
        help="show this help message and exit")
    optional.add_argument('-s', '--scenario', action='store', default='netherlands',
        choices=['netherlands', 'netherlands-simple', 'holland', 'holland-simple'],
        help='specify which scenario needs to be loaded - default: netherlands')
    optional.add_argument('--store', action='store_true',
        help="store the results in a .scv file - default: false")
    optional.add_argument('-t', '--times', action='store', type=int, nargs='?',
        const=0, default=1, help="specify how many times to run - default: 1")
    optional.add_argument('-v', '--visual', action='store_true',
        help="create visual of the results - default: false")

    optional.add_argument('--version', action='version', version='%(prog)s 1.0')
    optional.add_argument('--temp', action='store', type=int, nargs='?',
        default='1000', help="the maximum temp of the cooling function as integer")
    optional.add_argument('--cooling', action='store', type=int, nargs='?',
        default='0', choices=[0, 1, 2, 3], help="an integer representing the choice of cool function")
    optional.add_argument('-i', '--ignore', action='store',
        help='ignore station - default: none')
    optional.add_argument('--start', action='store', type=int, nargs='?',
        default = '0', choices=[0, 1, 2], \
        help="an integer representing the choice of soluiton to use as input - default: 0" )
    optional.add_argument('--route', action='store', type=int, nargs='?',
        default ='0', help="an integer representing how many iterations on routes should be ran - default: 0")
    optional.add_argument('--connection', action='store', type=int, nargs='?',
        default = '0', help="an integer representing how many iterations on connections should be ran - default: 0")

    args = parser.parse_args()

    algo = args.algorithm
    demo = args.demo
    scenario = args.scenario
    store = args.store
    times = args.times
    visual = args.visual
    temp = args.temp
    cooling = args.cooling
    ignore = args.ignore
    start_algorithm = args.start
    route_iterations = args.route
    connection_iterations = args.connection

    station_dict, train, max_time = helper.load_scenario(scenario, ignore)

    solution = helper.init_solution(station_dict, train, max_time)
    best_solution, best_score = helper.init_best_solution(solution, \
        station_dict, train, max_time)

    best_solution, best_score, outfile, score = helper.run_times(times, algo, \
        solution, best_solution, best_score, temp, cooling, \
        start_algorithm, route_iterations, connection_iterations)

    run_time = time.time() - start_time

    best_solution.print_solution()
    helper.print_score(run_time, times, score, outfile, visual, store)

    if store != True:
        os.remove(outfile)

    if (demo):
        helper.run_demo(scenario)

    os.remove("./data/temp/displayroute.csv")

    exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
