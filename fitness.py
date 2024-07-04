# Import the necessary scripts
from charles import population


def fitness_individual(individual):
    """
  Calculates the fitness score of an Individual by assessing penalties based on the specified criteria.

  Parameters:
  - individual (list): A list representing the schedule of an individual, which includes multiple Practical Turns,
    each containing a weekly schedule.

  Returns:
  - int: The total penalty points for the individual, where a lower penalty indicates a better fitness.
  """

    penalties = 0               # Initialize the penalties to 0
    MIN_BLOCKS_PER_SUBJECT = 8  # Minimum number of blocks each subject must have in a week
    NUM_DAYS = 5                # Total number of days in the weekly schedule
    MIDDLE_BLOCKS = {3, 4}      # Preferred positions for 'break' blocks (0-based indexing)

    # Initialize subject counts for each Practical Turn and overlap tracking for each day
    subject_week_counts = [{} for _ in range(len(individual))]  # Track subject counts per Practical Turn
    overlaps = [set() for _ in range(NUM_DAYS)]  # Tracks overlaps by day and block across all Practical Turns

    # Evaluate each Practical Turn in the individual's schedule
    for class_idx, practical_turn in enumerate(individual):

        for day_idx, day in enumerate(practical_turn):
            day_subjects = {}
            break_found = False  # Indicator to check if 'Break' is found in the day

            # Assess each block in the day's schedule
            for block_idx, subject in enumerate(day):
                if subject != 'Break':
                    # Count blocks per subject for minimum block requirements
                    if subject not in day_subjects:
                        day_subjects[subject] = 0
                    day_subjects[subject] += 1

                    # Check for subject overlap in the same day and block across all Practical Turns
                    if (day_idx, block_idx, subject) in overlaps[day_idx]:
                        penalties += 3  # Add a penalty of 3 for each overlap
                    else:
                        overlaps[day_idx].add((day_idx, block_idx, subject))
                else:
                    break_found = True
                    # Add penalty if 'break' is found outside the preferred middle blocks
                    if block_idx not in MIDDLE_BLOCKS:
                        penalties += 2  # Add a penalty of 2 for 'break' outside middle blocks

            # Penalty if no 'Break' was found in the day
            if not break_found:
                penalties += 4  # Add a penalty of 4 for no 'Break' in the day

            # Add the day's subject counts to the weekly totals for this class
            for subject, count in day_subjects.items():
                if subject not in subject_week_counts[class_idx]:
                    subject_week_counts[class_idx][subject] = 0
                subject_week_counts[class_idx][subject] += count

    # Check if each subject has the minimum required blocks per week and penalize shortfalls
    for weekly_counts in subject_week_counts:
        for subject, total_count in weekly_counts.items():
            if total_count < MIN_BLOCKS_PER_SUBJECT:
                # Add a penalty of 5 times each shortfall
                # Use max to prevent penalty from turning into reward if exists more than 8 blocks per week of the same subject
                penalties += max(0,(MIN_BLOCKS_PER_SUBJECT - total_count) * 5)  # Multiply shortfall by penalty weight

    # Return the total penalties as the fitness score (lower is better)
    return penalties


def evaluate_population(population):
    """
  Evaluates the fitness of an entire population of individuals

  Parameters:
  - population (list): A list of individuals, each an individual schedule to be evaluated.

  Returns:
  - list: A list of fitness scores for each individual in the population.
  """
    fitness_scores = []

    for individual in population:

        # Calculate fitness for each individual and append to results
        score = fitness_individual(individual)
        fitness_scores.append(score)

    return fitness_scores


def hamming_distance_between_individuals(individual1, individual2):
    """
    Calculate the distance between two individuals (weekly schedules for all Practical Turns).
    The distance is the count of differing blocks between the two individuals.

    Parameters:
    - individual1 (list): The first individual (schedule) to compare.
    - individual2 (list): The second individual (schedule) to compare.

    Returns:
    - int: The total distance (number of differing blocks) between the two individuals.
    """

    total_distance = 0  # Initialize the total distance to zero

    # Iterate over all Practical Turns in the individuals
    for class_index in range(len(individual1)):
        turn_distance = 0  # Initialize the Practical Turn distance to zero

        # Iterate over all days in the Practical Turn
        for day_index in range(len(individual1[class_index])):
            day_distance = 0  # Initialize day distance to zero

            # Iterate over all blocks in the day
            for block_index in range(len(individual1[class_index][day_index])):

                # Increment day distance if blocks differ
                if individual1[class_index][day_index][block_index] != individual2[class_index][day_index][block_index]:
                    day_distance += 1

            # Add day distance to Practical Turn distance
            turn_distance += day_distance

        # Add Practical Turn distance to the total distance
        total_distance += turn_distance

    return total_distance


