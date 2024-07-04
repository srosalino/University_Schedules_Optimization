# Import the necessary libraries and scripts
import random
from fitness import evaluate_population, fitness_sharing as apply_fitness_sharing


def evolve_population(population, selection_algorithm, crossover, pc, mutation, pm, generations,
                      elitism=True, use_fitness_sharing=False):
    """
    Using Genetic Algorithms and given a population, a selection algorithm, a crossover (and its probability of
    happening), a mutation (and its probability of happening) and using elitism consisting of only 1 individual, evolve
    the population and return the best individual. In other words, return the best weekly schedule for all Practical
    Turns.

    Parameters:
    - population (list): The population of individuals.
    - selection_algorithm (function): The selection algorithm to be used in the Genetic Algorithm.
    - crossover (function): The crossover operator to be used in the Genetic Algorithm.
    - pc (float): Crossover rate
    - mutation (function): The mutation operator to be used in the Genetic Algorithm.
    - pm (float): Mutation rate
    - generations (int): The number of generations to run the Genetic Algorithm
    - elitism (bool): A boolean True/False indicating whether to apply elitism in the Genetic Algorithm
    - use_fitness_sharing (bool): A boolean True/False indicating whether to apply fitness sharing in the GA

    Returns:
    - best_individual (list): The best individual found.
    - best_fitness_per_generation (list): Best fitness values for each generation.
    """

    best_individual = None
    best_fitness = float('inf')  # Since this is a minimization optimization problem
    best_fitness_per_generation = []

    for generation in range(generations):
        new_population = []

        # Evaluate the fitness of the current population
        fitness_scores = evaluate_population(population)

        # Apply fitness sharing if enabled
        if use_fitness_sharing:
            fitness_scores = apply_fitness_sharing(population)

        # Apply elitism by keeping the best individual
        if elitism:
            best_index = fitness_scores.index(min(fitness_scores))
            best_individual = population[best_index]
            best_fitness = fitness_scores[best_index]
            new_population.append(best_individual)

        while len(new_population) < len(population):
            # Selection
            parent1 = selection_algorithm(population, fitness_scores)
            if parent1 in population and fitness_scores[population.index(parent1)] == 0:
                # If a Global Optimum was selected, immediately return it
                return parent1, best_fitness_per_generation

            parent2 = selection_algorithm(population, fitness_scores)
            if parent2 in population and fitness_scores[population.index(parent2)] == 0:
                # If a Global Optimum was selected, immediately return it
                return parent2, best_fitness_per_generation

            # Crossover
            if random.random() < pc:  # Crossover probability
                offspring1, offspring2 = crossover(parent1, parent2)
            else:
                # If crossover does not happen, perform the replication of the parents into the offspring
                offspring1, offspring2 = parent1, parent2

            # Mutation
            if random.random() < pm:  # Mutation probability for offspring1
                offspring1 = mutation(offspring1)
            if random.random() < pm:  # Mutation probability for offspring2
                offspring2 = mutation(offspring2)

            new_population.extend([offspring1, offspring2])

        # Ensure new population size matches the original population size
        population = new_population[:len(population)]

        # Find the best individual in the current population
        fitness_scores = evaluate_population(population)
        current_best_index = fitness_scores.index(min(fitness_scores))
        current_best_fitness = fitness_scores[current_best_index]

        if current_best_fitness < best_fitness:
            best_individual = population[current_best_index]
            best_fitness = current_best_fitness

        best_fitness_per_generation.append(best_fitness)

        # Print progress
        print(f"Generation {generation + 1}: Best Fitness = {current_best_fitness}")

    return best_individual, best_fitness_per_generation
