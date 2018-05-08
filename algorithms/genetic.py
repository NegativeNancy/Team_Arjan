from algorithms import random as ra
from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn


def genetic(list_of_solutions):
    print("genetic")

    best_score
    score_list = []


    # Return best two solutions
    # Let them make a child

    # Caclulate score, save best in best_score and best_solution
    score_tuple = calc_overall_fitness(list_of_solutions)
    score_list = score_tuple[0]
    best_score = score_tuple[1]
    # Make children ?

    #



def calc_overall_fitness(list_of_solutions):
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

    """"
    print("make_population")

    solution_list = []

    for i in range(population_size):
        ra.random(max_trains, max_time)

    return solution_list

def selection():
    print("selection")

def make_child():
    print("make_child")

def mutation():
    print("mutation")
