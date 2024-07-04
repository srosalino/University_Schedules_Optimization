# Import the necessary libraries
import random


def fitness_proportionate_selection(population, fitness_scores):
    """
    Selects an individual from the population based on fitness proportionate selection
    for this minimization problem.

    Parameters:
    - population (list): The population of individuals.
    - fitness_scores (list): The corresponding fitness scores for each individual.

    Returns:
    - Individual: A randomly selected individual based on fitness proportionality.
    """

    # Check for global optimum individual. If found, immediately return it
    for individual, fitness in zip(population, fitness_scores):
        if fitness == 0:
            return individual

    # Calculate the total fitness in the population
    total_fitness = sum(1.0 / f for f in fitness_scores)

    # Calculate the probability of selecting every individual, given that this is a minimization optimization problem
    selection_probs = [(1.0 / f) / total_fitness for f in fitness_scores]

    # Select the chosen individual
    return random.choices(population, weights=selection_probs, k=1)[0]


def ranking_selection(population, fitness_scores):
    """
    Selects an individual using ranking selection for this minimization problem.

    Parameters:
    - population (list): The population of individuals.
    - fitness_scores (list): The corresponding fitness scores for each individual.

    Returns:
    - Individual: A randomly selected individual based on ranking.
    """

    # Check for global optimum individual. If found, immediately return it
    for individual, fitness in zip(population, fitness_scores):
        if fitness == 0:
            return individual

    # Rank individuals by fitness, highest fitness first since this is a minimization optimization problem
    ranked_individuals = sorted(zip(population, fitness_scores), key=lambda x: x[1])

    # Assign selection probabilities based on the individual's rank
    rank_position = [len(population) - i for i in range(len(population))]

    # Sum all the ranking positions
    total_weight = sum(rank_position)

    # Calculate the probability of selecting every individual, given that this is a minimization optimization problem
    selection_probs = [weight / total_weight for weight in rank_position]
    selected_individuals = random.choices([individual for individual, score in ranked_individuals],
                                          weights=selection_probs, k=1)

    # Select the chosen individual
    return selected_individuals[0]


def tournament_selection(population, fitness_scores, tournament_size=3):
    """
    Selects an individual using tournament selection for this minimization problem.

    Parameters:
    - population (list): The population of individuals.
    - fitness_scores (list): The corresponding fitness scores for each individual.
    - tournament_size (int): The number of individuals in each tournament.

    Returns:
    - Individual: The best individual (with the lowest fitness) from the randomly selected tournament group.
    """
    # Randomly select the individuals that will be competing in the tournament (with repetition)
    tournament = random.choices(list(zip(population, fitness_scores)), k=tournament_size)

    # Select the individual with the lowest fitness (the best individual) within the tournament
    winner = min(tournament, key=lambda x: x[1])

    # Return the winner individual of the tournament
    return winner[0]
