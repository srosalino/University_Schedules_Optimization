# Import the necessary libraries
import random


def generate_subjects():
    """
    Generates a dictionary where each key represents a Practical Turn, and each value is a list of subjects assigned to
    that turn.

    The function creates a list of 30 unique subjects and then assigns a random subset of 4 subjects to each of the 10
    Practical Turns.

    Returns:
    - dict: A dictionary with keys as 'Class_i' where i is the Practical Turn number, and values are lists of 4 randomly
    chosen subjects.
    """

    # Create a list of generic subject names ranging from 'Subject_1' to 'Subject_30'
    all_subjects = [f"Subject_{j}" for j in range(1, 31)]

    # Initialize a dictionary to hold the subjects for each Practical Turn
    class_subjects = {}

    # Loop through a predefined number of Practical Turns (10 in this case)
    for i in range(1, 11):
        # Assign each Practical Turn a random set of 4 subjects from the list of all subjects
        # `random.sample` ensures that the selected subjects for each class are unique and no subject is repeated within
        # a class
        class_subjects[f"Class_{i}"] = random.sample(all_subjects, 4)

    # Return the dictionary containing the Practical Turns and their corresponding subjects
    return class_subjects


def save_to_file(class_subjects):
    """
    Saves the Practical Turn subjects data to a text file.

    Parameters:
    - class_subjects (dict): A dictionary where keys are class names and values are lists of subjects.

    This function writes each class and its subjects to a file named 'timetable_data.txt',
    with each class subjects listed on a new line.
    """
    with open('timetable_data.txt', 'w') as file:
        for class_name, subjects in class_subjects.items():
            # Format the line as 'ClassName: Subject1, Subject2, ...'
            line = f"{class_name}: {', '.join(subjects)}\n"
            file.write(line)  # Write the formatted line to the file


def main():
    """
    Main function to generate subjects for classes and save them to a file.

    This function serves as the entry point of the script, generating subjects for classes
    and then saving this data to a file using the save_to_file function.
    """
    class_subjects = generate_subjects()  # Generate a dictionary of class subjects
    save_to_file(class_subjects)          # Save the generated subjects to a file


# Call the main function to execute the script
if __name__ == "__main__":
    main()
