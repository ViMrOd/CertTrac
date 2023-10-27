# CertTracApp/management/commands/import_data.py
import csv
from django.core.management.base import BaseCommand
from CertTracApp.models import Tutor  # Import your Django model

class Command(BaseCommand):
    help = 'Import data from a CSV file into the database'

    def handle(self, *args, **options):
        csv_file = 'tutor.csv'  # Replace with the path to your CSV file

        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row if it exists

            for row in csv_reader:
                tutor = row[0]
                name = row[1]
                level = row[2]
                date_hired = row[3]
                level = row[12]

                level_1_hours = row[4]
                level_1_hours_in_person = row[5]
                logged_25_hours_level_1 = row[6]
                level_1_complete = row[7]

                level_2_hours = row[8]
                level_2_hours_in_person = row[9]
                logged_25_hours_level_2 = row[10]
                level_2_complete = row[11]

                if email == 'mmccan11@kent.edu':  # Check if this is the special row
                    # Create a new instance of your Django model with ID = -1
                    instance = Tutor(id = -1, first_name = first_name, last_name = last_name, email = email, date_hired = date_hired, 
                                         level = level, 
                                         level_1_hours = level_1_hours, level_1_hours_in_person = level_1_hours_in_person,
                                         logged_25_hours_level_1 = logged_25_hours_level_1, level_1_complete = level_1_complete,
                                         level_2_hours = level_2_hours, level_2_hours_in_person = level_2_hours_in_person,
                                         logged_25_hours_level_2 = logged_25_hours_level_2, level_2_complete = level_2_complete)
                else:
                    # Create a new instance of your Django model (ID will auto-increment)
                    instance = Tutor(first_name = first_name, last_name = last_name, email = email, date_hired = date_hired, 
                                         level = level, 
                                         level_1_hours = level_1_hours, level_1_hours_in_person = level_1_hours_in_person,
                                         logged_25_hours_level_1 = logged_25_hours_level_1, level_1_complete = level_1_complete,
                                         level_2_hours = level_2_hours, level_2_hours_in_person = level_2_hours_in_person,
                                         logged_25_hours_level_2 = logged_25_hours_level_2, level_2_complete = level_2_complete)

                # Save the instance to the database
                instance.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))