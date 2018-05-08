import random as ra
from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn

# Goede definitie van crossover
# Swap in hillclimber is mutatie

def genetic(station_dict, max_trains, max_time):
    print("genetic")

    # best_score
    # score_list = []
    # index = 0

    # Return best two solutions
    # Let them make a child

    # Caclulate score, save best in best_score and best_solution
    #score_list, best_score, index = calc_overall_fitness(list_of_solutions)
    # Make children ?

    #return [], []



def calc_fitness(list_of_solutions):
    """Calculates fitness of all solutions in solution listself.

    Args:
        list_of_solutions: List of all parent solutions

    Returns:
        A list of all scores in the list_of_solutions
        The best score
        The index of best score?

    """
    score_list = []
    best_score = 0
    index = 0
    for i in range(len(list_of_solutions)):
        score_list.append(sn.score(list_of_solutions[i]))
        if score_list[i] > best_score:
            best_score = score_list[i]
            index = i
    return score_list, best_score, index

    # Calculate score of solution


def make_population(population_size):
    """Generate a population consisted of random solutions.

    Args:
        population_size: Integers specifying how big the population should be.

    Returns:
        A list of [INTEGER] random solutions.

    """

    solution_list = []
    score_list = []

    for i in range(population_size):
        solution, station_dict = ra.random(station_dict, max_trains, max_time)
        solution_list.append(solution)
        score_list.append(sn.score())

    print(score_list)
    return solution_list

def selection():
    # Raise error ipv
    raise NotImplementedError

    # Alleen beste houden is niet altijd beste
    # moeilijk

def crossover():
    raise NotImplementedError


def mutation():
    raise NotImplementedError
