import os

# File paths linked to global variables
COMPETITORS_FILE = "competitors.txt"
EVENTS_FILE = "events.txt"
RESULTS_FILE = "results.txt"

def initialize_files():
    # Ensure all required files exist and creates an empty file if there are any missing files
    for file in [COMPETITORS_FILE, EVENTS_FILE, RESULTS_FILE]:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                pass


def validate_positive_int(prompt, upper_limit=None):
    # Ensures the user provides a positive numeric input and will loop until the user provides a valid input
    while True:
        try:
            value = int(input(prompt))
            if value < 0 or (upper_limit and value > upper_limit): # If the value is negative
                raise ValueError # Manually sends value error if input is invalid
            return value
        except ValueError:
            print("Invalid input. Please enter a valid positive number.")

def read_file(file_name):
    # Reads the data from the file and returns a list of line and the 'r' opens the file in read mode
    with open(file_name, 'r') as file:
        return [line.strip() for line in file]


def write_file(file_name, lines):
    # Write a list of lines to a file, included 'w' as it overwrites the file
    with open(file_name, 'w') as file:
        file.write("\n".join(lines))


def generate_id(file_name, start):
    # Generates a new unique ID and determines the highest existing ID and goes up in increments of 1
    lines = read_file(file_name)
    if lines:
        # Filter out any empty lines or lines with invalid data
        valid_lines = [line for line in lines if line.strip() != '']

        if valid_lines:
            # Get the last valid line and extract the ID from it
            last_id = int(valid_lines[-1].split(',')[0].strip())  # Strip any extra spaces before conversion
            return last_id + 1  # Return next ID by adding 1 to the last ID
    return start  # Return the start ID if no valid lines are found

# Menu functions
def register_competitor():
    #Menu to register a competitor
    name = input("Enter competitor's name: ").strip()
    gender = input("Enter gender (Male/Female): ").strip()
    age = input("Enter age: ").strip()

    #Validation ensuring valid inputs with corresponding error message
    if gender not in ['Male', 'Female']:
        print("Invalid gender. Please enter Male or Female.")
        return

    #Validation ensuring the input is a positive number
    if not age.isdigit() or int(age) <= 0:
        print("Invalid age. Please enter a positive number.")
        return

    #Writes the users inputs into the designated file
    competitor_id = generate_id(COMPETITORS_FILE, 1)
    with open(COMPETITORS_FILE, 'a') as file:
        file.write(f"{competitor_id},{name},{gender},{age}\n") # Formatting for the data entered into the files
    print(f"Competitor {name} registered successfully with ID {competitor_id}.")


def register_event():
    # Register a new event and write it to the file
    event_name = input("Enter event name: ").strip()
    event_id = generate_id(EVENTS_FILE, 100)
    with open(EVENTS_FILE, 'a') as file:
        file.write(f"{event_id},{event_name}\n")
    print(f"Event '{event_name}' registered successfully with ID {event_id}.")


def record_times():
    #Record times for a competitor in an event
    initialize_files()
    competitor_id = input("Enter competitor ID: ").strip()
    event_id = input("Enter event ID: ").strip().upper()

    #Validation ensuring that the users input is numeric
    if not competitor_id.isdigit() or not event_id.isdigit():
        print("IDs must be numeric.")
        return

    #Validation ensuring that no duplicate records are written to the file
    competitor_exists = any(line.startswith(competitor_id) for line in read_file(COMPETITORS_FILE))
    event_exists = any(line.startswith(event_id) for line in read_file(EVENTS_FILE))

    #Validation ensuring that the competitor/event exists within the files
    if not competitor_exists:
        print(f"No competitor found with ID {competitor_id}.")
        return
    if not event_exists:
        print(f"No event found with ID {event_id}.")
        return

    #User inputs
    swim_time = int(input("Enter swim time (minutes): "))
    cycle_time = int(input("Enter cycle time (minutes): "))
    run_time = int(input("Enter run time (minutes): "))

    #Validation ensuring that any user inputs arent negative
    if any(t < 0 for t in [swim_time, cycle_time, run_time]):
        print("Times must be non-negative.")
        return

    #Variables calculating the total time and formatting them into the result_entry variable
    total_time = swim_time + cycle_time + run_time
    result_entry = f"{competitor_id},{event_id},{swim_time},{cycle_time},{run_time},{total_time}"

    #Opens the results file and writes the result_entry variable
    with open(RESULTS_FILE, 'a') as file:
        file.write(result_entry + "\n")
    print("Times recorded successfully.")