def get_length(individual):
    """
    Calculate the total length of an individual.
    The length is the total number of blocks across all Practical Turns and days.

    Parameters:
    - individual (list): The individual (schedule) to measure.

    Returns:
    - int: The total number of blocks in the individual's schedule.
    """

    total = 0  # Initialize the total length to zero

    # Iterate over all Practical Turns in the individual
    for turn in individual:

        # Iterate over all days in the Practical Turn
        for day in turn:

            if isinstance(day, list):
                # If the day is a list, add its length to the total
                total += len(day)

            else:
                # If the day is not a list, increment the total by 1
                total += 1

    return total


def hamming_distance_among_population(population):
    """
    Calculate the Hamming distance between each pair of individuals in the population.

    The Hamming distance between two individuals is defined as the number of differing blocks
    at corresponding positions in their schedules.

    Parameters:
    - population (list): A list of individuals where each individual represents a weekly schedule.

    Returns:
    - hamming_distance (list of lists): A matrix containing the Hamming distances between each pair of individuals.
                                         Each element hamming_distance[i][j] represents the Hamming distance
                                         between individual i and individual j.
    """

    hamming_distance = []  # Initialize the matrix to store the Hamming distances

    # Iterate over each individual in the population
    for individual_1 in population:

        dist_individuals = []  # Initialize the list to store distances for the current individual

        # Iterate over each individual in the population again to compute pairwise distances
        for individual_2 in population:

            # Compute the Hamming distance between individual_1 and individual_2
            dist_individuals.append(hamming_distance_between_individuals(individual_1, individual_2))

        # Append the distances for the current individual to the Hamming distance matrix
        hamming_distance.append(dist_individuals)

    return hamming_distance


def invert_normalized_distance(distance):
    """
    Inversely normalize the distances in the given distance matrix, which consists of all distances among all
    individuals in the population
    The normalization is done by calculating 1 - (distance / length of individuals).

    Parameters:
    - distance (list of lists): The distance matrix to be inversely normalized.
                            Each element distance[i][j] represents the distance between individual i and individual j.

    Returns:
    - invert_normalized_distance (list of lists): The inversely normalized distance matrix.
                                           Each element is calculated as 1 - (distance[i][j] / length of individual).
    """

    invert_normalized_distance = []  # Initialize the inversely normalized distance matrix

    # Iterate over each row in the distance matrix
    for i in range(len(distance)):

        distance_ = []  # Initialize the inversely normalized row

        # Iterate over each distance in the row
        for j in range(len(distance[i])):

            # Calculate the inversely normalized distance
            distance_.append(1 - (distance[i][j] / get_length(population[0])))

        # Append the inversely normalized row to the result matrix
        invert_normalized_distance.append(distance_)

    return invert_normalized_distance


def fitness_sharing(population):
    """
    Apply fitness sharing to a population to adjust the fitness of individuals based on their similarity.
    In this minimization problem, rare individuals will have their fitness values improved (decreased),
    while similar individuals will have their fitness values worsened (increased), promoting diversity.

    Parameters:
    - population (list): A list of individuals where each individual represents a weekly schedule.

    Returns:
    - new_scores (list): A list of adjusted fitness scores for the population after applying fitness sharing.
    """

    # Evaluate the fitness of the population
    fitness_scores = evaluate_population(population)

    # Calculate the Hamming distances between each pair of individuals in the population
    hamming_distances = hamming_distance_among_population(population)

    # Invert and normalize the Hamming distances
    invert_normalized_distances = invert_normalized_distance(hamming_distances)

    # Calculate the sum of the inverted normalized distances for each individual
    sums = []
    for li in invert_normalized_distances:
        sums.append(sum(li))

    # Adjust the fitness scores based on the similarity sums
    # For this minimization problem, reduce fitness for rare individuals and increase for similar ones
    new_fitness_values = []
    for i in range(len(sums)):
        if sums[i] != 0:
            new_fitness_values.append(fitness_scores[i] * sums[i])
        else:
            new_fitness_values.append(fitness_scores[i])

    return new_fitness_values
