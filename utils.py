# Import the necessary libraries
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import sem, t


def load_experiment_results(file_path):
    """
    Load experiment results from a file.

    Parameters:
    - file_path (str): The path to the file containing the experiment results.

    Returns:
    - list: A list of dictionaries containing the experiment results.
    """
    results = []
    try:
        with open(file_path, 'r') as file:
            for line in file.readlines():
                try:
                    # eval to convert the string representation of a dictionary back to a dictionary
                    result = eval(line.strip())
                    results.append(result)
                except SyntaxError as e:
                    print(f"Error parsing line: {line}. Error: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return results


def aggregate_results(results, key):
    """
    Aggregate the results based on a specified key.

    Parameters:
    - results (list): A list of dictionaries containing the experiment results.
    - key (str): The key to aggregate the results by Selection Algorithm, Crossover and Mutation

    Returns:
    - dict: A dictionary containing the aggregated results.
    """
    aggregated_data = {}

    for result in results:
        value = result[key]
        average_best_fitnesses = result['average_best_fitnesses']

        if value not in aggregated_data:
            aggregated_data[value] = []
        aggregated_data[value].append(average_best_fitnesses)

    # Calculate the mean and 95% confidence interval for each generation across all trials for each key value
    for value, fitness_lists in aggregated_data.items():
        mean = np.mean(fitness_lists, axis=0)
        se = sem(fitness_lists, axis=0)
        h = se * t.ppf((1 + 0.95) / 2., len(fitness_lists) - 1)
        aggregated_data[value] = {
            'mean': mean,
            'conf_interval': h
        }

    return aggregated_data


def plot_aggregated_data(aggregated_data, title, ylabel, xlabel='Generation', save_path=None):
    """
    Plot the aggregated data with 95% confidence intervals.

    Parameters:
    - aggregated_data (dict): A dictionary containing the aggregated data.
    - title (str): The title of the plot.
    - ylabel (str): The label for the y-axis.
    - xlabel (str): The label for the x-axis.
    - save_path (str): The path to save the plot. If None, the plot will be displayed.
    """
    plt.figure(figsize=(10, 6))

    for label, data in aggregated_data.items():
        mean = data['mean']
        conf_interval = data['conf_interval']
        generations = np.arange(len(mean))
        plt.plot(generations, mean, label=label)
        plt.fill_between(generations, mean - conf_interval, mean + conf_interval, alpha=0.2)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim(0, 1001)  # Set the y-axis range from 0 to 1000, to ensure a fair and non-deceptive plot comparison
    plt.yticks(np.arange(0, 1001, 100))  # Set y-ticks with a step of 100 for all plots, to ensure a fair comparison
    plt.xticks(np.arange(0, 501, 50))  # Set x-ticks with a step of 50 for all plots, to ensure a fair comparison
    plt.legend()
    plt.grid(False)

    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()


def main():

    # Load experiment results
    results = load_experiment_results('experiment_results.txt')

    if not results:
        print("No results to plot.")
        return

    # Aggregate results by selection algorithm
    selection_data = aggregate_results(results, 'selection_algorithm')
    plot_aggregated_data(selection_data, 'Average Best Fitness by Selection Algorithm, Across All Trials', 'Average Best Fitness', save_path='selection_algorithms_plot.png')

    # Aggregate results by crossover
    crossover_data = aggregate_results(results, 'crossover')
    plot_aggregated_data(crossover_data, 'Average Best Fitness by Crossover Operator, Across All Trials', 'Average Best Fitness', save_path='crossovers_plot.png')

    # Aggregate results by mutation
    mutation_data = aggregate_results(results, 'mutation')
    plot_aggregated_data(mutation_data, 'Average Best Fitness by Mutation Operator, Across All Trials', 'Average Best Fitness', save_path='mutations_plot.png')

    # Aggregate results by fitness sharing
    fitness_sharing_data = {'With Fitness Sharing': [], 'Without Fitness Sharing': []}
    for result in results:
        if result['fitness_sharing']:
            fitness_sharing_data['With Fitness Sharing'].append(result['average_best_fitnesses'])
        else:
            fitness_sharing_data['Without Fitness Sharing'].append(result['average_best_fitnesses'])

    for key, fitness_lists in fitness_sharing_data.items():
        mean = np.mean(fitness_lists, axis=0)
        se = sem(fitness_lists, axis=0)
        h = se * t.ppf((1 + 0.95) / 2., len(fitness_lists) - 1)
        fitness_sharing_data[key] = {
            'mean': mean,
            'conf_interval': h
        }

    plot_aggregated_data(fitness_sharing_data, 'Average Best Fitness with and without Fitness Sharing, Across All Trials', 'Average Best Fitness', save_path='fitness_sharing_plot.png')


if __name__ == "__main__":
    main()
