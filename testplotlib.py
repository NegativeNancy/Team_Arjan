import numpy as np
import matplotlib as mlp
import matplotlib.pyplot as plt

def plot_data(file_name):
    """Plots the scores from the found solutions.

    Parameters:
    Takes one parameter, name of the fileself.

    Returns:
    Two line plots, one sorted, one not sorted. And one bar chart, sorted..
    """
    with open(file_name) as file:
        values = []
        x = []
        count = 0
        for line in file:
            values.append(float(line.strip('\n')))
            count += 1
            x.append(count)

    # Plot the sorted data
    plt.plot(sorted(values))
    plt.ylabel('score')
    plt.show()

    # Plot the completely random data
    plt.plot(values)
    plt.ylabel('score')
    plt.show()

    # dit werkt dus niet
    # new_x = [i for i in range(0, len(x), 500)]
    # new_y = []
    # for i in range(0, len(values), 500):
    #     new_val = 0
    #     for j in range(500):
    #         new_val += values[i]
    #     new_y.append(new_val)
    # print(new_y)
    # print(new_x)
    # plt.bar(new_x, sorted(new_y), color="rebeccapurple", align="center")
    # plt.ylabel('score')
    # plt.show()
