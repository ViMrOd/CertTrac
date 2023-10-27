import csv

# Replace 'New CRLA Tracker.csv' and 'output.csv' with your file names
input_file = 'New CRLA Tracker.csv'
output_file = 'course.csv'

# Define the indices of the columns you want to select (0, 3 - 25, 31 - 57)
columns_to_select_indices = [i for i in range(3, 26)] + [i for i in range(31, 58)]

try:
    with open(input_file, 'r', newline='') as csv_file:
        # Create a CSV reader
        csv_reader = csv.reader(csv_file)

        current_row = 1
        
        with open(output_file, 'w', newline='') as csv_output_file:
            # Create a CSV writer
            csv_writer = csv.writer(csv_output_file)

            header_row = ["Name", "Type", "Level"]
            csv_writer.writerow(header_row)
            
            # Iterate through the CSV rows
            for row in csv_reader:
                if current_row == 3:
                    for i in columns_to_select_indices:
                        if i < 31:
                            level = 1
                        else:
                            level = 2

                        if i in range(3, 7) or i in range(31, 37):
                            type = "Basics"
                        elif i in range(7, 11) or i in range(37, 43):
                            type = "Commmunication"
                        elif i in range(11, 17) or i in range(43, 49):
                            type = "Learning & Study Techniques"
                        elif i in range(17, 20) or i in range(49, 53):
                            type = "Ethics & Equality"
                        elif i in range(20, 26) or i in range(53, 58):
                            type = "Electives"

                        courses = [row[i]] + [type] + [level]
                        csv_writer.writerow(courses)
                    break
                
                current_row += 1
                    
    print(f"Tutor data has been successfully written to {output_file}")
except FileNotFoundError:
    print("The input CSV file was not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")