def generate_reports():
    while True:
        # Display menu
        print("\n1. Competitors Registered")
        print("2. Events Registered")
        print("3. Event Results")
        print("4. Exit")

        option = validate_positive_int("Enter your choice: ")

        if option == 1:
            # Prompt the user to enter the event ID
            event_id = input("Enter the Event ID to view registered competitors: ").strip()

            # Read the results to find competitors registered for the given event
            results = read_file(RESULTS_FILE)

            # Collect competitor IDs for the specified event_id from results.txt
            competitor_ids = set()
            for line in results:
                fields = line.split(",")
                if len(fields) >= 2 and fields[
                    1].strip() == event_id:  # Check if the line is valid and matches the event_id
                    competitor_ids.add(fields[0])  # Add competitor_id to the set

            if not competitor_ids:
                print(f"No competitors registered for event ID {event_id}.")
            else:
                # Read competitors file to get competitor details
                competitors = read_file(COMPETITORS_FILE)

                print("\nCompetitors Registered:")
                print(f"{'ID':<5}{'Name':<20}{'Gender':<10}{'Age':<5}")
                print("-" * 40)

                for line in competitors:
                    fields = line.split(",")
                    if len(fields) == 4:  # Ensure the line has 4 parts (ID, Name, Gender, Age)
                        competitor_id, name, gender, age = fields
                        if competitor_id in competitor_ids:
                            print(f"{competitor_id:<5}{name:<20}{gender:<10}{age:<5}")

        elif option == 2:
            # Displays list of all registered events
            events = read_file(EVENTS_FILE)
            if not events:
                print("No events registered.")
            else:
                # Filters any wrong lines or empty entries
                valid_events = [line for line in events if "," in line and len(line.split(",")) > 1]
                # Sort the events alphabetically by event name (second element)
                event_display = sorted(valid_events, key=lambda line: line.split(",")[1].strip().lower())
                print("\nEvents Registered:")
                print("Event ID\tEvent Name")
                print("-" * 40)
                for line in event_display:
                    event_id, event_name = line.split(",", 1)  # Split once into two parts
                    print(f"{event_id}\t\t{event_name}")

        elif option == 3:
            event_id = validate_positive_int("Enter the event ID to view results: ")
            results = read_file(RESULTS_FILE)

            # Filter the results based on the event_id and handle empty or broken lines
            event_results = []
            for line in results:
                parts = line.split(",")
                if len(parts) > 1 and parts[1] == str(
                        event_id):  # Ensure there's at least 2 parts and the event_id matches
                    event_results.append(line)

            if not event_results:
                print(f"No results found for event ID {event_id}.")
            else:
                # Retrieve the event details from the event file
                events = read_file(EVENTS_FILE)
                event_details = None
                for event in events:
                    event_parts = event.split(",")
                    if len(event_parts) >= 2 and event_parts[0] == str(event_id):
                        event_details = event_parts
                        break

                if event_details:
                    print(f"\nEvent Details for Event ID {event_id}")
                    print(f"Event Name: {event_details[1]}")
                else:
                    print(f"Event ID {event_id} not found in the event list.")

                print("\nResults for Event ID", event_id)
                print("Competitor ID\tSwim Time\tCycle Time\tRun Time\tTotal Time")
                print("-" * 50)

                # Sorting competitors based on their total time (index 5)
                sorted_event_results = sorted(event_results, key=lambda x: int(x.split(",")[5]))

                # List competitors and times
                for result in sorted_event_results:
                    parts = result.split(",")
                    if len(parts) >= 6:  # Ensure there are enough elements (ID, Swim, Cycle, Run, Total Time)
                        print(f"{parts[0]}\t{parts[2]}\t{parts[3]}\t{parts[4]}\t{parts[5]}")

                # Gender breakdown percentage male/female
                male_count = 0
                female_count = 0
                total_competitors = len(sorted_event_results)

                # Check the gender of each competitor from the competitors file
                competitors = read_file(COMPETITORS_FILE)
                competitor_genders = {line.split(",")[0]: line.split(",")[2] for line in competitors if
                                      len(line.split(",")) >= 3}

                for result in sorted_event_results:
                    competitor_id = result.split(",")[0]
                    gender = competitor_genders.get(competitor_id, "").strip()
                    if gender == "Male":
                        male_count += 1
                    elif gender == "Female":
                        female_count += 1

                # Calculate and display the gender percentages
                if total_competitors > 0:
                    male_percentage = (male_count / total_competitors) * 100
                    female_percentage = (female_count / total_competitors) * 100
                    print("\nGender Percentage:")
                    print(f"Male: {male_percentage:.2f}%")
                    print(f"Female: {female_percentage:.2f}%")
                else:
                    print("\nNo competitors found for the event.")

        elif option == 4:
            # Option to exit the application
            print("Returning to the main menu.")
            break
        else:
            print("Invalid option. Please choose a valid option.")


# Main menu
def main_menu():
    #Main menu interface
    initialize_files()
    while True:
        print("T R I  T R A C K E R")
        print("1. Register")
        print("2. Record Times")
        print("3. Generate Reports")
        print("4. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            print("Registration Menu")
            print("1. Register Competitor")
            print("2. Register Event")
            sub_choice = input("Select an option: ")
            if sub_choice == "1":
                register_competitor() # Calls the register_competitor function
            elif sub_choice == "2":
                register_event() # Calls the register_event function
            else:
                print("Invalid option.")
        elif choice == "2":
            record_times() # Calls the record_times function
        elif choice == "3":
            generate_reports() # Calls the generate reports function
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid option.")


# Calls the main function to start the program
main_menu()
