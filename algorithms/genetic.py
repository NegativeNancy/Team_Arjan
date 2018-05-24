from algorithms import random as ra
from algorithms import hillclimber as hc
from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
import random as rd

def genetic(solution):
    """ Algorithm that finds a genetic solution.

    Args:
        station_dict:
        max_trains: Maximum amount of trains allowed.
        max_minutes: Maximum amount of minutes the trains can run forself

    Returns:
        A genetically generated solution
    """
    score_list = []
    solution_list = []
    crossover_list = []

    crossover_list = make_list(solution.max_trains)
    population_size = 10

    # Make population.
    solution_list = make_population(population_size, solution)

    best_score = 0
    best_solution = sn.Solution([], solution.station_dict, solution.max_trains, solution.max_minutes, solution.station_dict_key_list)
    generation = 0
    while generation < 10:
        pop_size = 0

        crossover_solution_list = []
        crossover_score_list = []
        score_list, best, nextone = calc_fitness(solution_list)
        # Create next generation.
        #while pop_size < population_size:
        for _ in range(round(population_size / 2)):
            # Pick two parents.
            parents_index, parents = pick_next_population_parents(score_list, \
                population_size)
            for _ in range(rd.randint(1, 4)):
            #for j in range(2):
                crossover_solution = crossover(crossover_list, solution, \
                    solution_list[parents_index[0]], solution_list[parents_index[1]])
                crossover_solution_score = crossover_solution.score()
                crossover_solution_score, crossover_solution = \
                    mutation(crossover_solution_score, crossover_solution)

                crossover_solution_list.append(crossover_solution)
                crossover_score_list.append(crossover_solution_score)
                # Determine best score.
                if crossover_solution_score > best_score:
                    best_score = crossover_solution_score
                    best_solution = crossover_solution
                    print("best score", best_score, "generation", generation)

            parents_index = []
            parents = []

        solution_list = list(crossover_solution_list)
        score_list = list(crossover_score_list)
        generation += 1
        print(generation)

    # Find best crossover.
    print(best_solution.score())
    return best_solution

def calc_and_print_mean(score_list):
    summer = sum(score_list)
    print(round(summer / 500, 1))

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
        List of indices that the selected parents are at and the actual selected
        solutions themselves.
    """
    parent_indices = []
    parent_solutions = []
    # Select two solutions.
    for i in range(2):
        index, selected = select_score(score_list, population_size)
        parent_indices.append(index)
        parent_solutions.append(selected)

    return parent_indices, parent_solutions


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
    for score in score_list:
        new_sum_of_scores += score
        if new_sum_of_scores < chance:
            index += 1
        else:
            break

    return index, score_list[index]

def make_population(population_size, solution):
    """ Generate a population consisted of random solutions.

    Args:
        population_size: Integers specifying how big the population should be.

    Returns:
        A list of random solutions, size of the list is the previously specified
        population size.

    """
    solution_list = []

    # Create set amount of new solutions.
    for i in range(population_size):
        genetic_solution = ra.random(solution, False)
        solution_list.append(genetic_solution)
    return solution_list

def make_list(max_trains):
    """ Creates a list with number zero through maximum specified trains.

    Args:
        max_trains: Maximum amount of trains that can be used in the solution.

    Returns:
        List filled with numbers 0 to max_trains times 2.
    """
    return list(range(max_trains * 2))

def crossover(crossover_list, solution, solution1, solution2):
    """ Randomly crosses two solutions with each other.

    Args:
        crossover_array: Array filled with integers zero through maximum amount
        of trains.
        max_trains: Maximum amount of trains allowed in solution.
        solution1: Part one of the next generation.
        soluiton2: Part two of the next generation.
        station_dict: Dictionary filled with every station.

    Returns:
        The new crossover solution.
    """

    choice_list = create_crossover_list(crossover_list, solution.max_trains)
    crossover_solution_list = []
    time_list = []
    # Select routes from both solutions.
    for i in choice_list:
        if i > solution.max_trains - 1:
            # Select route from solution two.
            crossover_solution_list.append(solution2.route_list[i - solution.max_trains])
            time_list.append(solution2.route_list[i - solution.max_trains].time())
        else:
            # Select route from solution one
            crossover_solution_list.append(solution1.route_list[i])
            time_list.append(solution1.route_list[i].time())
    #print(crossover_solution_list)
    # too_much = 0
    # print(sum(time_list))
    # if sum(time_list) > 3600:
    #     print(sum(time_list))
    #     too_much += 1
    # if too_much > 0:
    #     print("too much", too_much)

    crossover_solution = sn.Solution(crossover_solution_list, \
    solution.station_dict, solution.max_trains, solution.max_minutes,
    solution.station_dict_key_list)

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

def mutation(old_score, solution):
    # for _ in range(50):
    #     old_score = hc.iteration_routes(old_score, solution)
    # return old_score, solution
    print("one")
    return hc.iteration_routes(old_score, solution), solution
