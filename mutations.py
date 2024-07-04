# Import the necessary libraries
from random import sample


def block_swap_mutation(individual):
    """
    Perform block swap mutation on an individual.
    This mutation operator selects two random blocks within each day for each Practical Turn and swaps them.

    Parameters:
    - individual (list): The individual to be mutated.

    Returns:
    - individual (list): The mutated individual.
    """

    # Iterates over all Practical Turns
    for turn_index in range(len(individual)):

        # Iterates over all days
        for day_index in range(len(individual[0])):

            # Chooses randomly 2 blocks from the total number of blocks
            block_indexes = sample(range(0, len(individual[0][0])), 2)

            # Swaps the two selected blocks in the day's schedule
            individual[turn_index][day_index][block_indexes[0]], individual[turn_index][day_index][block_indexes[1]] = (
              individual[turn_index][day_index][block_indexes[1]], individual[turn_index][day_index][block_indexes[0]])

    return individual


def block_inversion_mutation(individual):
    """
    Perform block inversion mutation on an individual.
    This mutation operator selects a random range of blocks within each day of each Practical Turn and inverts the order
    of those blocks.

    Parameters:
    - individual (list): The individual to be mutated.

    Returns:
    - individual (list): The mutated individual.
    """

    # Iterates over all Practical Turns
    for class_index in range(len(individual)):

        # Iterates over all days
        for day_index in range(len(individual[0])):

            # Chooses randomly 2 blocks from the total number of blocks and ensures they are not consecutive
            block_indexes = sample(range(0, len(individual[0][0])), 2)
            while abs(block_indexes[0] - block_indexes[1]) == 1:
                block_indexes = sample(range(0, len(individual[0][0])), 2)
            block_indexes.sort()

            # Inverts the order of the blocks within the selected range
            individual[class_index][day_index][block_indexes[0]:block_indexes[1]] = (
                individual[class_index][day_index][block_indexes[0]:block_indexes[1]][::-1])

    return individual


def block_scramble_mutation(individual):
    """
    Applies block scramble mutation to an individual. This mutation randomly scrambles the order of blocks
    within each day for all Practical Turns.

    Parameters:
    - individual (list): The individual to be mutated.

    Returns:
    - list: The mutated individual.
    """

    # Iterates over all Practical Turns
    for turn_index in range(len(individual)):

        # Iterates over all days within the current Practical Turn
        for day_index in range(len(individual[0])):

            # Gets the blocks for the current day
            blocks = individual[turn_index][day_index]

            # Scrambles the order of the blocks
            scrambled_blocks = sample(blocks, len(blocks))

            # Replaces the original blocks with the scrambled blocks
            individual[turn_index][day_index] = scrambled_blocks

    return individual
