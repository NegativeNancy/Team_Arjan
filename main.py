"""RailNL optimal route finder"""

from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
from algorithms import random as ra
import loading_files as load
import random, sys, getopt, csv, os, os.path, datetime

def main(argv):

    time = 0
    algo = ''
    score = 0

    try:
        opts, args = getopt.getopt(argv,"ht:a",["times=", "algorithm="])
    except getopt.GetoptError:
        print ('Use main.py -h to view all possible arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('main.py -t or --times = <times to run>, -a or --algorithm \
                == <algorithm to run>')
        elif opt in ("-t", "--times"):
            times = int(arg)
        elif opt in ("-a", "--algorithm"):
            algo = arg

    if times > 0:
        folder_output = "./data/scores/"
        filename = datetime.datetime.now().strftime("scores__%Y-%m-%d__%I%M%S.csv")

        outfile = os.path.join(folder_output, filename)

        with open(outfile, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
 
            for i in range(times): 
                solution,station_dict = random_alg()
                temp = solution.score()
                spamwriter.writerow([temp])

                if score < temp:
                    score = temp
                    print(score)


        print("\n")
        print("Times runned: ", times)
        print("Highst score: ", score)
    else:
        solution,station_dict = random_alg()
        print(solution.score())


def holland_main():
    load.load_stations()


def random_alg():
    return ra.random()
    

if __name__ == "__main__":
    main(sys.argv[1:])

   