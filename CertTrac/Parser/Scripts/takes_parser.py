import csv
from datetime import datetime

# Replace 'New CRLA Tracker.csv' and 'output.csv' with your file names
input_file = 'New CRLA Tracker.csv'
output_file = 'takes.csv'

# Define the indices of the columns you want to select (0, 3 - 25, 31 - 57)
columns_to_select_indices = [0] + [i for i in range(3, 26)] + [i for i in range(31, 58)]

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
            ID = 1
            for row in csv_reader:
                if current_row == 3:
                    # For row 3, generate class list
                    class_list = [row[i] for i in columns_to_select_indices]
                    header_row = ["ID", "Name", "Course", "Semester", "Date"]

                    csv_writer.writerow(header_row)

                if current_row > 3 and current_row < 115:
                    name = row[0]
                    class_num = 0

                    for i in columns_to_select_indices:
                        if i != 0 and row[i]:
                            if " and " in row[i]:
                                    dates = row[i].split(" and ")
                            elif " &" in row[i]:
                                dates = row[i].split(" &")
                            else:
                                dates = row[i].split(" & ")

                            for date in dates:
                                date = date.strip()

                                if date != "Pre-Update Certified 05/11/2022":
                                    sem = date.split(" ")[0]
                                    date = date.split(" ")[1]
                                else:
                                    sem = "Pre-Update Certified"
                                    date = "05/11/2022"

                                #Reverse Date
                                date = datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")

                                columns_to_select = [ID if name != "McCannon, Michael" else -1] + [name] + [class_list[class_num]] + [sem] + [date]

                                csv_writer.writerow(columns_to_select)
                        class_num += 1
                    ID = ID + 1 if name != "McCannon, Michael" else ID
                current_row += 1
    
    print(f"Tutor data has been successfully written to {output_file}")
except FileNotFoundError:
    print("The input CSV file was not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")