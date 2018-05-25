from classes import Stations as st
from classes import Route as rt
from classes import Solution as sn
from functions import helper
from algorithms import hillclimber as hc
import random as rd
import math

def simulated_annealing(solution, cool_function, max_temp, steps_routes = 0, steps_connections = 10000):
    """ Simulated annealing algorthm that tries to find the optimal set of routes,
    A.K.A. an optimal solution.

    Args:
        solution: An instance of the solution class.
        steps: The ammount of steps for the proces to do.
        max_temp: The maximum temp of the cooling function, as integer.
        cool_function: An integer representing the choice of cool function.

    Returns:
        The solution.
    """

    # Fill solution with empty routes if the route_list is empty.
    if solution.route_list == []:
        for i in range(solution.max_trains):
            route = rt.Route([])
            solution.route_list.append(route)

    score = solution.score()

    for step in range(steps_routes):
        route_index, new_route = hc.iteration_routes(solution)
        old_route, new_score, solution = propose_change(solution, route_index, new_route)
        if determine_accpetance(steps_routes, step, max_temp, \
            cool_function, score, new_score):
            score = new_score
        else:
            # Revert the change.
            solution.route_list[route_index] = old_route

    for step in range(steps_connections):
        # route_index, new_route = hc.iteration_routes(solution)
        route_index, new_route = hc.iteration_connections(solution)
        old_route, new_score, solution = propose_change(solution, route_index, new_route)
        if determine_accpetance(steps_connections, step, max_temp, \
            cool_function, score, new_score):
            score = new_score
        else:
            # Revert the change.
            solution.route_list[route_index] = old_route

    return solution


def propose_change(solution, route_index, new_route):
    """ Changes a route in the solution with a new route.

    Args:
        solution: An instance of the solution class.
        route_index: An integer, this determines which route to swap out.
        new_route: The route that will replace the old route.

    Returns:
        The old route, the new score, and new solution.
    """
    old_route = solution.route_list[route_index]
    solution.route_list[route_index]= new_route
    new_score = solution.score()

    return old_route, new_score, solution


def determine_accpetance(max_steps, step, max_temp, cool_function, old_score, new_score):
    """ Determines if a change is accepted, based on a cooling function.

    Args:
        max_steps: Integer expressing the maximum number of iterations.
        step: Integer which iteration the proces is in.
        max_temp: The maximum temperature of the algorithm.
        cool_function: Integer representing the choice of cool function.
        old_score: The score of the solution before the proposed change.
        new_score: The score of the solution after the proposed change.

    Returns:
        A boolean describing whether the change is accepted or not.
    """
    # Determine which cooling function to use.
    if cool_function == 0:
        temperature = lineair_cooling(max_temp, step, max_steps)
    elif cool_function == 1:
        temperature = sigmoid_cooling(max_temp, step, max_steps)
    elif cool_function == 2:
        temperature = sawteeth_cooling(max_temp, step, max_steps)
    else:
        temperature = logistic_cooling(max_temp, step, max_steps)

    # Return wheter the change is accepted or not.
    return probability_function(temperature, old_score, new_score)


def lineair_cooling(max_temp, step, max_steps):
    """ A cooling function based on a lineair function.

    Args:
        max_temp: An integer describing the maximum temperature of the cooling
            function.
        step: An integer representing how many iterations are done.
        max_steps: An integer representing how many iteration steps will be done.

    Returns:
        The temperature as a boolean.
    """
    # Linear scaling temperature, scaling down from max_temp to 0.
    temperature = max_temp - (step / max_steps) * max_temp

    return temperature

def sigmoid_cooling(max_temp, step, max_steps):
    """ A cooling function based on a Sigmoid function.

    Args:
        max_temp: An integer describing the maximum temperature of the cooling
            function.
        step: An integer describing how many iterations are done.
        max_steps: An integer describing how many iteration steps will be done.

    Returns:
        The temperature as boolean.
    """
    # A Sigmoid function.
    sigmoid_result = max_temp / (1 + math.exp((-12 / max_steps) * \
        (step - max_steps / 2)))

    # The temperature corresponding to the result of the Sigmoid function.
    temperature = max_temp - sigmoid_result

    return temperature

def logistic_cooling(max_temp, step, max_steps):
    """ A cooling function based on a logistic function.

    Args:
        max_temp: An integer describing the maximum temperature of the cooling
            function.
        step: An integer describing how many iterations are done.
        max_steps: An integer describing how many iteration steps will be done.

    Returns:
        The temperature as boolean.
    """
    # A logistic function.
    logistic_result = max_temp / (1 + math.exp(-6 * step / max_steps))
    # The temperature corresponding to the result of the logistic function.
    temperature = 2 * (max_temp -logistic_result)

    return temperature

def sawteeth_cooling(max_temp, step, max_steps):
    """ A cooling function based on a saw.

    Args:
        max_temp: An integer describing the maximum temperature of the cooling
            function.
        step: An integer describing how many iterations are done.
        max_steps: An integer describing how many iteration steps will be done.

    Returns:
        The temperature as boolean.
    """
    # Taking the moculo of two lineair functions, gives a sawtooth.
    temperature = (max_temp - 3 * max_temp * step / max_steps) \
        % (max_temp - max_temp * step / max_steps)

    return temperature


def probability_function(temperature, old_score, new_score):
    """ Determines wheter a change is accepted or not.

    Args:
        temperature: The temperature of the algorithm, as double.
        old_score: The old score, as double.
        new_score: The new score, as double.

    Results:
        Boolean representing whether the change is accepted or not.
    """
    # Prevent malfunctions when temperature can reach 0.
    if temperature != 0 and new_score < old_score:
        # compute the probability with which a change should be accepted.
        probability = math.exp((new_score - old_score) / temperature)
    else:
        if new_score < old_score:
            probability = 0
        else:
            probability = 1

    # Accept change.
    if rd.random() < probability:
        return True
    # Deny change.
    else:
        return False
