import pandas as pd
import re
import os
import csv

# Define the regex pattern for three uppercase letters, a hyphen, and two digits
pattern = r'^[A-Z]{3}-\d{2}'

# Directory containing the CSV files
directory = '/Users/ruben/PycharmProjects/PDFExtract/files/Misc/'

# Path to the output CSV file (the master file)
output_file_path = '/Users/ruben/PycharmProjects/PDFExtract/files/Misc/master_file.csv'

# Initialize an empty DataFrame to collect all filtered rows
master_df = pd.DataFrame()


def find_first_instance_row(root, search_term):
    file_path= directory + root
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row_number, row in enumerate(reader, start=1):  # Start counting rows at 1
            if search_term in row:
                return row_number
    return None  # Return None if the term is not found

# Iterate through all files in the directory
for filename in os.listdir(directory):
    # Check if the file is a CSV
    if filename.endswith('.csv') and filename != 'master_file.csv':

        # The term to search for
        search_term = "CONTRACT MONTH"

        # Find the row number
        row_number = find_first_instance_row(filename, search_term)

        if row_number:
            print(f"The term '{search_term}' was first found at row number {row_number}.")
        else:
            print(f"The term '{search_term}' was not found in the file.")
        # Construct full file path
        file_path = os.path.join(directory, filename)

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path, skiprows=row_number)

        # Filter rows where the first column matches the specified pattern
        # Assuming the data is in the first column, adjust 'df.iloc[:, 0]' if necessary
        filtered_df = df[df.iloc[:, 0].astype(str).apply(lambda x: bool(re.match(pattern, x)))]

        # Append the filtered DataFrame to the master DataFrame
        master_df = pd.concat([master_df, filtered_df], ignore_index=True)

# Save the master DataFrame to the master CSV file
master_df.to_csv(output_file_path, index=False)

print("All filtered rows have been saved to the master CSV file.")

