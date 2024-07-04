# Import the necessary libraries
from random import random, randint


def uniform_day_crossover(parent1, parent2):
    """
    Perform uniform crossover on two parent individuals at the day level.
    Each day's schedule is swapped between parents with a 50% probability.

    Parameters:
    - parent1 (list): The first parent individual.
    - parent2 (list): The second parent individual.

    Returns:
    - offspring1 (list): The first offspring generated from the parents.
    - offspring2 (list): The second offspring generated from the parents.
    """

    # Initialize empty lists to store the offspring
    offspring1 = []
    offspring2 = []

    # Ensure both parents have the same number of Practical Turns
    if len(parent1) == len(parent2):

        for turn_ in range(len(parent1)):

            # Ensure both parents have the same number of days for the current Practical Turn
            if len(parent1[turn_]) == len(parent2[turn_]):

                # Initialize empty lists to store the daily schedules for each Practical Turn in the offspring
                class_schedule1 = []
                class_schedule2 = []

                for day in range(len(parent1[turn_])):

                    # With a 50% probability, swap the daily schedules between parents
                    if random() < 0.5:
                        class_schedule1.append(parent1[turn_][day][:])
                        class_schedule2.append(parent2[turn_][day][:])
                    else:
                        class_schedule1.append(parent2[turn_][day][:])
                        class_schedule2.append(parent1[turn_][day][:])

                # Add the Practical Turn schedules to the offspring
                offspring1.append(class_schedule1)
                offspring2.append(class_schedule2)

            else:
                print("Parents must have the same number of days for each Practical Turn")

    else:
        print("Parents must have the same number of Practical Turns")

    return offspring1, offspring2


def uniform_block_crossover(parent1, parent2):
    """
    Perform uniform crossover on two parent individuals at the block level.
    Each block within a day is swapped between parents with a 50% probability.

    Parameters:
    - parent1 (list): The first parent individual.
    - parent2 (list): The second parent individual.

    Returns:
    - offspring1 (list): The first offspring generated from the parents.
    - offspring2 (list): The second offspring generated from the parents.
    """

    # Initialize empty lists to store the offspring
    offspring1 = []
    offspring2 = []

    # Ensure both parents have the same number of Practical Turns
    if len(parent1) == len(parent2):

        for turn_idx in range(len(parent1)):

            # Ensure both parents have the same number of days for the current Practical Turn
            if len(parent1[turn_idx]) == len(parent2[turn_idx]):

                # Initialize empty lists to store the daily schedules for each Practical Turn in the offspring
                class_schedule1 = []
                class_schedule2 = []

                for day_idx in range(len(parent1[turn_idx])):

                    # Ensure both parents have the same number of blocks for the current day
                    if len(parent1[turn_idx][day_idx]) == len(parent2[turn_idx][day_idx]):

                        # Initialize empty lists to store the block schedules for each day in the offspring
                        day_schedule1 = []
                        day_schedule2 = []

                        for block_idx in range(len(parent1[turn_idx][day_idx])):

                            # With a 50% probability, swap the blocks between parents
                            if random() < 0.5:
                                day_schedule1.append(parent1[turn_idx][day_idx][block_idx][:])
                                day_schedule2.append(parent2[turn_idx][day_idx][block_idx][:])
                            else:
                                day_schedule1.append(parent2[turn_idx][day_idx][block_idx][:])
                                day_schedule2.append(parent1[turn_idx][day_idx][block_idx][:])

                        # Add the day schedules to the class schedules
                        class_schedule1.append(day_schedule1)
                        class_schedule2.append(day_schedule2)

                    else:
                        print(f"Parents must have the same number of blocks for each day in each Practical Turn")

                # Add the class schedules to the offspring
                offspring1.append(class_schedule1)
                offspring2.append(class_schedule2)

            else:
                print("Parents must have the same number of days for each Practical Turn")

    else:
        print("Parents must have the same number of Practical Turns")

    return offspring1, offspring2


