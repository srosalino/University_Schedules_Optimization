# Import the necessary libraries and scripts
from charles import initialize_population
from selection_algorithms import fitness_proportionate_selection, ranking_selection, tournament_selection

from crossovers import (uniform_day_crossover_named, uniform_block_crossover_named, single_point_day_crossover_named,
                        single_point_block_crossover_named)

from mutations import block_swap_mutation, block_inversion_mutation, block_scramble_mutation

from optimization_problem import evolve_population
import numpy as np


def run_experiments(pop_size, num_practical_turns, subjects_per_practical_turn, days_per_week, blocks_per_day,
                    generations, pc, pm, trials):
    """
    Run a series of experiments with all possible combinations of selection algorithms, crossover operators,
    mutation operators, elitism settings, and fitness sharing settings using the predefined Genetic Algorithm to evolve
    a population.

    Parameters:
    - pop_size (int): Number of individuals in the population.
    - num_practical_turns (int): Number of Practical Turns per individual.
    - subjects_per_practical_turn (int): Number of subjects each Practical Turn is enrolled in.
    - days_per_week (int): Number of days in a week.
    - blocks_per_day (int): Number of blocks in each day.
    - generations (int): Number of generations to run the Genetic Algorithm.
    - pc (float): Crossover probability.
    - pm (float): Mutation probability.
    - trials (int): Number of trials to run the experiment.

    Returns:
    - dict: A dictionary containing the average best fitness values for each generation and each experiment combination.
    """

    results = []

    # Initialize the set of global optima to be empty
    global_optima_found = []

    # Initialize the variable containing the best individual's representation to None
    overall_best_individual = None

    # Initialize the overall best fitness found in the Genetic Algorithm to None
    overall_best_fitness = float('inf')

    # Initialize a counter of total experiments carried out
    total_experiments = 0

    # Define the selection algorithms, crossovers, and mutations
    selection_algorithms = [fitness_proportionate_selection, ranking_selection, tournament_selection]
    crossovers = [
        (uniform_day_crossover_named, "uniform_day_crossover"),
        (uniform_block_crossover_named, "uniform_block_crossover"),
        (single_point_day_crossover_named, "single_point_day_crossover"),
        (single_point_block_crossover_named, "single_point_block_crossover")
    ]
    mutations = [block_swap_mutation, block_inversion_mutation, block_scramble_mutation]
    mutation_names = ["block_swap_mutation", "block_inversion_mutation", "block_scramble_mutation"]

    # Iterate over all combinations
    for selection_algorithm in selection_algorithms:
        for crossover, crossover_name in crossovers:
            for mutation, mutation_name in zip(mutations, mutation_names):
                for elitism in [True]:
                    for use_fitness_sharing in [True, False]:
                        all_trials_best_fitnesses = []

                        for trial in range(trials):

                            # Increment the total experiments and print a progress message
                            total_experiments += 1
                            print(f'Experiment number {total_experiments} out of 1080')

                            print(f"Running trial {trial + 1} with {selection_algorithm.__name__}, "
                                  f"{crossover_name}, {mutation_name}, elitism={elitism}, "
                                  f"fitness_sharing={use_fitness_sharing}")

                            # Initialize population
                            initial_population = initialize_population(pop_size, num_practical_turns,
                                                                       subjects_per_practical_turn,
                                                                       days_per_week, blocks_per_day)

                            # Evolve the population with the given parameters
                            best_individual, best_fitness_per_generation = evolve_population(
                                initial_population,
                                selection_algorithm,
                                crossover,
                                pc,
                                mutation,
                                pm,
                                generations,
                                elitism,
                                use_fitness_sharing=use_fitness_sharing
                            )

                            all_trials_best_fitnesses.append(best_fitness_per_generation)

                            # Track the best overall individual
                            if best_fitness_per_generation[-1] < overall_best_fitness:
                                overall_best_fitness = best_fitness_per_generation[-1]
                                overall_best_individual = best_individual

                            # Append a found Global Optimum to the Global Optimum list
                            if best_fitness_per_generation[-1] == 0:
                                global_optima_found.append({
                                    "individual": best_individual,
                                    "selection_algorithm": selection_algorithm.__name__,
                                    "crossover": crossover_name,
                                    "mutation": mutation_name,
                                    "elitism": elitism,
                                    "fitness_sharing": use_fitness_sharing,
                                    "trial": trial + 1
                                })
                                print(f"Global optimum found during trial {trial + 1}. Ending trial early.")
                                break

                        # Pad all fitness sequences to the same length, if a trial ends earlier, due to the finding
                        # of a Global Optimum
                        max_length = max(len(seq) for seq in all_trials_best_fitnesses)
                        for seq in all_trials_best_fitnesses:
                            seq.extend([seq[-1]] * (max_length - len(seq)))

                        # Compute the average best fitness for each generation
                        average_best_fitnesses = np.mean(all_trials_best_fitnesses, axis=0)

                        # Store the results for this experiment configuration
                        results.append({
                            "selection_algorithm": selection_algorithm.__name__,
                            "crossover": crossover_name,
                            "mutation": mutation_name,
                            "elitism": elitism,
                            "fitness_sharing": use_fitness_sharing,
                            "average_best_fitnesses": average_best_fitnesses.tolist()
                        })

    # Save the results of the experiment to a text file
    with open("experiment_results.txt", "w") as file:
        for result in results:
            file.write(f"{result}\n")
        if overall_best_individual is not None:
            file.write(f"Overall Best Individual: {overall_best_individual}\n")
            file.write(f"Overall Best Fitness: {overall_best_fitness}\n")

    # Save the global optima found to a separate file
    with open("set_of_global_optima.txt", "w") as file:
        for optimum in global_optima_found:
            file.write(f"Individual: {optimum['individual']}\n"
                       f"Selection Algorithm: {optimum['selection_algorithm']}\n"
                       f"Crossover: {optimum['crossover']}\n"
                       f"Mutation: {optimum['mutation']}\n"
                       f"Elitism: {optimum['elitism']}\n"
                       f"Fitness Sharing: {optimum['fitness_sharing']}\n"
                       f"Trial: {optimum['trial']}\n"
                       f"-----------------------------------\n")

    return results


if __name__ == "__main__":
    results = run_experiments(pop_size=100, num_practical_turns=10, subjects_per_practical_turn=4, days_per_week=5,
                              blocks_per_day=8, generations=500, pc=0.9, pm=0.2, trials=30)

    # Print the results
    for result in results:
        print(result)
