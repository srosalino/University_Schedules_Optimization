# Import the necessary libraries
import random


def initialize_population(pop_size, num_practical_turns, subjects_per_practical_turn, days_per_week, blocks_per_day):
    """
    Generates a population of schedules for a given number of individuals, where each individual
    consists of a possible weekly schedule for all the Practical Turns

    Parameters:
    - pop_size (int): Number of individuals (schedules) in the population.
    - num_practical_turns (int): Number of Practical Turns.
    - subjects_per_practical_turn (int): Number of unique subjects each Practical Turn can have.
    - days_per_week (int): Number of days per week that classes are scheduled.
    - blocks_per_day (int): Number of blocks (periods) in each day's schedule.

    Returns:
    - list: A list of individuals, where each individual is a list of Practical Turns, and each Practical Turn is a list
    of week days, with each day being a list of subjects (or 'Break') representing the schedule for that day for that
    Practical Turn.
    """

    # Initialize an empty list to store the Population
    population = []

    # Loop through the number of individuals to create
    for _ in range(pop_size):

        # Initialize an empty list to store the schedules for the current individual
        individual = []

        # Loop through the number of Practical Turns to create schedules for each turn
        for class_index in range(num_practical_turns):

            # Generate a list of subject names from 'Subject_1' to 'Subject_30'
            subjects = [f"Subject_{i + 1}" for i in range(31)]
            random.shuffle(subjects)  # Shuffle the list to randomize subject assignment

            # Slice the list to get the desired number of subjects for the current Practical Turn
            class_subjects = subjects[:subjects_per_practical_turn]

            # Generate a weekly schedule for each Practical Turn
            weekly_schedule = []

            for day in range(days_per_week):

                # Randomly decide how many Break blocks the current day will have
                num_break_blocks = random.randint(1, blocks_per_day)

                # The number of subjects blocks the current day will have is the blocks per day - number of break blocks
                num_subject_blocks = blocks_per_day - num_break_blocks

                # Randomly select which subjects the current Practical Turn will have using the count of subjects blocks
                # and selecting only from the subjects that the current Practical Turn is enrolled in
                day_schedule = random.choices(class_subjects, k=num_subject_blocks)

                # Fulfil the rest of the day with only Break blocks
                day_schedule.extend(['Break'] * num_break_blocks)

                random.shuffle(day_schedule)  # Shuffle to randomize the position of the 'Break' and subjects blocks

                weekly_schedule.append(day_schedule)  # Append the daily schedule to the weekly schedule of the current Practical Turn

            # Append the weekly schedule to the current individual's list of schedules
            individual.append(weekly_schedule)

        # Append the fully scheduled individual to the population list
        population.append(individual)

    return population


# Generate a population with 100 individuals, each with 10 Practical Turns, 4 subjects per Practical Turn,
# 5 days per week, and 8 blocks per day
population = initialize_population(100, 10, 4, 5,
                                   8)