def single_point_day_crossover(parent1, parent2):
    """
    Perform single-point crossover on two parent individuals at the day level.
    A random crossover point is selected, and the days are swapped between parents at that point.

    Parameters:
    - parent1 (list): The first parent individual.
    - parent2 (list): The second parent individual.

    Returns:
    - offspring1 (list): The first offspring generated from the parents.
    - offspring2 (list): The second offspring generated from the parents.
    """

    # Initialize empty lists to store the offspring
    offspring1 = []
    offspring2 = []

    # Iterate over each Practical Turn
    for turn_index in range(len(parent1)):

        # Select a random crossover point for the current Practical Turn
        xo_point = randint(1, len(parent1[turn_index]) - 1)

        # Initialize empty lists to store the daily schedules for each Practical Turn in the offspring
        class_schedule1 = []
        class_schedule2 = []

        # Before the crossover point, copy days from parent1 to offspring1 and from parent2 to offspring2
        for day_index in range(xo_point):
            class_schedule1.append(parent1[turn_index][day_index][:])
            class_schedule2.append(parent2[turn_index][day_index][:])

        # After the crossover point, copy days from parent2 to offspring1 and from parent1 to offspring2
        for day_index in range(xo_point, len(parent1[turn_index])):
            class_schedule1.append(parent2[turn_index][day_index][:])
            class_schedule2.append(parent1[turn_index][day_index][:])

        # Add the class schedules to the offspring
        offspring1.append(class_schedule1)
        offspring2.append(class_schedule2)

    return offspring1, offspring2


def single_point_block_crossover(parent1, parent2):
    """
    Perform single-point crossover on two parent individuals at the block level.
    A random crossover point is selected for each day, and the blocks are swapped between parents at that point.

    Parameters:
    - parent1 (list): The first parent individual.
    - parent2 (list): The second parent individual.

    Returns:
    - offspring1 (list): The first offspring generated from the parents.
    - offspring2 (list): The second offspring generated from the parents.
    """

    # Initialize empty lists to store the offspring
    offspring1 = []
    offspring2 = []

    # Iterate over each Practical Turn
    for turn_index in range(len(parent1)):

        # Initialize empty lists to store the daily schedules for each Practical Turn in the offspring
        class_schedule1 = []
        class_schedule2 = []

        # Iterate over each day
        for day_index in range(len(parent1[turn_index])):

            # Select a random crossover point for the current day
            xo_point = randint(1, len(parent1[turn_index][day_index]) - 1)

            # Initialize empty lists to store the block schedules for each day in the offspring
            day_schedule1 = []
            day_schedule2 = []

            # Iterate over each block
            for block_index in range(len(parent1[turn_index][day_index])):

                # Before the crossover point, copy blocks from parent1 to offspring1 and from parent2 to offspring2
                if block_index < xo_point:
                    day_schedule1.append(parent1[turn_index][day_index][block_index])
                    day_schedule2.append(parent2[turn_index][day_index][block_index])
                # After the crossover point, copy blocks from parent2 to offspring1 and from parent1 to offspring2
                else:
                    day_schedule1.append(parent2[turn_index][day_index][block_index])
                    day_schedule2.append(parent1[turn_index][day_index][block_index])

            # Add the day schedules to the Practical Turn schedules
            class_schedule1.append(day_schedule1)
            class_schedule2.append(day_schedule2)

        # Add the Practical Turn schedules to the offspring
        offspring1.append(class_schedule1)
        offspring2.append(class_schedule2)

    return offspring1, offspring2


def uniform_day_crossover_named(parent1, parent2):
    return uniform_day_crossover(parent1, parent2)


def uniform_block_crossover_named(parent1, parent2):
    return uniform_block_crossover(parent1, parent2)


def single_point_day_crossover_named(parent1, parent2):
    return single_point_day_crossover(parent1, parent2)


def single_point_block_crossover_named(parent1, parent2):
    return single_point_block_crossover(parent1, parent2)
