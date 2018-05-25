import matplotlib.pyplot as plt

def plot_data(file_name):
    """ Plots the scores from the found solutions, first sorted, then in the
    order they were found.

    Args:
        file_name: Datafile to plot from.
    """
    with open(file_name) as file:
        values = []
        x = []
        count = 0
        for line in file:
            values.append(float(line.strip('\n')))
            count += 1
            x.append(count)

    # Plot the sorted data.
    plt.plot(sorted(values))
    plt.ylabel('score')
    plt.show()

    # Plot the completely random data.
    plt.plot(values)
    plt.ylabel('score')
    plt.show()
