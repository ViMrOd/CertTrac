import csv
from datetime import datetime

# Replace 'New CRLA Tracker.csv' and 'output.csv' with your file names
input_file = 'New CRLA Tracker.csv'
output_file = 'tutor.csv'

# Define the indices of the columns you want to select 
columns_to_select_indices = [26, 27, 28, 30, 58, 59, 60, 62]

try:
    with open(input_file, 'r', newline='') as csv_file:
        # Create a CSV reader
        csv_reader = csv.reader(csv_file)
        
        with open(output_file, 'w', newline='') as csv_output_file:
            # Create a CSV writer
            csv_writer = csv.writer(csv_output_file)
            
            # Initialize a counter for the current row
            current_row = 1
            
            # Iterate through the CSV rows
            for row in csv_reader:
                if current_row == 3:
                    # For row 3, print only the specific columns you mentioned
                    header_row = ["First Name", "Last Name"] +["Email"] + ["Date Hired"] + ["level"] + [row[i] for i in columns_to_select_indices]

                    csv_writer.writerow(header_row)

                elif current_row > 3 and current_row < 115:
                    tutor_name = row[0]
                    
                    # Check if there is a space character in the tutor name before splitting
                    first_name = tutor_name.split(", ")[1]
                    last_name = tutor_name.split(", ")[0]

                    #Columns 28, 30, 60, 62 Reverse Date
                    logged_25_hours_level_1 = row[28]
                    if logged_25_hours_level_1:
                        logged_25_hours_level_1 = datetime.strptime(logged_25_hours_level_1, "%m/%d/%y").strftime("20%y-%m-%d")

                    level_1_complete = row[30]
                    if level_1_complete and level_1_complete != "N/A":
                        level_1_complete = datetime.strptime(level_1_complete, "%m/%d/%y").strftime("20%y-%m-%d")
                    else:
                        level_1_complete = ""

                    logged_25_hours_level_2 = row[60]
                    if logged_25_hours_level_2:
                        logged_25_hours_level_2 = datetime.strptime(logged_25_hours_level_2, "%m/%d/%y").strftime("20%y-%m-%d")

                    level_2_complete = row[62]
                    if level_2_complete:
                        level_2_complete = datetime.strptime(level_2_complete, "%m/%d/%y").strftime("20%y-%m-%d")

                    #Have put 0 for Trevor Walko for Level 2 Hours

                    #Calculate Level
                    level = -1

                    if row[30] != "N/A" and row[62]:
                        level = 2
                    if row[30] != "N/A" and not row[62]:
                        level = 1
                    if row[30] == "N/A" and not row[62]:
                        level = 0
                        
                    # Select and write the specific columns you mentioned
                    columns_to_select = [first_name, last_name] + [row[1]] + [row[2]] + [level] + [row[26]] + [row[27]] + [logged_25_hours_level_1] + [level_1_complete] + [row[58]] + [row[59]] + [logged_25_hours_level_2] + [level_2_complete]
                    
                    # Write the selected columns to the CSV file
                    csv_writer.writerow(columns_to_select)

                current_row += 1
    
    print(f"Tutor data has been successfully written to {output_file}")
except FileNotFoundError:
    print("The input CSV file was not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
