from algorithms import random as ra
from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import random as rd

def genetic(station_dict, max_trains, max_time):
    """ Algorithm that finds a genetic solution.

    Args:
        station_dict:
        max_trains: Maximum amount of trains allowed.
        max_minutes: Maximum amount of minutes the trains can run forself

    Returns:
        A genetically generted solution

    - Make initial population (make_population())
    - Match two solutions (pick_next_population_parents())
        - Do this for whole generation?
    - Cross these two pratens
    - Make sure they are part of the next generation

    """
    list_of_solutions = []
    score_list = []
    solution_list = []
    crossover_list = []
    crossover_solution_list = []
    crossover_score_list = []
    index_list = []
    listed = []

    crossover_list = make_list(max_trains)
    population_size = 1000

    # Make population.
    solution_list, score_list = make_population(population_size, station_dict, max_trains, max_time)

#    select_score(score_list)
    best_score = 0
    best_solution = sn.Solution([], station_dict)

    print(determine_best_score(score_list))
    worsened_solution = 0
    crossover_solution_list = []
    crossover_score_list = []
    worst_score = 100000
    index = 0
    generation = 0
    #worsened_solution < 25 or
    while generation < 500:
        crossover_solution_list = []
        crossover_score_list = []
        # Create next generation.
        for i in range(population_size):
            # Pick two parents.
            parents_index, parents = pick_next_population_parents(score_list, population_size)
            #print(index, index + 1)
            crossover_solution = crossover(crossover_list, max_trains, solution_list[parents_index[0]], solution_list[parents_index[1]], station_dict)
            crossover_solution_score = crossover_solution.score()
            crossover_solution_list.append(crossover_solution)
            crossover_score_list.append(crossover_solution_score)

            # Determine best score.
            if crossover_solution_score > best_score:
                best_score = crossover_solution_score
                best_solution = crossover_solution
                print("best score", best_score, "generation", generation)


            # Only allow solution to worsen a set amount of time.
            # if crossover_solution_score < worst_score or worst_score == crossover_solution_score:
            #     worsened_solution += 1
            #     worst_score = crossover_solution_score
            parents_index = []
            parents = []

        # print("mean")
        #calc_and_print_mean(crossover_score_list)

        solution_list = []
        solution_list = list(crossover_solution_list)
        generation += 1
        print(generation)

    # Find best crossover.
    print(best_solution.score())
    return best_solution, station_dict

def calc_and_print_mean(score_list):
    summer = sum(score_list)
    print(round(summer / 50, 1))


def determine_best_score(score_list):
    best_score = 0
    for i in score_list:
        if i > best_score:
            best_score = i
    return best_score

def pick_next_population_parents(score_list, population_size):
    """ Picks parents of the next generation.

    Args:
        population_size: Size of the population.

    Reutrns:
        List of indices that the selected parents are at and the actual selected solutionsself.
    """
    index_list = []
    listed = []

    # Select two solutions.
    for i in range(2):
        index, selected = select_score(score_list, population_size)
        index_list.append(index)
        listed.append(selected)

    return index_list, listed


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
        score_list.append(list_of_solutions[i].score())
        if score_list[i] > best_score:
            best_score = score_list[i]
            index = i

    return score_list, best_score, index

def select_score(score_list, population_size):
    """ Selects score to produce next population.

    Args:
        score_list: List of all the scores in the population.

    Returns:
        The index of the chosen score, and the score itself.
    """
    sum_of_scores = round(sum(score_list), 1)

    # Calculate chance of which score to pick.
    r = rd.random()
    chance = sum_of_scores * r
    new_sum_of_scores = 0
    index = 0

    # Loop through score list until new sum of scores is lower than the chance.
    for i in score_list:
        while new_sum_of_scores < chance:
            new_sum_of_scores += i
            index += 1

    return index % population_size, score_list[index % population_size]

def make_population(population_size, station_dict, max_trains, max_time):
    """ Generate a population consisted of random solutions.

    Args:
        population_size: Integers specifying how big the population should be.

    Returns:
        A list of random solutions, size of the list is the previously specified population size.

    """

    solution_list = []
    score_list = []
    # Create set amount of new solutions.
    for i in range(population_size):
        solution, station_dict = ra.random(station_dict, max_trains, max_time, False)
        solution_list.append(solution)
        score_list.append(solution.score())

    return solution_list, score_list

def make_list(max_trains):
    """ Creates a list with number zero through maximum specified trains.

    Args:
        max_trains: Maximum amount of trains that can be used in the solution.

    Returns:
        List filled with numbers 0 to max_trains times 2.
    """
    total_list = list(range(max_trains * 2))
    return total_list

def crossover(crossover_list, max_trains, solution1, solution2, station_dict):
    """ Randomly crosses two solutions with each other.

    Args:
        crossover_array: Array filled with integers zero through maximum amount of trains.
        max_trains: Maximum amount of trains allowed in solution.
        solution1: Part one of the next generation.
        soluiton2: Part two of the next generation.
        station_dict: Dictionary filled with every station.

    Returns:
        The new crossover solution.


    NIET ZES MAAR HELFT MAX tRAINSSSSS
    """

    index = 0
    choice_list = create_crossover_list(crossover_list, max_trains)
    crossover_solution_list = []

    # Select routes from both solutions.
    for i in choice_list:
        if i > max_trains - 1:
            # Select route from solution two.
            crossover_solution_list.append(solution2.route_list[i - max_trains])
        else:
            # Select route from solution one
            crossover_solution_list.append(solution1.route_list[i])


    crossover_solution = sn.Solution(crossover_solution_list, station_dict)

    return crossover_solution


def create_crossover_list(crossover_list, max_trains):
    """ Creates list stating which routes to pick from which solution.

    Args:
        crossover_list: List of zero through the maximum amount of trains.
        max_trains: Maximum amount of trains allowed in solution.

    Returns:
        A list filled with the chosen routes.

    """
    choice_list = []

    # Fill list with unique numbers.
    for i in range(max_trains):
        choice = rd.choice(crossover_list)
        while choice in choice_list:
            choice = rd.choice(crossover_list)
        choice_list.append(choice)

    return choice_list

def selection():
    raise NotImplementedError

def mutation():
    raise NotImplementedError


""" NOTES:

- How big should population be?
- Find good definiton of crossover.
- Swap in hillclimber is mutation
    - Chance of swap?
- Selection: keeping only the best solution might not always be the best idea.
    - Make chance of lesser solution coming through
- Pay attention to the fact that that the solutions are objects, and thus
    reside at the same adress: making another solution means that you overwrite
    the first one. Have yet to see tis but apparently it works ike that.
    This means I might have to work with deep copy and copy.
        Ddep copy copies all the objects within the object, copy only copies
        the most outer object, but leaves all the inner objects at the same
        location. Deep copy has a heavy load, so is a heavy operation.
"""


"""
Give the solutions with the highest score the highest chance of procreating.

Create whole new set of solutions based on the better solution
Normalise them?

"""
